import json
import time
from pathlib import Path

from workstation import ModelRouter, Node


CASES = [
    *[{"id": f"route-{i}", "kind": "route"} for i in range(1, 4)],
    *[{"id": f"failover-{i}", "kind": "failover"} for i in range(1, 4)],
    *[{"id": f"capacity-{i}", "kind": "capacity"} for i in range(1, 3)],
    *[{"id": f"recovery-{i}", "kind": "recovery"} for i in range(1, 3)],
]


def evaluate(case):
    router = ModelRouter([Node("a", "http://192.0.2.10:8080", 8), Node("b", "http://192.0.2.20:8080", 4)])
    if case["kind"] == "route":
        return router.route(6).name == "a"
    if case["kind"] == "failover":
        router.mark_unhealthy("a")
        return router.route(2).name == "b"
    if case["kind"] == "capacity":
        return router.route(20) is None
    router.mark_unhealthy("a")
    router.recover("a")
    return router.route(6).name == "a"


started = time.perf_counter()
results = [{"case_id": case["id"], "trial": trial, "passed": evaluate(case)} for case in CASES for trial in range(1, 4)]
passed = sum(item["passed"] for item in results)
report = {
    "mode": "deterministic-offline",
    "cases": len(CASES),
    "trials": len(results),
    "passed": passed,
    "success_rate": passed / len(results),
    "p50_latency_ms": round((time.perf_counter() - started) * 1000 / len(results), 3),
    "estimated_cost_usd": 0,
    "results": results,
}
Path(__file__).with_name("results.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({key: value for key, value in report.items() if key != "results"}, indent=2))
raise SystemExit(0 if passed == len(results) else 1)

