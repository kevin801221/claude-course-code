"""Hello World 範例：示範 main() 入口、可選 name 參數與 CLI 參數解析。"""

import argparse


def greet(name: str = "World") -> str:
    """回傳問候字串，name 預設為 World。"""
    return f"Hello, {name}!"


def main() -> None:
    parser = argparse.ArgumentParser(description="印出 Hello, <name>!")
    parser.add_argument(
        "--name",
        default="World",
        help="要問候的對象名稱（預設：World）",
    )
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
