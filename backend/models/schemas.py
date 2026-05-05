from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Criterion(BaseModel):
    criterion: str = Field(description="Original text of the criterion")
    category: Literal["demographics", "clinical", "laboratory", "treatment_history", "other"]
    field: str = Field(description="Standardized field name, e.g., 'age', 'ecog_score'")
    operator: Literal[">=", "<=", "==", "in", "not_in", "boolean", "exists"]
    value: Optional[str] = Field(description="Extracted value or null")

class TemporalConstraint(BaseModel):
    criterion: str
    field: str
    washout_days: Optional[int] = None

class ParsedTrial(BaseModel):
    trial_id: str
    title: str
    phase: Optional[str] = None
    conditions: List[str]
    inclusion_criteria: List[Criterion]
    exclusion_criteria: List[Criterion]
    temporal_constraints: List[TemporalConstraint]

class MatchableFields(BaseModel):
    age: int
    sex: Literal["Male", "Female"]
    ecog_score: int
    primary_diagnosis: str
    cancer_stage: Optional[str] = None
    biomarkers: dict
    lab_values: dict
    active_medications: List[str]
    prior_treatments: List[dict]
    comorbidities: List[str]
    organ_function: Literal["adequate", "impaired"]

class PatientProfile(BaseModel):
    patient_id: str
    matchable_fields: MatchableFields
    flags: List[str]
    summary: str

class CriterionResult(BaseModel):
    criterion: str
    met: bool
    confidence: Literal["high", "medium", "low"]
    reasoning: str

class MatchScore(BaseModel):
    trial_id: str
    patient_id: str
    match_score: int = Field(ge=0, le=100)
    eligible: bool
    criteria_results: List[CriterionResult]
    disqualifying_factors: List[str]
    risks_to_review: List[str]
    recommendation: Literal["STRONG_MATCH", "POSSIBLE_MATCH", "UNLIKELY", "DISQUALIFIED"]
    summary: str