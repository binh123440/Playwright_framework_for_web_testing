pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.42.0-jammy'
            args '--shm-size=2g --cap-add=SYS_ADMIN'
        }
    }
    
    environment {
        ALLURE_DIR = 'reports/allure-results'
        PYTHONUNBUFFERED = '1'
        HEADLESS = 'true'
        KEEP_LEGACY_SCREENSHOTS = '0'
    }
    
    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python -m pip install --upgrade pip setuptools wheel
                    pip install -r requirements.txt
                    playwright install --with-deps
                '''
            }
        }
        
        stage('Run E2E Tests') {
            steps {
                sh 'pytest tests/e2e -q --maxfail=1 --alluredir=${ALLURE_DIR}'
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'reports/screenshots/**,reports/allure-results/**', allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            sh 'ls -la reports || true'
        }
        success {
            echo 'Tests passed successfully!'
        }
        failure {
            echo 'Tests failed! Check console output and artifacts.'
        }
    }
}