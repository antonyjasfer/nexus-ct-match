import json
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from agents.patient_profiler import profile_patient
from agents.match_scorer import score_match
from config import PARSED_TRIALS_PATH

class NexusState(TypedDict):
    patient_record: dict
    trial_ids: List[str]
    patient_profile: dict
    match_results: List[dict]
    status: str

def load_trials():
    with open(PARSED_TRIALS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def profile_node(state: NexusState):
    profile = profile_patient(state["patient_record"])
    return {"patient_profile": profile.model_dump(), "status": "profiled"}

def score_node(state: NexusState):
    trial_db = load_trials()
    results = []
    for tid in state["trial_ids"]:
        if tid not in trial_db:
            continue
        result = score_match(state["patient_profile"], trial_db[tid])
        results.append(result.model_dump())
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return {"match_results": results, "status": "complete"}

workflow = StateGraph(NexusState)
workflow.add_node("profile", profile_node)
workflow.add_node("score", score_node)
workflow.set_entry_point("profile")
workflow.add_edge("profile", "score")
workflow.add_edge("score", END)

nexus_app = workflow.compile()

def run_nexus(patient_record: dict, trial_ids: list = None):
    trial_db = load_trials()
    if trial_ids is None:
        trial_ids = list(trial_db.keys())
    return nexus_app.invoke({
        "patient_record": patient_record,
        "trial_ids": trial_ids,
        "patient_profile": {},
        "match_results": [],
        "status": "started"
    })