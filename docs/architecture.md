# Production Architecture

## Control plane

The control plane owns benchmark definitions, policy constraints, signed result manifests, price snapshots and recommendation history. It never receives provider credentials from community result submissions.

## Execution plane

Ephemeral runners execute a pinned workload pack against an approved target. Production runners should use workload identity, private networking, secret injection, egress policy, immutable images and per-run namespaces.

## Evidence plane

Every run produces:

- Workload and evaluator versions
- Git commit and container digest
- Model, runtime, hardware and region metadata
- Raw latency/throughput/utilization observations
- Quality and successful-outcome results
- Price snapshot timestamp and source
- Attestation and content hash

Raw evidence is immutable. Derived scores can be recalculated when the index methodology evolves.

## Data platform

Recommended production stack:

- Object storage for immutable raw results
- Parquet and Apache Iceberg for versioned analytical data
- DuckDB for local analysis and a warehouse engine for hosted analytics
- OpenTelemetry for traces, metrics and cost attribution
- Prometheus plus NVIDIA DCGM Exporter for GPU telemetry
- Grafana and Power BI for engineering and executive views

## Security and compliance

- OIDC workload identity; no persistent cloud keys
- Signed images, SBOMs and provenance attestations
- Network policies and provider allowlists
- Dataset schema validation and quarantine for untrusted submissions
- Separation of benchmark facts from generated recommendations
- Complete audit log of recommendation, approval, deployment and rollback
- Policy-as-code gates for residency, availability, cost and model eligibility

## Failure handling

Recommendations are advisory until a controlled replay and canary satisfy the workload's SLO. Promotion requires a rollback target and an explicit approval policy. A failed evaluator, missing price snapshot or incomplete provenance makes the candidate ineligible rather than silently reducing confidence.

