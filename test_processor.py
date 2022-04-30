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

# def test_process():
#     result = processor.process({"search_string": "Google", "who": "vbalasu@gmail.com"})
#     assert result is True

def test_send_message():
    import datetime
    result = processor.send_message({'time': datetime.datetime.utcnow().isoformat()})
    assert result is True

def test_get_and_delete_message():
    result_get = processor.get_message()
    assert type(result_get) == dict or result_get is False
    if result_get:
        result_delete = processor.delete_message(result_get['ReceiptHandle'])
    assert result_delete is True

def test_send_2_messages():
    search_strings = ['Ukraine', 'Google Cloud', 'Databricks', 'Solana', 'Bitcoin']
    for ctr in range(2):
        processor.send_message({'ctr': ctr, 'search_string': search_strings[ctr]})
    assert True

def test_loop():
    result = processor.loop()
    assert result is True