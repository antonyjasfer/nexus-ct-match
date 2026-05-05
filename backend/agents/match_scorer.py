from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import MatchScore
from config import VLLM_BASE_URL, VLLM_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
import json

_llm = ChatOpenAI(
    base_url=VLLM_BASE_URL,
    api_key=VLLM_API_KEY,
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS
)

structured_llm = _llm.with_structured_output(MatchScore, method="json_mode")

SCORER_PROMPT = """You are a clinical trial matching expert.

Rules:
1. Check EVERY inclusion criterion. If ANY hard inclusion fails → eligible = false.
2. Check EVERY exclusion criterion. If ANY hard exclusion matches → match_score = 0, eligible = false.
3. Score 100 = perfect match. Subtract proportionally for partial matches.
4. Provide reasoning for EACH criterion.
5. Flag criteria needing human review.

Output MUST match MatchScore schema."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SCORER_PROMPT),
    ("human", "Patient Profile:\n{patient_profile}\n\nTrial Criteria:\n{trial_criteria}\n\nEvaluate and return structured JSON.")
])

chain = prompt | structured_llm

def score_match(patient_profile: dict, trial_criteria: dict) -> MatchScore:
    return chain.invoke({
        "patient_profile": json.dumps(patient_profile, indent=2),
        "trial_criteria": json.dumps(trial_criteria, indent=2)
    })