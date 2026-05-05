import json, os
from agents.protocol_parser import parse_protocol
from config import TRIALS_DIR, PARSED_TRIALS_PATH

def main():
    parsed = {}
    for fname in sorted(os.listdir(TRIALS_DIR)):
        if not fname.endswith(".txt"):
            continue
        fpath = os.path.join(TRIALS_DIR, fname)
        print(f"Parsing {fname}...")
        with open(fpath, "r", encoding="utf-8") as f:
            text = f.read()
        try:
            result = parse_protocol(text)
            parsed[result.trial_id] = result.model_dump()
            inc = len(result.inclusion_criteria)
            exc = len(result.exclusion_criteria)
            print(f"  ✓ {result.trial_id}: {inc} inclusion, {exc} exclusion")
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
    
    with open(PARSED_TRIALS_PATH, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)
    print(f"\n✅ Saved {len(parsed)} trials to {PARSED_TRIALS_PATH}")

if __name__ == "__main__":
    main()