"""Command-line entry points for CSV surveys and an offline synthetic demo."""

import argparse
from pathlib import Path

from .demo import demo_samples
from .report import make_report
from .survey import read_csv, write_csv


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="generate a clearly synthetic 50 m survey")
    demo.add_argument("--output", type=Path, default=Path("outputs/demo"))
    report = sub.add_parser("report", help="map a schema-v1 survey CSV")
    report.add_argument("csv", type=Path)
    report.add_argument("--output", type=Path, default=Path("outputs/survey"))
    report.add_argument("--radius-m", type=float, default=8)
    args = parser.parse_args()
    try:
        if args.command == "demo":
            samples = demo_samples()
            args.output.mkdir(parents=True, exist_ok=True)
            write_csv(samples, args.output / "survey.csv")
            make_report(samples, args.output)
        else:
            make_report(read_csv(args.csv), args.output, radius_m=args.radius_m)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"Report saved to {args.output.resolve()}")
