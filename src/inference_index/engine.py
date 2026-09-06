from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Workload:
    requests_per_month: int
    input_tokens: int
    output_tokens: int
    required_quality: float
    p95_latency_ms: int
    availability: float
    region: str | None = None
    data_residency: str | None = None


@dataclass(frozen=True)
class Candidate:
    provider: str
    model: str
    runtime: str
    hardware: str
    region: str
    input_usd_per_million: float
    output_usd_per_million: float
    fixed_monthly_usd: float
    p95_latency_ms: int
    quality_score: float
    success_rate: float
    availability: float
    throughput_tokens_second: float
    evidence: str


def _load(path: str | Path) -> list[Candidate]:
    records = json.loads(Path(path).read_text())
    return [Candidate(**record) for record in records]


def score_candidate(workload: Workload, candidate: Candidate) -> dict[str, Any]:
    token_cost = workload.requests_per_month * (
        workload.input_tokens * candidate.input_usd_per_million / 1_000_000
        + workload.output_tokens * candidate.output_usd_per_million / 1_000_000
    )
    monthly_cost = token_cost + candidate.fixed_monthly_usd
    successful_requests = workload.requests_per_month * candidate.success_rate
    cost_per_success = monthly_cost / successful_requests if successful_requests else float("inf")

    eligible = (
        candidate.quality_score >= workload.required_quality
        and candidate.p95_latency_ms <= workload.p95_latency_ms
        and candidate.availability >= workload.availability
        and (not workload.region or candidate.region == workload.region)
    )
    quality_margin = candidate.quality_score - workload.required_quality
    latency_margin = workload.p95_latency_ms - candidate.p95_latency_ms
    utility = (
        (candidate.quality_score * candidate.success_rate * 100)
        / max(cost_per_success, 0.000001)
    )
    provenance = hashlib.sha256(
        json.dumps(asdict(candidate), sort_keys=True).encode()
    ).hexdigest()

    return {
        **asdict(candidate),
        "eligible": eligible,
        "monthly_cost_usd": round(monthly_cost, 2),
        "successful_requests": round(successful_requests),
        "cost_per_successful_request_usd": round(cost_per_success, 6),
        "quality_margin": round(quality_margin, 3),
        "latency_margin_ms": latency_margin,
        "utility_score": round(utility, 3),
        "provenance_sha256": provenance,
    }


def rank_candidates(workload_data: dict[str, Any], dataset_path: str | Path) -> dict[str, Any]:
    workload = Workload(**workload_data)
    results = [score_candidate(workload, candidate) for candidate in _load(dataset_path)]
    results.sort(key=lambda item: (not item["eligible"], -item["utility_score"]))
    eligible = [item for item in results if item["eligible"]]
    return {
        "schema_version": "0.1.0",
        "workload": asdict(workload),
        "recommendation": eligible[0] if eligible else None,
        "candidates": results,
        "warning": "Illustrative dataset: validate current pricing and benchmark on the target workload before procurement.",
    }

