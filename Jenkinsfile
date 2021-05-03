pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh 'cd /Desktop/dojo/python/my_environments; source djangoPy3Env/bin/activate;'
                sh 'cd ~/Desktop/LotDivider'
                sh 'python --version'
                sh 'python manage.py test LotDividerAPI'
            }
        }
    }
}