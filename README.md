# AI Self-Healing DevOps Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-qwen2.5--coder-lightgrey?style=for-the-badge)

---

## 📌 Project Overview

This project demonstrates an **AI-powered self-healing DevOps pipeline** where an AI agent autonomously monitors AWS infrastructure, analyzes failures using a local LLM (Ollama), and takes corrective actions — all integrated into a Jenkins CI/CD pipeline.

When the Jenkins pipeline detects a failure or the EC2 CPU exceeds a threshold, `ai_agent.py` is triggered automatically. It fetches metrics from **AWS CloudWatch**, sends them to the **Ollama `qwen2.5-coder` model** for diagnosis, and if the AI recommends scaling, it triggers **AWS Auto Scaling** — without any human intervention.

| Component | Technology |
|---|---|
| Web Application | Flask (Python) |
| CI/CD Pipeline | Jenkins |
| Containerization | Docker |
| Cloud Platform | AWS EC2 (`ap-south-1`) |
| AI Model | Ollama (`qwen2.5-coder`) |
| Metrics & Logs | AWS CloudWatch |
| Auto Scaling | AWS Auto Scaling Groups |
| Image Registry | DockerHub |

---

## 🏗️ Architecture

```
  Developer Push
       │
       ▼
┌─────────────────────────────────────────────────────┐
│                  Jenkins Pipeline                   │
│                                                     │
│  1. Checkout  →  2. Build & Tag Docker Image        │
│       ↓                                             │
│  3. Push to DockerHub  →  4. Deploy on EC2          │
│       ↓                                             │
│  5. AI Self-Healing Stage                           │
│       └──► ai_agent.py runs automatically           │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
 ┌─────────────────┐     ┌──────────────────────┐
 │  AWS CloudWatch │     │   AWS CloudWatch     │
 │  (CPU Metrics)  │     │   Logs (fetch_logs)  │
 └────────┬────────┘     └──────────┬───────────┘
          │                         │
          └────────────┬────────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │  Ollama AI Agent      │
           │  (qwen2.5-coder)      │
           │  Analyzes issue &     │
           │  suggests fix         │
           └───────────┬───────────┘
                       │
                       ▼
           ┌───────────────────────┐
           │  Auto Scaling Action  │
           │  (if CPU > 80%)       │
           │  DesiredCapacity → 2  │
           └───────────────────────┘
```

---

## ✨ Features

- **Flask Web App** — Simple Python web application with a home route and `/api` health endpoint, containerized with Docker
- **Jenkins CI/CD Pipeline** — Automated 5-stage pipeline: Checkout → Build → Push to DockerHub → Deploy on EC2 → AI Self-Healing
- **AI Self-Healing Agent (`ai_agent.py`)** — Fetches real-time CPU metrics from CloudWatch; if CPU exceeds 80%, passes the error log to Ollama for analysis and auto-scales the EC2 instance
- **CloudWatch Log Fetching (`fetch_logs.py`)** — Pulls events from AWS CloudWatch Logs (`trail` log group) for AI analysis
- **Automatic Failure Recovery** — Jenkins `post { failure }` block triggers `ai_agent.py --fix` on any pipeline failure
- **DockerHub Integration** — Builds and pushes Docker images to DockerHub using stored Jenkins credentials

---

## 📁 Repository Structure

```
ai-self-healing-devops/
├── app.py               # Flask web application (port 5000)
├── ai_agent.py          # AI self-healing agent (CloudWatch + Ollama + Auto Scaling)
├── fetch_logs.py        # AWS CloudWatch log fetcher
├── deploy.sh            # Deployment script executed on EC2 via SSH
├── Jenkinsfile          # 5-stage Jenkins pipeline definition
├── Dockerfile           # Docker image build instructions
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Flask HTML template
├── .dockerignore
├── .gitignore
└── Ai-Project-*.png     # Architecture / screenshot references
```

---

## 🚀 Getting Started

### Prerequisites

- AWS account with EC2, CloudWatch, and Auto Scaling access
- [Ollama](https://ollama.ai/) installed locally with `qwen2.5-coder` model pulled
- Jenkins server with the following plugins: Git, Docker Pipeline, SSH Agent, Credentials Binding
- DockerHub account
- Python 3.x with `boto3` and `requests`

### 1. Clone the Repository

```bash
git clone https://github.com/Petchimuthu19/ai-self-healing-devops.git
cd ai-self-healing-devops
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure AWS Credentials

```bash
aws configure
# Set region to ap-south-1
```

### 4. Pull the Ollama Model

```bash
ollama pull qwen2.5-coder
ollama serve   # runs on http://localhost:11434
```

### 5. Update `ai_agent.py` with Your Instance ID

```python
INSTANCE_ID = "i-xxxxxxxx"    # Replace with your actual EC2 instance ID
```

Also update the Auto Scaling Group name:

```python
autoscaling.set_desired_capacity(
    AutoScalingGroupName='my-asg',   # Replace with your ASG name
    DesiredCapacity=2
)
```

### 6. Run the Flask App Locally

```bash
python app.py
# App runs at http://0.0.0.0:5000
```

### 7. Run the AI Agent Manually

```bash
python ai_agent.py
```

---

## 🔁 Jenkins Pipeline Stages

| Stage | Description |
|---|---|
| **Checkout** | Clones the repo from GitHub (`main` branch) |
| **Build & Tag** | Builds Docker image tagged as `my-app:latest` |
| **Push to Registry** | Logs into DockerHub and pushes the image |
| **Deploy on EC2** | SCPs `deploy.sh` to EC2 and executes it via SSH |
| **AI Self-Healing** | Runs `ai_agent.py` to check CPU and auto-remediate |

### Jenkins Credentials Required

| Credential ID | Type | Purpose |
|---|---|---|
| `dockerhub_cred` | Username/Password | DockerHub login |
| `ec2-key` | SSH Private Key | SSH access to EC2 |

### Pipeline Failure Handler

If any stage fails, Jenkins automatically runs:
```bash
python3 ai_agent.py --fix
```

---

## 🤖 How the AI Agent Works

```python
# 1. Fetch CPU from CloudWatch (last 5 minutes)
cpu = get_cpu_usage()   # returns average CPU %

# 2. If CPU > 80%, build an error log string
if cpu > 80:
    logs = f"ERROR: EC2 CPU usage is {cpu}%"

    # 3. Send to Ollama (qwen2.5-coder model) for analysis
    result = analyze_logs(logs)

    # 4. If AI response mentions "cpu" or "scale", trigger Auto Scaling
    take_action(result)
    # → autoscaling.set_desired_capacity(DesiredCapacity=2)
```

The Ollama model is prompted with:
> *"Analyze this DevOps issue and suggest fix: ERROR: EC2 CPU usage is X%"*

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Flask** | Python web application framework |
| **Docker** | Containerizing the Flask app |
| **Jenkins** | CI/CD pipeline orchestration |
| **AWS EC2** | Application hosting (`ap-south-1`) |
| **AWS CloudWatch** | CPU metrics and log monitoring |
| **AWS Auto Scaling** | Automated EC2 scaling action |
| **Ollama (`qwen2.5-coder`)** | Local LLM for log/error analysis |
| **boto3** | AWS SDK for Python |
| **DockerHub** | Container image registry |

---

## 📸 Project Screenshots

| Screenshot | Description |
|---|---|
| `Ai-Project-EC2.png` | EC2 instance running the deployed app |
| `Ai-Project-Cloudwatch.png` | CloudWatch metrics dashboard |
| `Ai-Project-jenkins.png` | Jenkins pipeline execution view |

---

## ⚠️ Notes

- The EC2 IP (`13.233.132.134`) in the Jenkinsfile is a placeholder — update it to your own EC2 public IP before running the pipeline.
- Ollama must be running locally (`http://localhost:11434`) before triggering `ai_agent.py`.
- Ensure the EC2 instance's security group allows inbound SSH (port 22) from the Jenkins server and inbound HTTP (port 5000) for the Flask app.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built to demonstrate how AI agents can be embedded directly into DevOps pipelines for autonomous infrastructure healing.
