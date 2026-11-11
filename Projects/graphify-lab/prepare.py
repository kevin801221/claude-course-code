"""Copy the five-file lab into a new scratch directory. No agent or network needed."""
import argparse
from pathlib import Path
from shutil import copyfile

HERE = Path(__file__).resolve().parent
FILES = ("app.py", "service.py", "validation.py", "repository.py", "notification.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--solution", action="store_true", help="Use the optional-email implementation")
    args = parser.parse_args()
    dest = args.destination.resolve()
    if dest.exists():
        parser.error(f"Directory already exists: {dest}. Choose a NEW directory; nothing was changed.")
    dest.mkdir(parents=True)
    for name in FILES:
        replacement = HERE / "reference" / name
        src = replacement if args.solution and replacement.is_file() else HERE / "starter" / name
        copyfile(src, dest / name)
    print(f"Prepared {'solution' if args.solution else 'starter'} at {dest}")
