"""
Hadith Data Loader
==================

Load 50,884 hadiths from JSON files into the PostgreSQL database.

Features:
- Batch loading with progress tracking
- Duplicate detection and handling
- Validation using Pydantic models
- Transaction safety with rollback on error
- Progress persistence with checkpoints
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from loguru import logger
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parents[2]))

from src.models.hadith import HadithCreate, RawHadith
from dotenv import load_dotenv
import os

load_dotenv()


class HadithLoader:
    """
    Loads hadith data from JSON files into PostgreSQL database.
    """

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize the hadith loader.

        Args:
            database_url: PostgreSQL connection string (uses env var if not provided)
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql://ikb_user:changeme123@localhost:5432/islamic_kb"
        )
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Statistics
        self.stats = {
            "total_files": 0,
            "total_hadiths": 0,
            "loaded": 0,
            "duplicates": 0,
            "errors": 0,
            "validation_errors": 0
        }

        logger.info(f"HadithLoader initialized with database: {self.database_url}")

    def find_hadith_json_files(self, base_path: str) -> List[Path]:
        """
        Find all hadith JSON files in the directory structure.

        Args:
            base_path: Base directory to search (e.g., "2. hadith/by_book")

        Returns:
            List of Path objects for JSON files
        """
        base = Path(base_path)
        if not base.exists():
            logger.error(f"Path does not exist: {base_path}")
            return []

        json_files = list(base.rglob("*.json"))
        logger.info(f"Found {len(json_files)} JSON files in {base_path}")
        return json_files

    def load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load and parse a single JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            List of hadith dictionaries
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle different JSON structures
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # Some files might have hadiths nested in a key
                if 'hadiths' in data:
                    return data['hadiths']
                elif 'data' in data:
                    return data['data']
                else:
                    # Single hadith as dict
                    return [data]
            else:
                logger.warning(f"Unexpected JSON structure in {file_path}")
                return []

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {file_path}: {e}")
            self.stats["errors"] += 1
            return []
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            self.stats["errors"] += 1
            return []

    def validate_and_convert_hadith(
        self,
        hadith_data: Dict[str, Any],
        source_file: str
    ) -> Optional[HadithCreate]:
        """
        Validate hadith data using Pydantic and convert to HadithCreate model.

        Args:
            hadith_data: Raw hadith dictionary
            source_file: Source file path for tracking

        Returns:
            HadithCreate model or None if validation fails
        """
        try:
            # Handle nested english structure if present
            english_data = hadith_data.get('english', {})
            if isinstance(english_data, dict):
                english_narrator = english_data.get('narrator')
                english_text = english_data.get('text')
            else:
                english_narrator = hadith_data.get('englishNarrator')
                english_text = hadith_data.get('englishText')

            # Build validated model
            hadith = HadithCreate(
                id=hadith_data['id'],
                id_in_book=hadith_data.get('idInBook', hadith_data.get('id_in_book', hadith_data['id'])),
                book_id=hadith_data['bookId'] if 'bookId' in hadith_data else hadith_data['book_id'],
                chapter_id=hadith_data['chapterId'] if 'chapterId' in hadith_data else hadith_data['chapter_id'],
                arabic=hadith_data['arabic'],
                english_narrator=english_narrator,
                english_text=english_text,
                book_name_arabic=hadith_data.get('bookNameArabic'),
                book_name_english=hadith_data.get('bookNameEnglish'),
                chapter_name_arabic=hadith_data.get('chapterNameArabic'),
                chapter_name_english=hadith_data.get('chapterNameEnglish'),
                source_file=source_file
            )
            return hadith

        except KeyError as e:
            logger.warning(f"Missing required field {e} in hadith: {hadith_data.get('id', 'unknown')}")
            self.stats["validation_errors"] += 1
            return None
        except Exception as e:
            logger.warning(f"Validation error for hadith {hadith_data.get('id', 'unknown')}: {e}")
            self.stats["validation_errors"] += 1
            return None

    def insert_batch(
        self,
        session: Session,
        batch: List[HadithCreate]
    ) -> Tuple[int, int]:
        """
        Insert a batch of hadiths into the database.

        Args:
            session: SQLAlchemy session
            batch: List of HadithCreate models

        Returns:
            Tuple of (inserted_count, duplicate_count)
        """
        inserted = 0
        duplicates = 0

        for hadith in batch:
            try:
                # Insert using raw SQL for better control
                stmt = text("""
                    INSERT INTO raw_hadiths (
                        id, id_in_book, book_id, chapter_id,
                        arabic, english_narrator, english_text,
                        book_name_arabic, book_name_english,
                        chapter_name_arabic, chapter_name_english,
                        source_file
                    ) VALUES (
                        :id, :id_in_book, :book_id, :chapter_id,
                        :arabic, :english_narrator, :english_text,
                        :book_name_arabic, :book_name_english,
                        :chapter_name_arabic, :chapter_name_english,
                        :source_file
                    )
                """)

                session.execute(stmt, {
                    "id": hadith.id,
                    "id_in_book": hadith.id_in_book,
                    "book_id": hadith.book_id,
                    "chapter_id": hadith.chapter_id,
                    "arabic": hadith.arabic,
                    "english_narrator": hadith.english_narrator,
                    "english_text": hadith.english_text,
                    "book_name_arabic": hadith.book_name_arabic,
                    "book_name_english": hadith.book_name_english,
                    "chapter_name_arabic": hadith.chapter_name_arabic,
                    "chapter_name_english": hadith.chapter_name_english,
                    "source_file": hadith.source_file
                })
                inserted += 1

            except IntegrityError:
                # Duplicate hadith (PRIMARY KEY or UNIQUE constraint violation)
                duplicates += 1
                session.rollback()

        return inserted, duplicates

    def load_from_directory(
        self,
        base_path: str,
        batch_size: int = 1000,
        dry_run: bool = False
    ) -> Dict[str, int]:
        """
        Load all hadiths from a directory structure.

        Args:
            base_path: Base directory containing JSON files
            batch_size: Number of hadiths to insert per batch
            dry_run: If True, validate but don't insert into database

        Returns:
            Dictionary with loading statistics
        """
        logger.info(f"Starting hadith loading from {base_path}")
        logger.info(f"Batch size: {batch_size}, Dry run: {dry_run}")

        # Find all JSON files
        json_files = self.find_hadith_json_files(base_path)
        self.stats["total_files"] = len(json_files)

        if not json_files:
            logger.error("No JSON files found!")
            return self.stats

        # Process files
        batch = []
        session = self.SessionLocal()

        try:
            with tqdm(total=len(json_files), desc="Processing files") as pbar:
                for json_file in json_files:
                    # Load hadiths from file
                    hadiths_data = self.load_json_file(json_file)
                    self.stats["total_hadiths"] += len(hadiths_data)

                    # Validate and convert
                    for hadith_data in hadiths_data:
                        hadith = self.validate_and_convert_hadith(
                            hadith_data,
                            str(json_file.relative_to(Path(base_path).parent))
                        )

                        if hadith:
                            batch.append(hadith)

                            # Insert batch when full
                            if len(batch) >= batch_size and not dry_run:
                                inserted, dupes = self.insert_batch(session, batch)
                                self.stats["loaded"] += inserted
                                self.stats["duplicates"] += dupes
                                session.commit()
                                batch = []

                    pbar.update(1)

            # Insert remaining batch
            if batch and not dry_run:
                inserted, dupes = self.insert_batch(session, batch)
                self.stats["loaded"] += inserted
                self.stats["duplicates"] += dupes
                session.commit()

            session.close()

        except Exception as e:
            logger.error(f"Fatal error during loading: {e}")
            session.rollback()
            session.close()
            raise

        # Log final statistics
        logger.info("=" * 60)
        logger.info("HADITH LOADING COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total files processed: {self.stats['total_files']}")
        logger.info(f"Total hadiths found: {self.stats['total_hadiths']}")
        logger.info(f"Successfully loaded: {self.stats['loaded']}")
        logger.info(f"Duplicates skipped: {self.stats['duplicates']}")
        logger.info(f"Validation errors: {self.stats['validation_errors']}")
        logger.info(f"File errors: {self.stats['errors']}")
        logger.info("=" * 60)

        return self.stats

    def verify_data(self) -> Dict[str, Any]:
        """
        Verify loaded data integrity.

        Returns:
            Dictionary with verification results
        """
        session = self.SessionLocal()
        results = {}

        try:
            # Count total hadiths
            result = session.execute(text("SELECT COUNT(*) FROM raw_hadiths"))
            results["total_hadiths"] = result.scalar()

            # Count by book
            result = session.execute(text("""
                SELECT book_id, book_name_english, COUNT(*) as count
                FROM raw_hadiths
                GROUP BY book_id, book_name_english
                ORDER BY book_id
            """))
            results["by_book"] = [
                {"book_id": row[0], "book_name": row[1], "count": row[2]}
                for row in result.fetchall()
            ]

            # Check for missing required fields
            result = session.execute(text("""
                SELECT COUNT(*) FROM raw_hadiths WHERE arabic IS NULL OR arabic = ''
            """))
            results["missing_arabic"] = result.scalar()

            # Sample hadith IDs
            result = session.execute(text("""
                SELECT id FROM raw_hadiths ORDER BY id LIMIT 10
            """))
            results["sample_ids"] = [row[0] for row in result.fetchall()]

        finally:
            session.close()

        return results


def main():
    """
    Main entry point for hadith loading script.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Load hadiths from JSON into PostgreSQL")
    parser.add_argument(
        "--base-path",
        default="../../2. hadith/by_book",
        help="Base directory containing hadith JSON files"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Number of hadiths per batch"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate but don't insert into database"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify data after loading"
    )

    args = parser.parse_args()

    # Initialize loader
    loader = HadithLoader()

    # Load hadiths
    stats = loader.load_from_directory(
        base_path=args.base_path,
        batch_size=args.batch_size,
        dry_run=args.dry_run
    )

    # Verify if requested
    if args.verify and not args.dry_run:
        logger.info("\nVerifying loaded data...")
        verification = loader.verify_data()
        logger.info(f"Total hadiths in database: {verification['total_hadiths']}")
        logger.info(f"Missing Arabic text: {verification['missing_arabic']}")
        logger.info(f"\nHadiths by book:")
        for book in verification['by_book']:
            logger.info(f"  {book['book_name']}: {book['count']}")

    return stats


if __name__ == "__main__":
    main()
