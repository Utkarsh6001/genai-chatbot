# genai-chatbot: helpful run script
# This script starts the backend from the repo root with the correct PYTHONPATH.
# Usage: python run_backend.py

import os
from pathlib import Path
import subprocess

BASE = Path(__file__).parent / 'genai-chatbot' / 'backend'
os.chdir(BASE)
subprocess.run(['python', 'app.py'])
