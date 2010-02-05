


def test_compile():
    try:
        import tiddlywebplugins.wikidata
        assert True
    except ImportError, exc:
        assert False, exc
