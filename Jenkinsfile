pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install pip and Python Dependencies') {
            steps {
                sh 'python3 -m ensurepip --user'
                sh 'export PATH="$HOME/.local/bin:$PATH" && python3 -m pip install --user -r requirements.txt'
            }
        }

        stage('Start Redfish Mock') {
            steps {
                sh 'export PATH="$HOME/.local/bin:$PATH" && nohup python3 redfish_mock.py > mock.log 2>&1 &'
                sh 'sleep 5'
            }
        }

        stage('Run PyTest') {
            steps {
                sh 'export PATH="$HOME/.local/bin:$PATH" && python3 -m pytest test_redfish.py --junitxml=pytest_report.xml -v'
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
                sh 'export PATH="$HOME/.local/bin:$PATH" && python3 -m locust -f locustfile.py --headless -u 10 -r 2 --run-time 30s --html=locust_report.html'
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
