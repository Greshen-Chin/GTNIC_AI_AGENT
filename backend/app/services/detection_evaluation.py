"""Measured, reproducible lab results. Never substitutes for production accuracy."""
import hashlib
import json
import time
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from app.services.request_detector import detect_request, DETECTOR_VERSION

CASE_PATH = Path(__file__).resolve().parents[2] / "evaluation" / "request_cases.v1.json"


@lru_cache(maxsize=1)
def evaluate_detector():
    source = CASE_PATH.read_bytes()
    dataset = json.loads(source)
    rows = []
    tp = tn = fp = fn = correct = 0
    for case in dataset["cases"]:
        start = time.perf_counter()
        detection = detect_request(case["event"])
        elapsed = (time.perf_counter() - start) * 1000
        predicted = detection["threat_type"] if detection else None
        expected = case["expected"]
        correct += predicted == expected
        tp += expected is not None and predicted is not None
        tn += expected is None and predicted is None
        fp += expected is None and predicted is not None
        fn += expected is not None and predicted is None
        rows.append({"name": case["name"], "expected": expected, "predicted": predicted,
                     "correct": predicted == expected, "elapsed_ms": round(elapsed, 4)})
    count = len(rows)
    return {
        "dataset_version": dataset["version"], "dataset_sha256": hashlib.sha256(source).hexdigest(),
        "detector_version": DETECTOR_VERSION,
        "scope": dataset["scope"], "source": "labelled-lab-fixtures", "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "total_scenarios": count, "correct": correct,
        "accuracy": round(correct / count * 100, 2) if count else None,
        "binary_accuracy": round((tp + tn) / count * 100, 2) if count else None,
        "precision": round(tp / (tp + fp) * 100, 2) if tp + fp else None,
        "recall": round(tp / (tp + fn) * 100, 2) if tp + fn else None,
        "false_positive_rate": round(fp / (fp + tn) * 100, 2) if fp + tn else None,
        "false_negative_rate": round(fn / (fn + tp) * 100, 2) if fn + tp else None,
        "confusion_matrix": {"tp": tp, "tn": tn, "fp": fp, "fn": fn}, "runs": rows,
        "limitations": ["Hand-labelled synthetic lab cases; not production ground truth.",
                        "Does not measure Gemini narrative accuracy, exploitation success or unseen attacks."],
    }
