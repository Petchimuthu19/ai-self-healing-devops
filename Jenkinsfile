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

        stage('Deploy') {
            steps {
                sh 'echo Deploying to AWS...'
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
