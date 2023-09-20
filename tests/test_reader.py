from pathlib import Path

from src.reader import read_timebank, read_lusa


ROOT = Path(__file__).parent.parent

def test_read_timebank():
    dataset = read_timebank(ROOT / "resources" / "timebank")
    assert len(dataset) == 183


def test_read_lusa():
    dataset = read_lusa(ROOT / "resources" / "lusa_news")
    assert len(dataset) == 119