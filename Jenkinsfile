pipeline {
    agent any

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

        stage('Deploy on EC2') {
            steps {
                sh '''
                # Copy files to EC2
                scp -o StrictHostKeyChecking=no -i $KEY my-app.tar ec2-user@$EC2_IP:/home/ec2-user/
                scp -o StrictHostKeyChecking=no -i $KEY deploy.sh ec2-user@$EC2_IP:/home/ec2-user/

                # Run deployment script on EC2
                ssh -o StrictHostKeyChecking=no -i $KEY ec2-user@$EC2_IP "
                    chmod +x deploy.sh &&
                    ./deploy.sh
                "
                '''
            }
        }

        stage('AI Analysis (Self-Healing)') {
            steps {
                sh 'python3 ai_agent.py'
            }
        }
    }
}
