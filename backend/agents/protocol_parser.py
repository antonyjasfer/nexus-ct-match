from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.schemas import ParsedTrial
from utils.json_helper import safe_parse_json
from config import VLLM_BASE_URL, VLLM_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS, PARSER_SYSTEM_PROMPT
import json

_llm = ChatOpenAI(
    base_url=VLLM_BASE_URL,
    api_key=VLLM_API_KEY,
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    max_tokens=MAX_TOKENS
)

structured_llm = _llm.with_structured_output(ParsedTrial, method="json_mode")

prompt = ChatPromptTemplate.from_messages([
    ("system", PARSER_SYSTEM_PROMPT),
    ("human", "Parse this clinical trial protocol:\n\n{protocol_text}")
])

chain = prompt | structured_llm

def parse_protocol(protocol_text: str) -> ParsedTrial:
    try:
        return chain.invoke({"protocol_text": protocol_text})
    except Exception as e:
        raw = _llm.invoke(f"{PARSER_SYSTEM_PROMPT}\n\n{protocol_text}")
        data = safe_parse_json(raw.content)
        return ParsedTrial(**data)