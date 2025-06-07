import unittest
import sys


def main() -> None:
    loader = unittest.TestLoader()
    tests = loader.discover(".")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()
