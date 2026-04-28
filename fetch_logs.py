import boto3

client = boto3.client('logs')

response = client.filter_log_events(
    logGroupName='trail'
)

logs = ""
for event in response['events']:
    logs += event['message'] + "\n"
