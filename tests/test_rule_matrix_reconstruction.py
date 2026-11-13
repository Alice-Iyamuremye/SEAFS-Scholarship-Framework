import json
from pathlib import Path


def test_reconstruction_covers_all_27_combinations():
    path = Path(__file__).parents[1] / "research" / "seafs_27_combination_reconstruction.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rules = data["rules"]
    assert len(rules) == 27
    combos = {(r["gpa"], r["financial_need"], r["recommendations"]) for r in rules}
    terms = {"Low", "Medium", "High"}
    assert len(combos) == 27
    assert all(a in terms and b in terms and c in terms for a,b,c in combos)
    inferred = {r["gpa"]+"/"+r["financial_need"]+"/"+r["recommendations"]:r["consequent"] for r in rules if r["provenance"] == "reconstructed"}
    assert inferred == {"Low/Low/Medium":"Reject", "Low/Medium/Medium":"Waitlist"}
