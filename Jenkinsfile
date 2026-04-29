pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'echo SUCCESS'
            }
        }
    }
}

    environment {
        EC2_IP = "52.66.209.208"
        KEY = "/var/lib/jenkins/Test.pem"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Petchimuthu19/Ai-Project.git'
            }
        }
     
        stage('Debug') {
            steps {
                sh 'pwd'
                sh 'ls -l'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                export DOCKER_BUILDKIT=0
                pwd
                ls -l
                docker build -t my-app .
                '''
            }
        }

        stage('Save Docker Image') {
            steps {
                sh 'docker save my-app > my-app.tar'
            }
        }


        stage('Deploy on EC2') {
            steps {
                sh '''
                scp -i $KEY deploy.sh ec2-user@$EC2_IP:/home/ec2-user/
                scp -i $KEY my-app.tar ec2-user@$EC2_IP:/home/ec2-user/

                ssh -i $KEY ec2-user@$EC2_IP "chmod +x deploy.sh && ./deploy.sh"
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
