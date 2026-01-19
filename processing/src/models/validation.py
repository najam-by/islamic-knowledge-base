"""
Validation and Quality Scoring Models
=====================================

Pydantic models for validation results and quality metrics.

Models:
- ValidationStatus: Pass/warning/fail enum
- ValidationCategory: Temporal/semantic/consistency/overall
- ValidationIssue: Individual validation issue
- ValidationResult: Complete validation record
- QualityMetrics: Aggregated quality scores
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class ValidationStatus(str, Enum):
    """Validation outcome status."""
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


class ValidationCategory(str, Enum):
    """Category of validation check."""
    TEMPORAL = "temporal"
    SEMANTIC = "semantic"
    CONSISTENCY = "consistency"
    OVERALL = "overall"


class ValidationIssue(BaseModel):
    """
    Individual validation issue.
    Stored as part of JSONB 'issues' field.
    """
    model_config = ConfigDict(validate_assignment=True)

    issue_type: str = Field(..., max_length=100, description="Type of issue")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    description: str = Field(..., min_length=10, description="Issue description")
    field: Optional[str] = Field(None, description="Field that failed validation")
    expected: Optional[str] = Field(None, description="Expected value/range")
    actual: Optional[str] = Field(None, description="Actual value")
    suggestion: Optional[str] = Field(None, description="Suggested fix")

    class Config:
        json_schema_extra = {
            "example": {
                "issue_type": "anchor_conflict",
                "severity": "high",
                "description": "Temporal anchor creates circular dependency",
                "field": "anchor_before",
                "expected": "No cycles in anchor relationships",
                "actual": "Cycle detected: E2 -> E2.1 -> E2",
                "suggestion": "Remove anchor_before reference to E2"
            }
        }


class ValidationResult(BaseModel):
    """
    Complete validation result database record.

    Maps to: validation_results table
    """
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    id: Optional[int] = None
    hadith_id: int = Field(..., description="References raw_hadiths.id")
    version: str = Field("v1.0", max_length=20, description="Processing version")

    # Validation metadata
    validation_type: str = Field(..., max_length=100, description="Type of validation performed")
    validation_category: ValidationCategory = Field(..., description="Category of validation")
    status: ValidationStatus = Field(..., description="Overall status")

    # Issues (stored as JSONB)
    issues: Optional[Dict[str, Any]] = Field(
        None,
        description="JSONB: List of validation issues"
    )

    # Quality scores
    quality_score: Optional[Decimal] = Field(None, ge=0, le=1, decimal_places=3)
    temporal_confidence: Optional[Decimal] = Field(None, ge=0, le=1, decimal_places=3)
    semantic_completeness: Optional[Decimal] = Field(None, ge=0, le=1, decimal_places=3)
    validation_pass_rate: Optional[Decimal] = Field(None, ge=0, le=1, decimal_places=3)

    # Metadata
    validated_at: Optional[datetime] = None
    validator_version: Optional[str] = Field(None, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "hadith_id": 1,
                "version": "v1.0",
                "validation_type": "pcap_temporal_consistency",
                "validation_category": "temporal",
                "status": "pass",
                "issues": None,
                "quality_score": 0.92,
                "temporal_confidence": 0.85,
                "validation_pass_rate": 1.0,
                "validator_version": "1.0"
            }
        }


class QualityMetrics(BaseModel):
    """
    Aggregated quality metrics for a hadith across all validations.
    """
    model_config = ConfigDict(validate_assignment=True)

    hadith_id: int
    version: str = Field("v1.0")

    # Component scores
    temporal_confidence: Decimal = Field(..., ge=0, le=1, decimal_places=3)
    evidence_strength: Decimal = Field(..., ge=0, le=1, decimal_places=3)
    validation_pass_rate: Decimal = Field(..., ge=0, le=1, decimal_places=3)
    semantic_completeness: Decimal = Field(..., ge=0, le=1, decimal_places=3)

    # Overall score (weighted average)
    overall_score: Decimal = Field(..., ge=0, le=1, decimal_places=3)

    # Issue counts
    critical_issues: int = Field(0, ge=0)
    high_issues: int = Field(0, ge=0)
    medium_issues: int = Field(0, ge=0)
    low_issues: int = Field(0, ge=0)

    # Validation results
    total_validations: int = Field(..., ge=0)
    passed_validations: int = Field(..., ge=0)
    warning_validations: int = Field(..., ge=0)
    failed_validations: int = Field(..., ge=0)

    def calculate_overall_score(self) -> Decimal:
        """
        Calculate overall quality score using weighted formula.
        Formula from PHASE_2_PLAN.md Section 7.2:
        overall = 0.35*temporal + 0.25*evidence + 0.25*validation + 0.15*semantic
        """
        score = (
            Decimal("0.35") * self.temporal_confidence +
            Decimal("0.25") * self.evidence_strength +
            Decimal("0.25") * self.validation_pass_rate +
            Decimal("0.15") * self.semantic_completeness
        )
        return round(score, 3)

    @classmethod
    def from_validation_results(
        cls,
        hadith_id: int,
        version: str,
        results: List[ValidationResult],
        temporal_confidence: Decimal,
        evidence_strength: Decimal,
        semantic_completeness: Decimal
    ) -> "QualityMetrics":
        """
        Create QualityMetrics from a list of validation results.
        """
        total = len(results)
        passed = sum(1 for r in results if r.status == ValidationStatus.PASS)
        warning = sum(1 for r in results if r.status == ValidationStatus.WARNING)
        failed = sum(1 for r in results if r.status == ValidationStatus.FAIL)

        # Count issues by severity
        critical = high = medium = low = 0
        for result in results:
            if result.issues and isinstance(result.issues, dict):
                for issue in result.issues.get("issues", []):
                    severity = issue.get("severity", "low")
                    if severity == "critical":
                        critical += 1
                    elif severity == "high":
                        high += 1
                    elif severity == "medium":
                        medium += 1
                    else:
                        low += 1

        pass_rate = Decimal(passed) / Decimal(total) if total > 0 else Decimal(0)

        metrics = cls(
            hadith_id=hadith_id,
            version=version,
            temporal_confidence=temporal_confidence,
            evidence_strength=evidence_strength,
            validation_pass_rate=pass_rate,
            semantic_completeness=semantic_completeness,
            overall_score=Decimal(0),  # Will be calculated
            critical_issues=critical,
            high_issues=high,
            medium_issues=medium,
            low_issues=low,
            total_validations=total,
            passed_validations=passed,
            warning_validations=warning,
            failed_validations=failed
        )

        # Calculate overall score
        metrics.overall_score = metrics.calculate_overall_score()
        return metrics

    class Config:
        json_schema_extra = {
            "example": {
                "hadith_id": 1,
                "version": "v1.0",
                "temporal_confidence": 0.85,
                "evidence_strength": 0.90,
                "validation_pass_rate": 0.95,
                "semantic_completeness": 0.88,
                "overall_score": 0.89,
                "critical_issues": 0,
                "high_issues": 0,
                "medium_issues": 2,
                "low_issues": 5,
                "total_validations": 20,
                "passed_validations": 19,
                "warning_validations": 1,
                "failed_validations": 0
            }
        }


class ValidationBatch(BaseModel):
    """
    Batch of validation results for reporting.
    """
    model_config = ConfigDict(validate_assignment=True)

    batch_id: str
    version: str = Field("v1.0")
    results: List[ValidationResult] = Field(..., min_length=1)

    # Summary statistics
    total_hadiths: int = Field(..., ge=0)
    passed_hadiths: int = Field(..., ge=0)
    warning_hadiths: int = Field(..., ge=0)
    failed_hadiths: int = Field(..., ge=0)
    avg_quality_score: Optional[Decimal] = Field(None, ge=0, le=1)

    validated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "batch_id": "validation_batch_001",
                "version": "v1.0",
                "results": [],
                "total_hadiths": 1000,
                "passed_hadiths": 950,
                "warning_hadiths": 40,
                "failed_hadiths": 10,
                "avg_quality_score": 0.87
            }
        }
