pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/Petchimuthu19/Ai-Project.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t my-app .'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh 'scp -i Test.pem app ec2-user@43.205.206.144:/home/ec2-user/'
                sh 'ssh ec2-user@43.205.206.144 "docker run -d -p 80:80 my-app"'
            }
        }

        // 🔥 YOUR AI INTEGRATION
        stage('AI Analysis (Self-Healing)') {
            steps {
                sh 'python3 ai_agent.py'
            }
        }
    }
}
