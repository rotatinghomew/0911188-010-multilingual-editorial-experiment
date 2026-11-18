import argparse
import json
from pathlib import Path
from .service import report
from .workbench import run_workbench

def main():
    parser = argparse.ArgumentParser(description='查看本地业务数据总览')
    parser.add_argument('action', choices=['summary', 'enrollment', 'metrics', 'decision', 'broadcast'])
    parser.add_argument('--data', default=str(Path(__file__).parents[1] / 'data'))
    parser.add_argument('--key', help='业务编号')
    parser.add_argument('--ledger', default='workbench.sqlite3', help='本地凭证库')
    args = parser.parse_args()
    try:
        value = report(args.data) if args.action == 'summary' else run_workbench(
            args.action, Path(args.data), args.key, args.ledger,
        )
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f'无法处理：{error}\n')
    print(json.dumps(value, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
