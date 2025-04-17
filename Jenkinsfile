pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout([ 
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [], 
                    userRemoteConfigs: [[ 
                        url: 'https://github.com/Tom77-7/AbroadConsultancy.git', 
                        credentialsId: 'AbroadID' 
                    ]] 
                ])
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker Compose services...'
                bat 'docker-compose -p abroadconsultancy build'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Skipping tests for now...'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application using Docker Compose...'
                bat 'docker-compose -p abroadconsultancy up -d'
            }
        }
    }
}