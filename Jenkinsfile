pipeline {
    agent {
        docker {
            image 'python:3.9-slim' // Используем образ с Python 3
            args '-u root'         // Нужно для установки пакетов (если потребуется)
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Start Redfish Mock') {
            steps {
                sh 'nohup python3 redfish_mock.py > mock.log 2>&1 &'
                sh 'sleep 5'
            }
        }

        stage('Run PyTest') {
            steps {
                sh 'python3 -m pytest test_redfish.py --junitxml=pytest_report.xml -v'
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
                sh 'python3 -m locust -f locustfile.py --headless -u 10 -r 2 --run-time 30s --html=locust_report.html'
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