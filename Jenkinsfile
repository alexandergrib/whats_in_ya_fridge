pipeline {
    agent {
        docker { image 'hello-world' }
    }
    stages {
        stage('Test') {
            steps {
                sh 'docker --version'
//                     sh 'echo "hello"'
            }
        }
    }
}