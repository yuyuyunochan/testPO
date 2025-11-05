pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'  // чтобы можно было устанавливать пакеты (если нужно)
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Start Redfish Mock') {
            steps {
                sh 'nohup python redfish_mock.py > mock.log 2>&1 &'
                sh 'sleep 5'
            }
        }

        stage('Run PyTest') {
            steps {
                sh 'python -m pytest test_redfish.py --junitxml=pytest_report.xml -v'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'pytest_report.xml'
                    junit 'pytest_report.xml'
                }
            }
        }

        stage('Run Load Testing') {
            steps {
                sh 'python -m locust -f locustfile.py --headless -u 10 -r 2 --run-time 30s --html=locust_report.html'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'locust_report.html'
                }
            }
        }

        stage('Cleanup') {
            steps {
                sh 'pkill -f redfish_mock.py || true'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'mock.log'
        }
    }
}