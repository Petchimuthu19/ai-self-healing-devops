import requests
import boto3

OLLAMA_URL = "http://localhost:11434/api/chat"

def analyze_logs(logs):
    payload = {
        "model": "qwen2.5-coder",
        "messages": [
            {"role": "user", "content": f"Analyze this DevOps log and suggest fix:\n{logs}"}
        ]
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["message"]["content"]

# AWS client
autoscaling = boto3.client('autoscaling', region_name='ap-south-1')

def take_action(ai_result):
    print("AI Decision:", ai_result)

    # 🔥 Example: CPU issue → scale EC2
    if "CPU" in ai_result or "scale" in ai_result:
        autoscaling.set_desired_capacity(
            AutoScalingGroupName='my-asg',
            DesiredCapacity=3
        )
        print("✅ Scaling EC2 instances...")

# Example log
logs = "ERROR: EC2 CPU usage 95%"

result = analyze_logs(logs)
take_action(result)
