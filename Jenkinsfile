pipeline {
    agent any
    stages{
        stage(‘Build’) {
            sh ‘docker-compose –f production.yml run –rm compile’
        }
        stage(‘Test) {
            sh ‘docker-compose –f production.yml run –rm test’
        }

    }
}

