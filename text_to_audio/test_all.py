import unittest


def main():
    # Discover and run all tests in the current directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir=".", pattern="test_*.py")
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(test_suite)

    # To be able to exit with a non-zero exit code if tests fail
    if result.failures or result.errors:
        exit(1)


if __name__ == "__main__":
    main()
