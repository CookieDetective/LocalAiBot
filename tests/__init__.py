# Ensure the repository root is on sys.path so top-level packages (like `tools`)
# can be imported when running pytest from the terminal.
import sys
from pathlib import Path

# repo_root = project root (parent of tests/)
repo_root = Path(__file__).resolve().parents[1]
repo_root_str = str(repo_root)

if repo_root_str not in sys.path:
    # insert at front so local packages shadow installed ones
    sys.path.insert(0, repo_root_str)

# keep __all__ explicit (optional)
__all__ = []