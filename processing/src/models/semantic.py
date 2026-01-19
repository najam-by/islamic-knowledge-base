"""
Semantic Tagging Models (HMSTS)
===============================

Pydantic models for HMSTS 5-layer semantic tagging.

Models:
- Layer0: Textual fact layer (speaker, modality, verb)
- Layer1: Ontological categories
- Layer2: Functional role
- InterpretiveLayer: Layer 3 axes (hermeneutic, spiritual)
- Layer4Vectors: Thematic vectors
- HMSTSOutput: Complete 5-layer semantic analysis
- HMSTSAssignment: Database record with metadata
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Enums for controlled vocabularies
# ============================================================================

class Modality(str, Enum):
    """Layer 0 modality classification."""
    OBLIGATORY = "obligatory"
    RECOMMENDED = "recommended"
    PERMITTED = "permitted"
    DISCOURAGED = "discouraged"
    FORBIDDEN = "forbidden"
    INFORMATIVE = "informative"


class FunctionalRole(str, Enum):
    """Layer 2 functional role classification."""
    NORMATIVE = "Normative"
    DESCRIPTIVE = "Descriptive"
    EXPLANATORY = "Explanatory"
    CORRECTIVE = "Corrective"
    EXEMPLARY = "Exemplary"
    PROPHETIC_STATE = "Prophetic State"
    DIVINE_ADDRESS = "Divine Address"
    DIVINE_ATTRIBUTE = "Divine Attribute"


class Scope(str, Enum):
    """Scope of application."""
    INDIVIDUAL = "individual"
    COMMUNAL = "communal"
    UNIVERSAL = "universal"


class Certainty(str, Enum):
    """Epistemic certainty level."""
    QATI = "qatʿī"      # Certain
    DHANNI = "ẓannī"    # Probable
    ISHARI = "ishārī"   # Allusive


class Conditionality(str, Enum):
    """Contextual conditionality."""
    ABSOLUTE = "absolute"
    CONTEXTUAL = "contextual"


# ============================================================================
# Layer Models
# ============================================================================

class Layer0(BaseModel):
    """
    Layer 0: Textual Fact Layer
    Basic factual information from the hadith text.
    """
    model_config = ConfigDict(validate_assignment=True)

    speaker: Optional[str] = Field(None, max_length=255, description="Who is speaking")
    addressee: Optional[str] = Field(None, max_length=255, description="Who is being addressed")
    verb_type: Optional[str] = Field(None, max_length=100, description="Type of verb (command, report, etc.)")
    modality: Optional[Modality] = Field(None, description="Deontic modality")

    class Config:
        json_schema_extra = {
            "example": {
                "speaker": "Prophet Muhammad (PBUH)",
                "addressee": "Companions",
                "verb_type": "command",
                "modality": "obligatory"
            }
        }


class Layer1(BaseModel):
    """
    Layer 1: Ontological Category
    High-level categorization of hadith content.
    """
    model_config = ConfigDict(validate_assignment=True)

    categories: List[str] = Field(
        ...,
        min_length=1,
        max_length=5,
        description="Ontological categories (Event, Legislation, Ethics, etc.)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "categories": ["Worship", "Ethics", "Spiritual State"]
            }
        }


class Layer2(BaseModel):
    """
    Layer 2: Functional Role
    Primary communicative function.
    """
    model_config = ConfigDict(validate_assignment=True)

    role: FunctionalRole = Field(..., description="Primary functional role")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "Normative"
            }
        }


class InterpretiveLayer(BaseModel):
    """
    Interpretive layer structure for Layer 3 axes.
    Used for both Axis A (Hermeneutic) and Axis B (Spiritual Ascent).
    """
    model_config = ConfigDict(validate_assignment=True)

    proposition: str = Field(..., min_length=10, description="Core proposition at this level")
    scope: Scope = Field(..., description="Scope of application")
    certainty: Certainty = Field(..., description="Epistemic certainty")
    conditionality: Conditionality = Field(..., description="Contextual conditionality")

    class Config:
        json_schema_extra = {
            "example": {
                "proposition": "Prayer is obligatory five times daily",
                "scope": "universal",
                "certainty": "qatʿī",
                "conditionality": "absolute"
            }
        }


class Layer3AxisA(BaseModel):
    """
    Layer 3 Axis A: Hermeneutic Dimensions
    Four levels: zahir (literal), ishara (indicative), akhlaq (moral), haqiqa (metaphysical)
    """
    model_config = ConfigDict(validate_assignment=True)

    zahir: Optional[InterpretiveLayer] = Field(None, description="Literal/apparent meaning")
    ishara: Optional[InterpretiveLayer] = Field(None, description="Indicative/allusive meaning")
    akhlaq: Optional[InterpretiveLayer] = Field(None, description="Moral/ethical dimension")
    haqiqa: Optional[InterpretiveLayer] = Field(None, description="Metaphysical/ultimate reality")

    class Config:
        json_schema_extra = {
            "example": {
                "zahir": {
                    "proposition": "Perform ritual prayer five times",
                    "scope": "universal",
                    "certainty": "qatʿī",
                    "conditionality": "absolute"
                },
                "akhlaq": {
                    "proposition": "Cultivate discipline and God-consciousness",
                    "scope": "universal",
                    "certainty": "ẓannī",
                    "conditionality": "contextual"
                }
            }
        }


class Layer3AxisB(BaseModel):
    """
    Layer 3 Axis B: Spiritual Ascent Dimensions
    Four levels: amal (outward), niyya (inward), hadd (limit), ma'rifa (ascent)
    """
    model_config = ConfigDict(validate_assignment=True)

    amal: Optional[InterpretiveLayer] = Field(None, description="Outward action")
    niyya: Optional[InterpretiveLayer] = Field(None, description="Inward intention")
    hadd: Optional[InterpretiveLayer] = Field(None, description="Limit/boundary")
    marifa: Optional[InterpretiveLayer] = Field(None, description="Ascent/gnosis")

    class Config:
        json_schema_extra = {
            "example": {
                "amal": {
                    "proposition": "Physical movements of prayer",
                    "scope": "universal",
                    "certainty": "qatʿī",
                    "conditionality": "absolute"
                },
                "niyya": {
                    "proposition": "Intention of worship and submission",
                    "scope": "individual",
                    "certainty": "ẓannī",
                    "conditionality": "contextual"
                }
            }
        }


class Layer4Vectors(BaseModel):
    """
    Layer 4: Thematic Vectors
    Thematic dimensions and value structures.
    """
    model_config = ConfigDict(validate_assignment=True)

    divine_attributes: List[str] = Field(
        default_factory=list,
        description="Divine attributes referenced (Al-Rahman, Al-Hakim, etc.)"
    )
    faculties_addressed: List[str] = Field(
        default_factory=list,
        description="Human faculties addressed (intellect, will, heart, etc.)"
    )
    maqam_hal: Optional[str] = Field(
        None,
        max_length=100,
        description="Spiritual station (maqam) or state (hal)"
    )
    legal_cause: Optional[str] = Field(
        None,
        max_length=255,
        description="Legal cause or rationale (illah)"
    )
    objective: Optional[str] = Field(
        None,
        max_length=255,
        description="Higher objective (maqsid)"
    )
    values: List[str] = Field(
        default_factory=list,
        description="Virtues and values promoted"
    )
    vices: List[str] = Field(
        default_factory=list,
        description="Vices and negative qualities warned against"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "divine_attributes": ["Al-Rahman", "Al-Rahim"],
                "faculties_addressed": ["intellect", "will"],
                "maqam_hal": "tawakkul",
                "legal_cause": "protection of life",
                "objective": "social cohesion",
                "values": ["justice", "mercy", "patience"],
                "vices": ["arrogance", "injustice"]
            }
        }


# ============================================================================
# Complete HMSTS Models
# ============================================================================

class HMSTSOutput(BaseModel):
    """
    Complete HMSTS 5-layer semantic analysis output from LLM.
    Used for LLM input/output and validation.
    """
    model_config = ConfigDict(validate_assignment=True)

    # Layer 0: Textual Fact
    layer0: Layer0 = Field(..., description="Textual fact layer")

    # Layer 1: Ontological Category
    layer1: Layer1 = Field(..., description="Ontological categories")

    # Layer 2: Functional Role
    layer2: Layer2 = Field(..., description="Functional role")

    # Layer 3: Four Meaning Axes
    layer3_axis_a: Optional[Layer3AxisA] = Field(None, description="Hermeneutic dimensions")
    layer3_axis_b: Optional[Layer3AxisB] = Field(None, description="Spiritual ascent dimensions")

    # Layer 4: Thematic Vectors
    layer4: Layer4Vectors = Field(..., description="Thematic vectors")

    class Config:
        json_schema_extra = {
            "example": {
                "layer0": {
                    "speaker": "Prophet Muhammad",
                    "modality": "obligatory"
                },
                "layer1": {
                    "categories": ["Worship", "Ethics"]
                },
                "layer2": {
                    "role": "Normative"
                },
                "layer4": {
                    "values": ["discipline", "humility"]
                }
            }
        }


class HMSTSAssignment(BaseModel):
    """
    Complete HMSTS assignment database record with metadata.

    Maps to: hmsts_tags table
    Note: layer3_axis_a, layer3_axis_b, layer4_vectors are stored as JSONB
    """
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    id: Optional[int] = None
    hadith_id: int = Field(..., description="References raw_hadiths.id")
    version: str = Field("v1.0", max_length=20, description="Processing version")

    # Layer 0 (as flat columns in DB)
    layer0_speaker: Optional[str] = Field(None, max_length=255)
    layer0_addressee: Optional[str] = Field(None, max_length=255)
    layer0_verb_type: Optional[str] = Field(None, max_length=100)
    layer0_modality: Optional[Modality] = None

    # Layer 1 (as array in DB)
    layer1_categories: List[str] = Field(..., min_length=1)

    # Layer 2 (as column in DB)
    layer2_role: FunctionalRole = Field(..., description="Functional role")

    # Layer 3 (as JSONB in DB)
    layer3_axis_a: Optional[Dict[str, Any]] = Field(None, description="JSONB: Hermeneutic dimensions")
    layer3_axis_b: Optional[Dict[str, Any]] = Field(None, description="JSONB: Spiritual ascent")

    # Layer 4 (as JSONB in DB)
    layer4_vectors: Optional[Dict[str, Any]] = Field(None, description="JSONB: Thematic vectors")

    # LLM metadata
    llm_model: Optional[str] = Field(None, max_length=100)
    llm_cost_usd: Optional[Decimal] = Field(None, ge=0, decimal_places=6)
    processing_duration_ms: Optional[int] = Field(None, ge=0)
    semantic_completeness_score: Optional[Decimal] = Field(None, ge=0, le=1, decimal_places=3)

    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_hmsts_output(cls, hadith_id: int, output: HMSTSOutput, version: str = "v1.0") -> "HMSTSAssignment":
        """
        Convert HMSTSOutput to HMSTSAssignment for database storage.
        Flattens Layer 0-2 and converts Layer 3-4 to JSONB dicts.
        """
        return cls(
            hadith_id=hadith_id,
            version=version,
            # Layer 0
            layer0_speaker=output.layer0.speaker,
            layer0_addressee=output.layer0.addressee,
            layer0_verb_type=output.layer0.verb_type,
            layer0_modality=output.layer0.modality,
            # Layer 1
            layer1_categories=output.layer1.categories,
            # Layer 2
            layer2_role=output.layer2.role,
            # Layer 3 (convert to dict for JSONB)
            layer3_axis_a=output.layer3_axis_a.model_dump() if output.layer3_axis_a else None,
            layer3_axis_b=output.layer3_axis_b.model_dump() if output.layer3_axis_b else None,
            # Layer 4 (convert to dict for JSONB)
            layer4_vectors=output.layer4.model_dump()
        )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "hadith_id": 1,
                "version": "v1.0",
                "layer0_modality": "obligatory",
                "layer1_categories": ["Worship", "Ethics"],
                "layer2_role": "Normative",
                "layer3_axis_a": {"zahir": {"proposition": "...", "scope": "universal"}},
                "layer4_vectors": {"values": ["justice", "mercy"]},
                "llm_model": "claude-3-5-sonnet-20241022",
                "llm_cost_usd": 0.10,
                "semantic_completeness_score": 0.92
            }
        }


class HMSTSBatch(BaseModel):
    """
    Batch of HMSTS assignments for parallel processing.
    """
    model_config = ConfigDict(validate_assignment=True)

    assignments: List[HMSTSAssignment] = Field(..., min_length=1, max_length=1000)
    batch_id: str = Field(..., description="Unique batch identifier")
    version: str = Field("v1.0", description="Processing version")
    total_cost_usd: Optional[Decimal] = Field(None, ge=0)
    total_duration_ms: Optional[int] = Field(None, ge=0)
    avg_completeness_score: Optional[Decimal] = Field(None, ge=0, le=1)

    class Config:
        json_schema_extra = {
            "example": {
                "assignments": [],
                "batch_id": "batch_001_v1.0_hmsts",
                "version": "v1.0",
                "total_cost_usd": 5.0,
                "total_duration_ms": 150000,
                "avg_completeness_score": 0.89
            }
        }
