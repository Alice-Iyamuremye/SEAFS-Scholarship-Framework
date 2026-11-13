"""Test configuration for importing the repository's top-level research modules."""
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
root_string = str(REPOSITORY_ROOT)
if root_string not in sys.path:
    sys.path.insert(0, root_string)
