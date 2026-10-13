"""Phase 1: generate fake search queries with a label per token.

Output: data/raw/queries.csv with columns `query` and `labels`
(space-separated, one label per token: author/category/format/other).
"""

import csv
import random

from query_parser.config import ROOT, load_params

VOCAB = {
    "author": ["maya patel", "john harlow", "lena brooks", "omar diaz", "rita chen", "sam okafor"],
    "category": ["mystery", "romance", "history", "science", "fantasy", "business", "cooking"],
    "format": ["ebook", "audiobook", "pdf", "podcast", "magazine"],
}

# {slot} is filled from VOCAB; any plain word is labeled "other"
TEMPLATES = [
    "{author} {format}",
    "{category} {format}",
    "best {category} {format}",
    "{category} by {author}",
    "{format} by {author}",
    "new {category} {format} for beginners",
    "{author}",
    "free {category} {format}",
]

OUT_PATH = ROOT / "data" / "raw" / "queries.csv"


def make_query(rng: random.Random) -> tuple[list[str], list[str]]:
    tokens, labels = [], []
    for piece in rng.choice(TEMPLATES).split():
        if piece.startswith("{"):
            slot = piece.strip("{}")
            words = rng.choice(VOCAB[slot]).split()
            tokens += words
            labels += [slot] * len(words)
        else:
            tokens.append(piece)
            labels.append("other")
    return tokens, labels


def main() -> None:
    params = load_params()["data"]
    rng = random.Random(params["seed"])

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["query", "labels"])
        for _ in range(params["n_queries"]):
            tokens, labels = make_query(rng)
            writer.writerow([" ".join(tokens), " ".join(labels)])

    print(f"wrote {params['n_queries']} queries to {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
