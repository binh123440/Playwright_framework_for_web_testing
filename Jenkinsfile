pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.42.0-jammy'
            args '--shm-size=2g --cap-add=SYS_ADMIN -u root'
            reuseNode true
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
        
        stage('Clean Cache') {
            steps {
                sh '''
                    echo "Cleaning up cache and temporary files..."
                    rm -rf .pytest_cache || true
                    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
                    find . -type f -name "*.pyc" -delete 2>/dev/null || true
                    echo "✓ Cache cleanup complete!"
                '''
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python -m pip install --upgrade pip setuptools wheel
                    pip install -r requirements.txt
                    python -m playwright install --with-deps
                '''
            }
        }
        
        stage('Run E2E Tests') {
            steps {
                sh 'xvfb-run pytest tests/e2e -v --maxfail=1 --alluredir=${ALLURE_DIR} -n auto --reruns 2 --reruns-delay 1'
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