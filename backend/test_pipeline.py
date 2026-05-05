import json, os
from config import PATIENTS_DIR, PARSED_TRIALS_PATH
from orchestrator import run_nexus

def main():
    # Load hero patient
    hero_path = os.path.join(PATIENTS_DIR, "patient_001_hero_nsclc.json")
    with open(hero_path, "r", encoding="utf-8") as f:
        patient_data = json.load(f)
    
    print("🚀 NEXUS Pipeline Test")
    print("=" * 50)
    
    result = run_nexus(patient_data)
    
    print(f"\n👤 Patient: {result['patient_profile']['matchable_fields']['primary_diagnosis']}")
    print(f"   Stage: {result['patient_profile']['matchable_fields']['cancer_stage']}")
    print(f"   ECOG: {result['patient_profile']['matchable_fields']['ecog_score']}")
    
    print(f"\n📊 Found {len(result['match_results'])} matches:")
    for m in result['match_results'][:3]:
        print(f"   • {m['trial_id']}: {m['match_score']}/100 | {m['recommendation']}")
    
    if result['match_results']:
        top = result['match_results'][0]
        print(f"\n🏆 TOP MATCH:")
        print(f"   Score: {top['match_score']}/100")
        print(f"   Eligible: {top['eligible']}")
        print(f"   Summary: {top['summary'][:200]}...")

if __name__ == "__main__":
    main()