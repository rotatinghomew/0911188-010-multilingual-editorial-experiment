import argparse
import json
from pathlib import Path
from .service import report

def main():
    parser = argparse.ArgumentParser(description='查看本地业务数据总览')
    parser.add_argument('action', choices=['summary'])
    parser.add_argument('--data', default=str(Path(__file__).parents[1] / 'data'))
    args = parser.parse_args()
    print(json.dumps(report(args.data), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
