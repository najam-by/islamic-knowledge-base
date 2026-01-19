"""
Processing State and Checkpoint Models
======================================

Pydantic models for tracking processing state, checkpoints, and batch progress.

Models:
- ProcessingStage: Enum for pipeline stages
- ProcessingStatus: Enum for status tracking
- Checkpoint: Resume point for processing
- BatchProgress: Progress tracking for current batch
- ProcessingState: Complete processing state
- ProcessingStatistics: Summary statistics
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class ProcessingStage(str, Enum):
    """Pipeline processing stages."""
    INITIALIZATION = "initialization"
    INGESTION = "ingestion"
    PREPROCESSING = "preprocessing"
    PCAP_PROCESSING = "pcap_processing"
    HMSTS_PROCESSING = "hmsts_processing"
    CROSS_LINKING = "cross_linking"
    VALIDATION = "validation"
    GRAPH_CONSTRUCTION = "graph_construction"
    EXPORT = "export"
    COMPLETE = "complete"


class ProcessingStatus(str, Enum):
    """Processing status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Checkpoint(BaseModel):
    """
    Processing checkpoint for resume capability.
    """
    model_config = ConfigDict(validate_assignment=True)

    checkpoint_id: str = Field(..., description="Unique checkpoint identifier")
    stage: ProcessingStage = Field(..., description="Current processing stage")
    version: str = Field("v1.0", max_length=20)

    # Progress tracking
    last_processed_hadith_id: int = Field(..., description="Last successfully processed hadith")
    total_processed: int = Field(..., ge=0, description="Total hadiths processed so far")
    total_remaining: int = Field(..., ge=0, description="Hadiths remaining")

    # State data
    batch_number: int = Field(..., ge=1)
    worker_id: Optional[str] = None
    state_data: Optional[Dict[str, Any]] = Field(None, description="Additional state information")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    valid_until: Optional[datetime] = Field(None, description="Checkpoint expiration")

    class Config:
        json_schema_extra = {
            "example": {
                "checkpoint_id": "ckpt_pcap_batch_005",
                "stage": "pcap_processing",
                "version": "v1.0",
                "last_processed_hadith_id": 500,
                "total_processed": 500,
                "total_remaining": 50384,
                "batch_number": 5,
                "state_data": {
                    "parallel_workers": 5,
                    "batch_size": 100
                }
            }
        }


class BatchProgress(BaseModel):
    """
    Real-time progress tracking for current batch.
    """
    model_config = ConfigDict(validate_assignment=True)

    batch_id: str = Field(..., description="Current batch identifier")
    stage: ProcessingStage = Field(..., description="Current stage")
    status: ProcessingStatus = Field(..., description="Current status")

    # Progress metrics
    total_items: int = Field(..., ge=1)
    processed_items: int = Field(0, ge=0)
    failed_items: int = Field(0, ge=0)
    skipped_items: int = Field(0, ge=0)

    # Timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    estimated_completion: Optional[datetime] = None
    actual_completion: Optional[datetime] = None

    # Resource usage
    llm_calls_made: int = Field(0, ge=0)
    total_cost_usd: Decimal = Field(Decimal(0), ge=0, decimal_places=6)
    total_tokens_used: int = Field(0, ge=0)
    avg_processing_time_ms: Optional[int] = Field(None, ge=0)

    # Error tracking
    errors: List[str] = Field(default_factory=list)
    last_error: Optional[str] = None
    retry_count: int = Field(0, ge=0)

    @property
    def progress_percentage(self) -> float:
        """Calculate progress as percentage."""
        if self.total_items == 0:
            return 0.0
        return round((self.processed_items / self.total_items) * 100, 2)

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.processed_items == 0:
            return 0.0
        successful = self.processed_items - self.failed_items
        return round((successful / self.processed_items) * 100, 2)

    class Config:
        json_schema_extra = {
            "example": {
                "batch_id": "batch_pcap_005",
                "stage": "pcap_processing",
                "status": "in_progress",
                "total_items": 100,
                "processed_items": 75,
                "failed_items": 2,
                "llm_calls_made": 75,
                "total_cost_usd": 4.50,
                "total_tokens_used": 750000,
                "avg_processing_time_ms": 2500
            }
        }


class ProcessingState(BaseModel):
    """
    Complete processing state for the entire pipeline.
    """
    model_config = ConfigDict(validate_assignment=True)

    session_id: str = Field(..., description="Unique processing session ID")
    version: str = Field("v1.0", max_length=20)
    current_stage: ProcessingStage = Field(..., description="Current pipeline stage")
    status: ProcessingStatus = Field(..., description="Overall processing status")

    # Hadith tracking
    total_hadiths: int = Field(50884, description="Total hadiths in corpus")
    processed_hadiths: int = Field(0, ge=0)
    failed_hadiths: int = Field(0, ge=0)

    # Stage completion
    completed_stages: List[ProcessingStage] = Field(default_factory=list)
    current_checkpoint: Optional[Checkpoint] = None
    current_batch: Optional[BatchProgress] = None

    # Resource totals
    total_llm_cost_usd: Decimal = Field(Decimal(0), ge=0, decimal_places=2)
    total_processing_time_seconds: int = Field(0, ge=0)
    total_llm_calls: int = Field(0, ge=0)

    # Timestamps
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Configuration
    config: Dict[str, Any] = Field(default_factory=dict, description="Processing configuration")

    @property
    def overall_progress_percentage(self) -> float:
        """Calculate overall progress."""
        return round((self.processed_hadiths / self.total_hadiths) * 100, 2)

    @property
    def estimated_total_cost(self) -> Decimal:
        """Estimate total cost based on current progress."""
        if self.processed_hadiths == 0:
            return Decimal(0)
        cost_per_hadith = self.total_llm_cost_usd / Decimal(self.processed_hadiths)
        return round(cost_per_hadith * Decimal(self.total_hadiths), 2)

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_20260119_001",
                "version": "v1.0",
                "current_stage": "pcap_processing",
                "status": "in_progress",
                "total_hadiths": 50884,
                "processed_hadiths": 5000,
                "failed_hadiths": 12,
                "completed_stages": ["initialization", "ingestion", "preprocessing"],
                "total_llm_cost_usd": 300.50,
                "total_llm_calls": 5000,
                "config": {
                    "batch_size": 100,
                    "parallel_workers": 5,
                    "llm_model": "claude-3-5-sonnet-20241022"
                }
            }
        }


class ProcessingStatistics(BaseModel):
    """
    Summary statistics for completed processing.
    """
    model_config = ConfigDict(validate_assignment=True)

    session_id: str
    version: str = Field("v1.0")

    # Completion metrics
    total_hadiths: int = Field(..., ge=0)
    successfully_processed: int = Field(..., ge=0)
    failed: int = Field(..., ge=0)
    success_rate: Decimal = Field(..., ge=0, le=1, decimal_places=4)

    # Stage-specific counts
    pcap_assigned: int = Field(0, ge=0)
    hmsts_tagged: int = Field(0, ge=0)
    cross_linked: int = Field(0, ge=0)
    validated: int = Field(0, ge=0)

    # Quality metrics
    avg_temporal_confidence: Decimal = Field(..., ge=0, le=1, decimal_places=3)
    avg_semantic_completeness: Decimal = Field(..., ge=0, le=1, decimal_places=3)
    avg_quality_score: Decimal = Field(..., ge=0, le=1, decimal_places=3)

    # Resource usage
    total_cost_usd: Decimal = Field(..., ge=0, decimal_places=2)
    total_duration_seconds: int = Field(..., ge=0)
    total_llm_calls: int = Field(..., ge=0)
    total_tokens_used: int = Field(..., ge=0)
    avg_cost_per_hadith: Decimal = Field(..., ge=0, decimal_places=6)
    avg_time_per_hadith_ms: int = Field(..., ge=0)

    # Validation results
    validation_pass_rate: Decimal = Field(..., ge=0, le=1, decimal_places=4)
    hadiths_requiring_review: int = Field(0, ge=0)

    # Timestamps
    started_at: datetime
    completed_at: datetime

    @property
    def total_duration_hours(self) -> float:
        """Total duration in hours."""
        return round(self.total_duration_seconds / 3600, 2)

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_20260119_001",
                "version": "v1.0",
                "total_hadiths": 50884,
                "successfully_processed": 50872,
                "failed": 12,
                "success_rate": 0.9998,
                "pcap_assigned": 50872,
                "hmsts_tagged": 50872,
                "avg_temporal_confidence": 0.82,
                "avg_semantic_completeness": 0.88,
                "avg_quality_score": 0.85,
                "total_cost_usd": 8500.00,
                "total_duration_seconds": 144000,
                "total_llm_calls": 101744,
                "avg_cost_per_hadith": 0.167,
                "validation_pass_rate": 0.9523,
                "hadiths_requiring_review": 247
            }
        }
