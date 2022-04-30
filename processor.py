# processor.py runs on the processing server
# it polls the state on the s3 bucket
# for every unfulfilled request, it generates a PDF
# and uploads it into the /apps/wsj/data folder

def get_state():
    import boto3, json
    s3 = boto3.client('s3')
    try:
        s3.download_file('cloudmatica', 'apps/wsj/state.json', '/tmp/state.json')
    except:
        return 'Unable to download state'
    with open('/tmp/state.json') as f:
        try:
            state = json.load(f)
        except:
            return 'Unable to parse state'
    return state

def identify_unprocessed(state):
    return [s for s in state if 'result' not in s]

def process(message):
    import subprocess
    search_string = message['search_string']
    output = subprocess.run(['python', 'library-fetch-article.py', search_string], capture_output=True)
    print(output.stdout, output.stderr)
    assert b'/tmp/' in output.stdout
    filename = output.stdout.decode().replace('\n', '')
    import boto3
    s3 = boto3.client('s3')
    key = 'apps/wsj/data/' + filename.replace('/tmp/', '')
    s3.upload_file(filename, 'cloudmatica', key)
    return True

def send_message(message_body):
    import boto3
    session = boto3.Session(profile_name='vbalasu_admin')
    sqs = session.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/251566558623/library-fetch-article'
    import json
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))
    return response['ResponseMetadata']['HTTPStatusCode'] == 200

def get_message():
    import boto3
    session = boto3.Session(profile_name='vbalasu_admin')
    sqs = session.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/251566558623/library-fetch-article'
    response = sqs.receive_message(QueueUrl=queue_url, WaitTimeSeconds=20)
    if 'Messages' in response:
        return response['Messages'][0]
    else:
        return False

def delete_message(receipt_handle):
    import boto3
    session = boto3.Session(profile_name='vbalasu_admin')
    sqs = session.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/251566558623/library-fetch-article'
    response = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    return response['ResponseMetadata']['HTTPStatusCode'] == 200
    

def loop():
    import json
    for ctr in range(2):
        print(ctr)
        message = get_message()
        if message:
            print(message['Body'])
            process(json.loads(message['Body']))
            delete_message(message['ReceiptHandle'])
        else:
            print('No message')
    return True
