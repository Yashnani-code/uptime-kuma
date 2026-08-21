pipeline {
    agent any
    tools {
        jdk 'jdk17'
        nodejs 'node18'
    }
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout from Git') {
            steps {
                git branch: 'main', url: 'https://github.com/Yashnani-code/uptime-kuma.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'npm install'
            }
        }
        stage('Sonarqube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=uptime -Dsonar.projectKey=uptime'
                }
            }
        }
        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: false
                }
            }
        }
        stage('OWASP FS SCAN') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    dependencyCheck additionalArguments: '--scan ./ --format XML --format HTML --out .', odcInstallation: 'DP-Check'
                    dependencyCheckPublisher pattern: 'dependency-check-report.xml'
                }
            }
        }
        stage('TRIVY FS SCAN') {
            steps {
                sh 'trivy fs --format table -o trivy-fs-report.html .'
            }
        }
        stage('Docker Build & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker build -t yashnani0512/uptime-kuma:latest .
                        docker push yashnani0512/uptime-kuma:latest
                    '''
                }
            }
        }
        stage('TRIVY IMAGE SCAN') {
            steps {
                sh 'trivy image --format table -o trivy-image-report.html yashnani0512/uptime-kuma:latest'
            }
        }
        stage('Deploy to Container') {
            steps {
                sh '''
                    docker stop uptime || true
                    docker rm uptime || true
                    docker run -d --name uptime -p 3001:3001 yashnani0512/uptime-kuma:latest
                '''
            }
        }
    }
}
       
       
       
