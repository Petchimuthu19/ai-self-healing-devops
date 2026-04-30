pipeline {
    agent any

    environment {
        EC2_IP = "13.233.132.134"
        IMAGE = "my-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Petchimuthu19/Ai-Project.git'
            }
        }

        stage('Build & Tag') {
            steps {
                sh '''
                docker build -t $IMAGE:latest .
                '''
            }
        }

        stage('Push to Registry (FASTER)') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub_creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "🔐 Logging into DockerHub..."
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                    echo "📦 Tagging image..."
                    docker tag $IMAGE:latest $DOCKER_USER/$IMAGE:latest

                    echo "🚀 Pushing image..."
                    docker push $DOCKER_USER/$IMAGE:latest
                    '''
               }
            }
        }    

        stage('Deploy on EC2 (USE GITHUB SCRIPT)') {
            steps {
                sshagent(['ec2-key']) {
                   sh '''
                   # Copy deploy.sh from Jenkins workspace to EC2
                   scp -o StrictHostKeyChecking=no deploy.sh ec2-user@$EC2_IP:/home/ec2-user/

                   # Execute script on EC2
                   ssh -o StrictHostKeyChecking=no ec2-user@$EC2_IP "
                        chmod +x /home/ec2-user/deploy.sh &&
                        /home/ec2-user/deploy.sh
                   "
                   '''
                }
            }
        }

        stage('AI Self-Healing') {
            steps {
                sh '''
                python3 ai_agent.py || echo "AI handled error"
                '''
            }
        }
    }

    post {
        failure {
            echo "Deployment failed → Running AI Fix"

            sh '''
            python3 ai_agent.py --fix
            '''
        }
    }
}
