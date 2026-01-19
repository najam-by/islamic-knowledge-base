"""
Islamic Knowledge Base - Pydantic Models
========================================

Data models for the IPKSA hadith processing system.
All models match the PostgreSQL database schema and support
LLM input/output validation.

Model Categories:
-----------------
1. Hadith Models (hadith.py):
   - RawHadith, PreprocessedHadith, HadithCreate, HadithSummary

2. Temporal Models (temporal.py):
   - TemporalMarker, EvidenceType, PCAPOutput, PCAPAssignment

3. Semantic Models (semantic.py):
   - Layer0-4 models, InterpretiveLayer, HMSTSOutput, HMSTSAssignment

4. Validation Models (validation.py):
   - ValidationStatus, ValidationResult, QualityMetrics

5. Processing Models (processing.py):
   - ProcessingStage, ProcessingState, Checkpoint, BatchProgress

Usage:
------
    from src.models import RawHadith, PCAPOutput, HMSTSOutput
    from src.models.temporal import EvidenceType
    from src.models.semantic import Modality, FunctionalRole
"""

# Hadith models
from .hadith import (
    RawHadith,
    PreprocessedHadith,
    HadithCreate,
    HadithSummary,
)

# Temporal models
from .temporal import (
    EvidenceType,
    TemporalMarker,
    PCAPOutput,
    PCAPAssignment,
    PCAPBatch,
)

# Semantic models
from .semantic import (
    Modality,
    FunctionalRole,
    Scope,
    Certainty,
    Conditionality,
    Layer0,
    Layer1,
    Layer2,
    InterpretiveLayer,
    Layer3AxisA,
    Layer3AxisB,
    Layer4Vectors,
    HMSTSOutput,
    HMSTSAssignment,
    HMSTSBatch,
)

# Validation models
from .validation import (
    ValidationStatus,
    ValidationCategory,
    ValidationIssue,
    ValidationResult,
    QualityMetrics,
    ValidationBatch,
)

# Processing models
from .processing import (
    ProcessingStage,
    ProcessingStatus,
    Checkpoint,
    BatchProgress,
    ProcessingState,
    ProcessingStatistics,
)

__all__ = [
    # Hadith
    "RawHadith",
    "PreprocessedHadith",
    "HadithCreate",
    "HadithSummary",
    # Temporal
    "EvidenceType",
    "TemporalMarker",
    "PCAPOutput",
    "PCAPAssignment",
    "PCAPBatch",
    # Semantic
    "Modality",
    "FunctionalRole",
    "Scope",
    "Certainty",
    "Conditionality",
    "Layer0",
    "Layer1",
    "Layer2",
    "InterpretiveLayer",
    "Layer3AxisA",
    "Layer3AxisB",
    "Layer4Vectors",
    "HMSTSOutput",
    "HMSTSAssignment",
    "HMSTSBatch",
    # Validation
    "ValidationStatus",
    "ValidationCategory",
    "ValidationIssue",
    "ValidationResult",
    "QualityMetrics",
    "ValidationBatch",
    # Processing
    "ProcessingStage",
    "ProcessingStatus",
    "Checkpoint",
    "BatchProgress",
    "ProcessingState",
    "ProcessingStatistics",
]

__version__ = "1.0.0"
