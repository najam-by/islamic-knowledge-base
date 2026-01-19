"""
Hadith Data Models
==================

Pydantic models for hadith entities matching the database schema.

Models:
- RawHadith: Immutable source data from JSON files
- PreprocessedHadith: Normalized text with parsed isnad
- HadithIPKSA: Complete enriched hadith (PCAP + HMSTS + links)
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class RawHadith(BaseModel):
    """
    Immutable source hadith data from sunnah.com JSON files.

    Maps to: raw_hadiths table
    """
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "id_in_book": 1,
                "book_id": 1,
                "chapter_id": 1,
                "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ",
                "english_narrator": "Narrated 'Umar bin Al-Khattab",
                "english_text": "The deeds are considered by the intentions",
                "book_name_english": "Sahih al-Bukhari",
                "chapter_name_english": "Revelation"
            }
        }
    )

    id: int = Field(..., description="Unique hadith identifier")
    id_in_book: int = Field(..., description="Hadith number within book")
    book_id: int = Field(..., description="Book collection ID")
    chapter_id: int = Field(..., description="Chapter/section ID")

    # Text content
    arabic: str = Field(..., min_length=1, description="Arabic text of hadith")
    english_narrator: Optional[str] = Field(None, description="Chain of narration in English")
    english_text: Optional[str] = Field(None, description="English translation of hadith text")

    # Metadata
    book_name_arabic: Optional[str] = Field(None, max_length=255)
    book_name_english: Optional[str] = Field(None, max_length=255)
    chapter_name_arabic: Optional[str] = None
    chapter_name_english: Optional[str] = None
    source_file: Optional[str] = Field(None, max_length=500, description="Source JSON file path")
    loaded_at: Optional[datetime] = Field(None, description="Timestamp when loaded into DB")


class PreprocessedHadith(BaseModel):
    """
    Preprocessed hadith with normalized text and parsed isnad.

    Maps to: preprocessed_hadiths table
    """
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "hadith_id": 1,
                "arabic_normalized": "انما الاعمال بالنيات",
                "isnad_chain": ["Umar bin Al-Khattab", "Hafs bin Aasim", "Yahya bin Sa'id"],
                "isnad_generation": 0,
                "explicit_temporal_references": [],
                "has_explicit_date": False,
                "text_length_arabic": 156,
                "text_length_english": 89
            }
        }
    )

    hadith_id: int = Field(..., description="References raw_hadiths.id")

    # Normalized text
    arabic_normalized: Optional[str] = Field(None, description="Normalized Arabic text")
    english_normalized: Optional[str] = Field(None, description="Normalized English text")

    # Isnad parsing
    isnad_chain: Optional[List[str]] = Field(
        None,
        description="Parsed chain of narrators (ordered from Prophet backward)"
    )
    isnad_generation: Optional[int] = Field(
        None,
        ge=0,
        le=10,
        description="Generation count in chain (0=Sahaba, 1=Tabi'un, etc.)"
    )

    # Temporal markers
    explicit_temporal_references: Optional[List[str]] = Field(
        None,
        description="Explicit date/event references found in text"
    )
    explicit_person_references: Optional[List[str]] = Field(
        None,
        description="Explicit person names found in text"
    )

    # Text statistics
    text_length_arabic: Optional[int] = Field(None, ge=0)
    text_length_english: Optional[int] = Field(None, ge=0)
    has_explicit_date: bool = Field(False, description="True if text contains explicit date")

    # Metadata
    processed_at: Optional[datetime] = None
    preprocessing_version: str = Field("1.0", max_length=20)


class HadithCreate(BaseModel):
    """
    Model for creating new hadith entries (without auto-generated fields).
    Used for data ingestion.
    """
    model_config = ConfigDict(validate_assignment=True)

    id: int
    id_in_book: int
    book_id: int
    chapter_id: Optional[int] = None  # Some hadiths have null chapter_id
    arabic: str = Field(..., min_length=1)
    english_narrator: Optional[str] = None
    english_text: Optional[str] = None
    book_name_arabic: Optional[str] = None
    book_name_english: Optional[str] = None
    chapter_name_arabic: Optional[str] = None
    chapter_name_english: Optional[str] = None
    source_file: Optional[str] = None


class HadithSummary(BaseModel):
    """
    Lightweight hadith summary for list views.
    """
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "book_id": 1,
                "book_name_english": "Sahih al-Bukhari",
                "chapter_name_english": "Revelation",
                "arabic": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ...",
                "english_text": "The deeds are considered by the intentions..."
            }
        }
    )

    id: int
    book_id: int
    book_name_english: Optional[str] = None
    chapter_name_english: Optional[str] = None
    arabic: str = Field(..., max_length=200, description="Truncated Arabic text")
    english_text: Optional[str] = Field(None, max_length=200, description="Truncated English text")
