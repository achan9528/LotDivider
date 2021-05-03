pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh '#!/bin/bash'
                sh 'export WORKSPACE=`pwd`'
                sh 'virtualenv venv'
                sh 'source venv/bin/activate'
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test LotDividerAPI'
            }
        }
    }
}