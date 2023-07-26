# cli.py

import subprocess
import os

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    subprocess.run(["streamlit", "run", os.path.join(current_dir, "app.py")])

if __name__ == "__main__":
    main()
