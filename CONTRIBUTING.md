# Contributing benchmark evidence

Contributions are welcome for runners, workload packs, provider adapters, evaluators and measured datasets.

Measured results must include reproducible configuration, collection timestamp, region, runtime version, model revision, hardware, concurrency, context distribution, pricing source and raw evidence location. Synthetic or illustrative results must be labelled as such.

Never submit customer prompts, credentials, personal data or proprietary workload content. Use synthetic or explicitly authorized workload packs.

Before opening a pull request:

```bash
python -m compileall -q src
pytest -q
```

