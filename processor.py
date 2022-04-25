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

def process(unprocessed):
    import subprocess, os
    for u in unprocessed:
        search_string = u['search_string']
        output = subprocess.run(['python', 'library-fetch-article.py', search_string], capture_output=True)
        print(output.stdout, output.stderr)
        assert b'/tmp/' in output.stdout
        filename = output.stdout.decode().replace('\n', '')
        import boto3
        s3 = boto3.client('s3')
        key = 'apps/wsj/data/' + filename.replace('/tmp/', '')
        s3.upload_file(filename, 'cloudmatica', key)
    return True