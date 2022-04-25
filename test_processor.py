import processor

def test_get_state():
    state = processor.get_state()
    assert type(state) == list

def test_identify_unprocessed():
    state = [{"search_string": "Databricks", "who": "vbalasu@gmail.com"}]
    unprocessed = processor.identify_unprocessed(state)
    assert unprocessed == state

def test_identify_processed():
    state = [{"search_string": "Databricks", "who": "vbalasu@gmail.com", "result": "/apps/wsj/data/result.pdf"}]
    unprocessed = processor.identify_unprocessed(state)
    assert unprocessed == []

def test_process():
    result = processor.process([{"search_string": "Google", "who": "vbalasu@gmail.com"}])
    assert result is True
