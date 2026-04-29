pipeline {
    agent any

    environment {
        EC2_IP = "52.66.209.208"
        KEY = "Test.pem"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/Petchimuthu19/Ai-Project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-app .'
            }
        }

        stage('Save Docker Image') {
            steps {
                sh 'docker save my-app > my-app.tar'
            }
        }

        stage('Copy to EC2') {
            steps {
                sh '''
                scp -i $KEY my-app.tar ec2-user@$EC2_IP:/home/ec2-user/
                '''
            }
        }

        stage('Deploy on EC2') {
            steps {
                sh '''
                ssh -i $KEY ec2-user@$EC2_IP << EOF
                docker load < my-app.tar
                docker stop my-app || true
                docker rm my-app || true
                docker run -d -p 80:3000 --name my-app my-app
                EOF
                '''
            }
        }

        // 🔥 AI Integration
        stage('AI Analysis (Self-Healing)') {
            steps {
                sh 'python3 ai_agent.py'
            }
        }
    }
}
