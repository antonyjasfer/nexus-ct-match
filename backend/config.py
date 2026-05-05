from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
TRIALS_DIR = DATA_DIR / "trials"
PATIENTS_DIR = DATA_DIR / "patients"
PARSED_TRIALS_PATH = DATA_DIR / "parsed_trials.json"

VLLM_BASE_URL = "http://localhost:8000/v1"
VLLM_API_KEY = "not-needed"
MODEL_NAME = "meta-llama/Llama-3.1-70B-Instruct"
TEMPERATURE = 0.0
MAX_TOKENS = 4000

PARSER_SYSTEM_PROMPT = """You are a clinical trial eligibility parser. Extract ALL criteria into structured JSON.

Rules:
- Extract EVERY inclusion and exclusion criterion verbatim
- Identify temporal constraints (washout periods, time windows)
- Use standardized field names (age, ecog_score, pdl1_expression, etc.)
- Preserve nested logic (AND/OR) in the criterion text
- If a criterion has multiple conditions, split them

Output MUST match the ParsedTrial schema."""