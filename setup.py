import subprocess
import sys
from pathlib import Path


def run(cmd):
    subprocess.check_call(cmd)


def main():
    root = Path(__file__).resolve().parent
    requirements = root / "requirements.txt"
    main_file = root / "main.py"

    run([sys.executable, "-m", "pip", "install", "-r", str(requirements)])
    run([sys.executable, str(main_file)])


if __name__ == "__main__":
    main()
