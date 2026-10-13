import random

from query_parser.generate_data import make_query


def test_one_label_per_token():
    rng = random.Random(0)
    for _ in range(100):
        tokens, labels = make_query(rng)
        assert len(tokens) == len(labels)
