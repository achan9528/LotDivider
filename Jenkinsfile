pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh 'coverage run manage.py test LotDividerAPI'
                sh 'coverage report'
            }
        }
    }
}