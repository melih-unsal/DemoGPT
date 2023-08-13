#!/usr/bin/env python

import os
import subprocess
import sys

from demogpt.prompt_based.cli import \
    main as plan_main  # Make sure to import the plan.cli module appropriately


def main():
    if "--basic" in sys.argv:
        sys.argv.remove("--basic")
        plan_main()
        return

    current_dir = os.path.dirname(os.path.realpath(__file__))
    subprocess.run(["streamlit", "run", os.path.join(current_dir, "app.py")])


if __name__ == "__main__":
    main()
