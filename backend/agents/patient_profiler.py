from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import PatientProfile
from config import VLLM_BASE_URL, VLLM_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
import json

_llm = ChatOpenAI(
    base_url=VLLM_BASE_URL,
    api_key=VLLM_API_KEY,
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS
)

structured_llm = _llm.with_structured_output(PatientProfile, method="json_mode")

PROFILER_PROMPT = """You are a medical record analyzer. Create a standardized clinical profile.

Rules:
- Calculate days_since_today for past treatments (today = 2026-05-04)
- Normalize lab values to standard units
- Determine organ_function: adequate/impaired based on creatinine, bilirubin, etc.
- Flag concerns for trial eligibility
- Output MUST match PatientProfile schema."""

prompt = ChatPromptTemplate.from_messages([
    ("system", PROFILER_PROMPT),
    ("human", "Analyze this patient record:\n\n{patient_record}")
])

chain = prompt | structured_llm

def profile_patient(patient_record: dict) -> PatientProfile:
    return chain.invoke({"patient_record": json.dumps(patient_record, indent=2)})