"""
Temporal Marker Loader
======================

Load 54 Prophetic era event markers from CSV into PostgreSQL database.

Features:
- CSV parsing with validation
- Pydantic model validation
- Hierarchical relationship verification
- Transaction safety
"""

import csv
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger

sys.path.insert(0, str(Path(__file__).parents[2]))

from src.models.temporal import TemporalMarker
from dotenv import load_dotenv
import os

load_dotenv()


class MarkerLoader:
    """
    Loads temporal marker data from CSV into PostgreSQL database.
    """

    def __init__(self, database_url: Optional[str] = None):
        """Initialize the marker loader."""
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql://ikb_user:changeme123@localhost:5432/islamic_kb"
        )
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

        self.stats = {
            "total_markers": 0,
            "loaded": 0,
            "errors": 0,
            "validation_errors": 0
        }

        logger.info(f"MarkerLoader initialized with database: {self.database_url}")

    def parse_date(self, date_str: str) -> Optional[date]:
        """Parse date from CSV (format: YYYY-MM-DD)."""
        if not date_str or date_str.strip() == "":
            return None
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None

    def load_csv(self, csv_path: str) -> List[Dict[str, Any]]:
        """
        Load and parse CSV file.

        Args:
            csv_path: Path to Prophetic_era_markers__v1_.csv

        Returns:
            List of marker dictionaries
        """
        path = Path(csv_path)
        if not path.exists():
            logger.error(f"CSV file not found: {csv_path}")
            return []

        markers = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    markers.append(row)

            logger.info(f"Loaded {len(markers)} markers from CSV")
            return markers

        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            return []

    def validate_and_convert_marker(
        self,
        marker_data: Dict[str, Any]
    ) -> Optional[TemporalMarker]:
        """
        Validate marker data using Pydantic.

        Args:
            marker_data: Raw marker dictionary from CSV

        Returns:
            TemporalMarker model or None if validation fails
        """
        try:
            # Parse dates (ce_start and ce_end in CSV)
            ce_start = self.parse_date(marker_data.get('ce_start', ''))
            ce_end = self.parse_date(marker_data.get('ce_end', ''))

            # Build validated model (map CSV columns to model fields)
            marker = TemporalMarker(
                event_id=marker_data['id'],
                parent_event_id=marker_data.get('parent') or None,
                depth=int(marker_data['depth']),
                era_category=None,  # Not in CSV, will derive from id (E0, E1, etc.)
                ce_start=ce_start,
                ce_end=ce_end,
                ah_value=marker_data.get('ah') or None,
                event_name_english=marker_data['marker'],
                event_name_arabic=None,  # Not in this CSV
                location=marker_data.get('place') or None,
                significance=None,  # Not in CSV
                certainty_date=marker_data.get('cert_date') or None,
                certainty_event=marker_data.get('cert_event') or None,
                source_tradition=marker_data.get('source_tradition') or None,
                notes=marker_data.get('notes') or None
            )
            return marker

        except (KeyError, ValueError) as e:
            logger.warning(f"Validation error for marker {marker_data.get('id', 'unknown')}: {e}")
            self.stats["validation_errors"] += 1
            return None
        except Exception as e:
            logger.warning(f"Unexpected error for marker {marker_data.get('id', 'unknown')}: {e}")
            self.stats["validation_errors"] += 1
            return None

    def insert_marker(
        self,
        session: Session,
        marker: TemporalMarker
    ) -> bool:
        """
        Insert a single marker into the database.

        Args:
            session: SQLAlchemy session
            marker: TemporalMarker model

        Returns:
            True if successful, False otherwise
        """
        try:
            stmt = text("""
                INSERT INTO temporal_markers (
                    event_id, parent_event_id, depth, era_category,
                    ce_start, ce_end, ah_value,
                    event_name_english, event_name_arabic,
                    location, significance,
                    certainty_date, certainty_event,
                    source_tradition, notes
                ) VALUES (
                    :event_id, :parent_event_id, :depth, :era_category,
                    :ce_start, :ce_end, :ah_value,
                    :event_name_english, :event_name_arabic,
                    :location, :significance,
                    :certainty_date, :certainty_event,
                    :source_tradition, :notes
                )
            """)

            session.execute(stmt, {
                "event_id": marker.event_id,
                "parent_event_id": marker.parent_event_id,
                "depth": marker.depth,
                "era_category": marker.era_category,
                "ce_start": marker.ce_start,
                "ce_end": marker.ce_end,
                "ah_value": marker.ah_value,
                "event_name_english": marker.event_name_english,
                "event_name_arabic": marker.event_name_arabic,
                "location": marker.location,
                "significance": marker.significance,
                "certainty_date": marker.certainty_date,
                "certainty_event": marker.certainty_event,
                "source_tradition": marker.source_tradition,
                "notes": marker.notes
            })
            return True

        except Exception as e:
            logger.error(f"Error inserting marker {marker.event_id}: {e}")
            self.stats["errors"] += 1
            return False

    def load_from_csv(
        self,
        csv_path: str,
        dry_run: bool = False
    ) -> Dict[str, int]:
        """
        Load all temporal markers from CSV file.

        Args:
            csv_path: Path to CSV file
            dry_run: If True, validate but don't insert

        Returns:
            Dictionary with loading statistics
        """
        logger.info(f"Starting temporal marker loading from {csv_path}")
        logger.info(f"Dry run: {dry_run}")

        # Load CSV
        markers_data = self.load_csv(csv_path)
        self.stats["total_markers"] = len(markers_data)

        if not markers_data:
            logger.error("No markers found in CSV!")
            return self.stats

        # Process markers
        session = self.SessionLocal()
        markers = []

        try:
            # Validate all markers first
            for marker_data in markers_data:
                marker = self.validate_and_convert_marker(marker_data)
                if marker:
                    markers.append(marker)

            logger.info(f"Validated {len(markers)} markers")

            # Insert in order (parents before children)
            if not dry_run:
                # Sort by depth to ensure parents exist before children
                markers.sort(key=lambda m: m.depth)

                for marker in markers:
                    if self.insert_marker(session, marker):
                        self.stats["loaded"] += 1

                session.commit()

            session.close()

        except Exception as e:
            logger.error(f"Fatal error during loading: {e}")
            session.rollback()
            session.close()
            raise

        # Log statistics
        logger.info("=" * 60)
        logger.info("TEMPORAL MARKER LOADING COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total markers in CSV: {self.stats['total_markers']}")
        logger.info(f"Successfully loaded: {self.stats['loaded']}")
        logger.info(f"Validation errors: {self.stats['validation_errors']}")
        logger.info(f"Insert errors: {self.stats['errors']}")
        logger.info("=" * 60)

        return self.stats

    def verify_data(self) -> Dict[str, Any]:
        """Verify loaded marker data."""
        session = self.SessionLocal()
        results = {}

        try:
            # Count total markers
            result = session.execute(text("SELECT COUNT(*) FROM temporal_markers"))
            results["total_markers"] = result.scalar()

            # Count by era
            result = session.execute(text("""
                SELECT era_category, COUNT(*) as count
                FROM temporal_markers
                WHERE era_category IS NOT NULL
                GROUP BY era_category
                ORDER BY era_category
            """))
            results["by_era"] = [
                {"era": row[0], "count": row[1]}
                for row in result.fetchall()
            ]

            # Count by depth
            result = session.execute(text("""
                SELECT depth, COUNT(*) as count
                FROM temporal_markers
                GROUP BY depth
                ORDER BY depth
            """))
            results["by_depth"] = [
                {"depth": row[0], "count": row[1]}
                for row in result.fetchall()
            ]

            # Verify hierarchical relationships
            result = session.execute(text("""
                SELECT COUNT(*) FROM temporal_markers
                WHERE parent_event_id IS NOT NULL
                AND parent_event_id NOT IN (SELECT event_id FROM temporal_markers)
            """))
            results["orphaned_markers"] = result.scalar()

        finally:
            session.close()

        return results


def main():
    """Main entry point for marker loading script."""
    import argparse

    parser = argparse.ArgumentParser(description="Load temporal markers from CSV into PostgreSQL")
    parser.add_argument(
        "--csv-path",
        default="../../Prophetic_era_markers__v1_.csv",
        help="Path to temporal markers CSV file"
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
    loader = MarkerLoader()

    # Load markers
    stats = loader.load_from_csv(
        csv_path=args.csv_path,
        dry_run=args.dry_run
    )

    # Verify if requested
    if args.verify and not args.dry_run:
        logger.info("\nVerifying loaded data...")
        verification = loader.verify_data()
        logger.info(f"Total markers in database: {verification['total_markers']}")
        logger.info(f"Orphaned markers: {verification['orphaned_markers']}")
        logger.info(f"\nMarkers by era:")
        for era in verification['by_era']:
            logger.info(f"  {era['era']}: {era['count']}")
        logger.info(f"\nMarkers by depth:")
        for depth in verification['by_depth']:
            logger.info(f"  Depth {depth['depth']}: {depth['count']}")

    return stats


if __name__ == "__main__":
    main()
