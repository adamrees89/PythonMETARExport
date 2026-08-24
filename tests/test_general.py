import os


def test_metarGet_exists():
    repo_root = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(repo_root, "metarGet.py")
    assert os.path.exists(path), f"metarGet.py not found at {path}"
