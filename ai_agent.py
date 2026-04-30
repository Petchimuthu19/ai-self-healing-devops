import boto3
import requests
from datetime import datetime, timedelta

# AWS
cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')
autoscaling = boto3.client('autoscaling', region_name='ap-south-1')

# Ollama
OLLAMA_URL = "http://localhost:11434/api/chat"

# Your EC2 instance ID
INSTANCE_ID = "i-xxxxxxxx"

def get_cpu_usage():

    metrics = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': INSTANCE_ID
            }
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=5),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average']
    )

    datapoints = metrics['Datapoints']

    if datapoints:
        return datapoints[-1]['Average']

    return 0


def analyze_logs(logs):

    payload = {
        "model": "qwen2.5-coder",
        "messages": [
            {
                "role": "user",
                "content": f"Analyze this DevOps issue and suggest fix:\n{logs}"
            }
        ]
    }

    response = requests.post(OLLAMA_URL, json=payload)

    return response.json()["message"]["content"]


def take_action(ai_result):

    print("AI Decision:", ai_result)

    if "cpu" in ai_result.lower() or "scale" in ai_result.lower():

        autoscaling.set_desired_capacity(
            AutoScalingGroupName='my-asg',
            DesiredCapacity=2
        )

        print("✅ Scaling EC2 instances...")


cpu = get_cpu_usage()

print(f"🔥 Current CPU Usage: {cpu}%")

if cpu > 80:

    logs = f"ERROR: EC2 CPU usage is {cpu}%"

    result = analyze_logs(logs)

    take_action(result)

else:
    print("✅ CPU usage normal")
