import sys
from pathlib import Path
import pytest


def main() -> None:
    test_dir = Path(__file__).resolve().parent / "src" / "tests"
    sys.exit(pytest.main([str(test_dir)]))


if __name__ == "__main__":
    main()
