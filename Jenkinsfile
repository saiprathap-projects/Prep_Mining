pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-north-1'
        AWS_ACCOUNT_ID = '543855656055'
    }

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'git@github.com:saiprathap-projects/Prep_Mining.git'
            }
        }

        stage('Login to ECR') {
            steps {
                withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
                    sh '''
                        set -e
                        echo "🔐 Logging into Amazon ECR..."
                        aws ecr get-login-password --region $AWS_REGION | \
                        docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                        echo "✅ Successfully logged into ECR."
                    '''
                }
            }
        }

        stage ('Terraform - Create ECR') {
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
                script {
                    sh '''
                        cd $WORKSPACE
                        docker compose version
                        docker compose build --no-cache
                    '''
                }
            }
        }

        stage('Tag & Push image to ECR') {
            steps {
                script {
                    def ecrUrl = "${env.AWS_ACCOUNT_ID}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"
                    def commitId = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    def versionTag = "v${env.BUILD_NUMBER}-${commitId}"

                    def images = [
                        'prep_mining_app'  : 'prep_mining_app',
                        'prep_mining_nginx': 'prep_mining_nginx',
                        'mysql'            : 'mysql'
                    ]

                    images.each { localName, repoName ->
                        def localImage = "${localName}:latest"
                        def latestTag = "${ecrUrl}/${repoName}:latest"
                        def versionedTag = "${ecrUrl}/${repoName}:${versionTag}"

                        sh """
                            docker tag ${localImage} ${latestTag}
                            docker tag ${localImage} ${versionedTag}
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
