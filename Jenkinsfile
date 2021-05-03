pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh 'source ~/.bashrc'
                sh 'activate-djangoEnv'
                sh 'project'
                sh 'python --version'
                sh 'python manage.py test LotDividerAPI'
            }
        }
    }
}