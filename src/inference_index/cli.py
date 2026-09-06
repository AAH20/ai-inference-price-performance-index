from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import rank_candidates


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="inference-index",
        description="Rank LLM inference options by cost per successful outcome.",
    )
    parser.add_argument("compare", nargs="?", default="compare")
    parser.add_argument("--workload", required=True, help="Workload JSON file")
    parser.add_argument("--dataset", required=True, help="Candidate benchmark JSON file")
    parser.add_argument("--output", help="Write complete result to a JSON file")
    args = parser.parse_args()

    result = rank_candidates(
        json.loads(Path(args.workload).read_text()),
        args.dataset,
    )
    rendered = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n")
    print(rendered)


if __name__ == "__main__":
    main()

