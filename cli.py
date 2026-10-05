"""命令行：python3 cli.py data.csv"""
import argparse
import sys

from profiler import profile_csv, report


def main(argv=None):
    p = argparse.ArgumentParser(description="data-profiler-lite 数据画像")
    p.add_argument("file", nargs="?", help="CSV 文件")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    if not args.file:
        print("错误：请提供 CSV 文件", file=sys.stderr)
        return 2
    with open(args.file, encoding="utf-8") as f:
        text = f.read()
    if args.json:
        import json
        print(json.dumps(profile_csv(text), ensure_ascii=False, indent=2))
    else:
        print(report(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
