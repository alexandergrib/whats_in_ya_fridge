pipeline {
    agent {
        docker { image 'centos' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'docker --version'
                sh 'docker-compose build'
                sh 'docker-compose up'
//                     sh 'echo "hello"'
            }
        }
    }
}