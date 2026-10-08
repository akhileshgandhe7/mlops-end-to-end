from query_parser.config import load_params


def test_params_load():
    params = load_params()
    assert params["data"]["seed"] == 42
