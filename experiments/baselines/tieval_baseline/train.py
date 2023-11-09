
from pathlib import Path

from tieval import datasets, models


PWD = Path(__file__).parent

def main():
    corpus = datasets.read("aquaint") + datasets.read("platinum") + datasets.read("eventtime")

    model = models.EventIdentificationBaseline(path=PWD / "model")
    for epoch in range(5):
        model.fit(
            corpus.train, 
            # corpus.test, 
            dropout=0.1,
            from_scratch=True
        )
    model.save()

if __name__ == "__main__":
    main()
