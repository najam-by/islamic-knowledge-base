"""
Temporal Assignment Models (PCAP)
=================================

Pydantic models for PCAP temporal assignment data.

Models:
- TemporalMarker: Prophetic era event reference
- EvidenceType: Enum for evidence classification
- PCAPOutput: Temporal assignment with confidence
- PCAPAssignment: Complete database record with metadata
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, field_validator


class EvidenceType(str, Enum):
    """Types of evidence for temporal assignment."""
    EXPLICIT_TEXT = "explicit_text"
    EXPLICIT_EVENT = "explicit_event"
    ISNAD_GENERATION = "isnad_generation"
    SIRAH_ALIGNMENT = "sirah_alignment"
    CONTEXTUAL_ORDER = "contextual_order"
    SPECULATIVE = "speculative"


class TemporalMarker(BaseModel):
    """
    Prophetic era event reference marker.

    Maps to: temporal_markers table
    """
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        json_schema_extra={
            "example": {
                "event_id": "E2.1",
                "parent_event_id": "E2",
                "depth": 1,
                "era_category": "E2",
                "ce_start": "624-03-13",
                "ce_end": "624-03-13",
                "ah_value": "2",
                "event_name_english": "Battle of Badr",
                "location": "Badr, Hejaz",
                "significance": "First major military victory",
                "certainty_date": "high",
                "certainty_event": "certain"
            }
        }
    )

    event_id: str = Field(..., max_length=20, description="Unique event identifier (e.g., E2.3.1)")
    parent_event_id: Optional[str] = Field(None, max_length=20, description="Parent event in hierarchy")
    depth: int = Field(..., ge=0, le=4, description="Depth in hierarchy (0=era, 1=sub-era, etc.)")
    era_category: Optional[str] = Field(None, max_length=10, description="Era category (E0, E1, E2, E3)")

    # Dates
    ce_start: Optional[date] = Field(None, description="Common Era start date")
    ce_end: Optional[date] = Field(None, description="Common Era end date")
    ah_value: Optional[str] = Field(None, max_length=50, description="After Hijrah value/range")

    # Names
    event_name_english: str = Field(..., max_length=255)
    event_name_arabic: Optional[str] = Field(None, max_length=255)

    # Details
    location: Optional[str] = Field(None, max_length=255)
    significance: Optional[str] = None
    certainty_date: Optional[str] = Field(None, max_length=10, description="Certainty of date")
    certainty_event: Optional[str] = Field(None, max_length=10, description="Certainty of event occurrence")
    source_tradition: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None
    loaded_at: Optional[datetime] = None


class PCAPOutput(BaseModel):
    """
    PCAP temporal assignment output from LLM.

    This model is used for LLM input/output and validation.
    """
    model_config = ConfigDict(validate_assignment=True)

    # Temporal assignment
    era_id: str = Field(..., pattern=r"^E[0-3](\.\d+)*$", description="Era ID (E0, E1, E2, E3, or sub-era)")
    sub_era_id: Optional[str] = Field(None, pattern=r"^E[0-3]\.\d+$", description="Sub-era ID if applicable")
    event_window_id: Optional[str] = Field(None, description="Specific event window ID")

    # Date ranges (After Hijrah)
    earliest_ah: Decimal = Field(..., ge=-53, le=11, description="Earliest possible AH date")
    latest_ah: Decimal = Field(..., ge=-53, le=11, description="Latest possible AH date")

    # Date ranges (Common Era) - optional
    earliest_ce: Optional[date] = None
    latest_ce: Optional[date] = None

    # Anchor relationships
    anchor_before: List[str] = Field(
        default_factory=list,
        description="Events that must occur before this hadith"
    )
    anchor_after: List[str] = Field(
        default_factory=list,
        description="Events that must occur after this hadith"
    )

    # Evidence and confidence
    evidence_type: EvidenceType = Field(..., description="Type of evidence used")
    posterior_confidence: Decimal = Field(
        ...,
        ge=0,
        le=1,
        decimal_places=3,
        description="Posterior confidence score [0,1]"
    )
    reasoning: str = Field(..., min_length=50, description="Explanation of temporal assignment")

    @field_validator('latest_ah')
    @classmethod
    def validate_ah_order(cls, v: Decimal, info) -> Decimal:
        """Ensure latest_ah >= earliest_ah."""
        if 'earliest_ah' in info.data and v < info.data['earliest_ah']:
            raise ValueError(f"latest_ah ({v}) must be >= earliest_ah ({info.data['earliest_ah']})")
        return v



class PCAPAssignment(PCAPOutput):
    """
    Complete PCAP assignment database record with metadata.

    Maps to: pcap_assignments table
    Extends PCAPOutput with database-specific fields.
    """
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    id: Optional[int] = None
    hadith_id: int = Field(..., description="References raw_hadiths.id")
    version: str = Field("v1.0", max_length=20, description="Processing version")

    # LLM metadata
    llm_model: Optional[str] = Field(None, max_length=100, description="LLM model used")
    llm_cost_usd: Optional[Decimal] = Field(None, ge=0, decimal_places=6, description="API cost in USD")
    processing_duration_ms: Optional[int] = Field(None, ge=0, description="Processing time in milliseconds")

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



class PCAPBatch(BaseModel):
    """
    Batch of PCAP assignments for parallel processing.
    """
    model_config = ConfigDict(validate_assignment=True)

    assignments: List[PCAPAssignment] = Field(..., min_length=1, max_length=1000)
    batch_id: str = Field(..., description="Unique batch identifier")
    version: str = Field("v1.0", description="Processing version")
    total_cost_usd: Optional[Decimal] = Field(None, ge=0)
    total_duration_ms: Optional[int] = Field(None, ge=0)

