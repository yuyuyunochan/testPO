pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'apt-get update -y'
                sh 'apt-get install -y python3 python3-pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Start Redfish Mock (as OpenBMC substitute)') {
            steps {
                sh 'nohup python3 redfish_mock.py > mock.log 2>&1 &'
                sh 'sleep 5'
            }
        }

        stage('Run PyTest (Autotests)') {
            steps {
                sh 'pytest test_redfish.py --junitxml=pytest_report.xml -v'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'pytest_report.xml'
                    junit 'pytest_report.xml'
                }
            }
        }

        stage('Run Load Testing (Locust)') {
            steps {
                sh 'locust -f locustfile.py --headless -u 10 -r 2 --run-time 30s --html=locust_report.html'
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
