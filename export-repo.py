import os
import shutil

ORGANIZATIONS = ["tum-esm"]
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(PROJECT_DIR, "out")


if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.mkdir(OUT_DIR)

for organization in ORGANIZATIONS:
    assert " " not in organization, "spaces not allowed in organization names"
