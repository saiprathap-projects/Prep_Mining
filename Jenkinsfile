pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-north-1'
        AWS_ACCOUNT_ID = '543855656055'
        ECR_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }

    stages {

        stage('Checkout') {
            steps {
                // Declarative checkout already happens automatically
                // This ensures latest repo is available
                checkout scm
            }
        }

        stage('Login to ECR') {
            steps {
                withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
                    sh '''
                        set -e
                        echo "🔐 Logging into Amazon ECR..."
                        aws sts get-caller-identity
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                        echo "✅ Successfully logged into ECR."
                    '''
                }
            }
        }

        stage('Terraform - Create ECR') {
            steps {
                withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
                    script {
                        def appExists = sh(script: "aws ecr describe-repositories --repository-names prep_mining_app --region ${AWS_REGION}", returnStatus: true) == 0
                        def nginxExists = sh(script: "aws ecr describe-repositories --repository-names prep_mining_nginx --region ${AWS_REGION}", returnStatus: true) == 0
                        def mysqlExists = sh(script: "aws ecr describe-repositories --repository-names mysql --region ${AWS_REGION}", returnStatus: true) == 0

                        if (appExists && nginxExists && mysqlExists) {
                            echo "✅ All ECR repositories already exist. Skipping Terraform."
                        } else {
                            echo "🚀 Running Terraform to create ECR repositories..."

                            // ✅ Make sure this directory path matches your repo structure (case-sensitive)
                            dir('terraform') {
                                sh '''
                                    set -euxo pipefail
                                    terraform init -input=false
                                    terraform plan -out=tfplan
                                    terraform apply -auto-approve tfplan
                                '''
                            }
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "🏗️ Building Docker images..."
                    docker compose version
                    docker compose build --no-cache
                '''
            }
        }

        stage('Tag & Push image to ECR') {
            steps {
                script {
                    def commitId = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    def versionTag = "v${env.BUILD_NUMBER}-${commitId}"

                    def images = [
                        'prep_mining_app'  : 'prep_mining_app',
                        'prep_mining_nginx': 'prep_mining_nginx',
                        'mysql'            : 'mysql'
                    ]

                    images.each { localName, repoName ->
                        def latestTag = "${ECR_URL}/${repoName}:latest"
                        def versionedTag = "${ECR_URL}/${repoName}:${versionTag}"

                        sh """
                            docker tag ${localName}:latest ${latestTag}
                            docker tag ${localName}:latest ${versionedTag}
                            docker push ${latestTag}
                            docker push ${versionedTag}
                            echo "✅ Successfully pushed ${repoName} to ECR."
                        """
                    }

                    env.IMAGE_VERSION = versionTag
                    echo "🧾 Image version set to: ${versionTag}"
                }
            }
        }
    }
}
