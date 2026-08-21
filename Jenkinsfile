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

        stage('Checkout from Git') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Yashnani-code/uptime-kuma.git'
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
                    sh '''
                        $SCANNER_HOME/bin/sonar-scanner \
                        -Dsonar.projectName=uptime \
                        -Dsonar.projectKey=uptime
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    waitForQualityGate(
                        abortPipeline: false,
                        credentialsId: 'Sonar-token'
                    )
                }
            }
        }

        stage('OWASP FS SCAN') {
            steps {
                dependencyCheck(
                    additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit',
                    odcInstallation: 'DP-Check'
                )

                dependencyCheckPublisher(
                    pattern: '**/dependency-check-report.xml'
                )
            }
        }

        stage('TRIVY FS SCAN') {
            steps {
                sh 'trivy fs . > trivyfs.json'
            }
        }

        stage('Docker Build & Push') {
            steps {
                script {
                    withDockerRegistry(
                        credentialsId: 'docker',
                        toolName: 'docker'
                    ) {

                        sh 'docker build -t uptime .'

                        sh 'docker tag uptime YOUR_DOCKERHUB_USERNAME/uptime:latest'

                        sh 'docker push YOUR_DOCKERHUB_USERNAME/uptime:latest'
                    }
                }
            }
        }

        stage('TRIVY IMAGE SCAN') {
            steps {
                sh '''
                    trivy image \
                    YOUR_DOCKERHUB_USERNAME/uptime:latest \
                    > trivy.json
                '''
            }
        }

        stage('Remove Old Container') {
    steps {
        sh 'docker stop uptime-kuma || true'
        sh 'docker rm uptime-kuma || true'
    }
}

        stage('Deploy to Container') {
            steps {
                sh '''
                    docker run -d \
                    --name uptime \
                    -p 3001:3001 \
                    YOUR_DOCKERHUB_USERNAME/uptime:latest
                '''
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
    }
}
