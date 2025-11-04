pipeline {
    agent any

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
            environment {
               AWS_REGION = 'eu-north-1'               
               AWS_ACCOUNT_ID = '543855656055'         
            }
            steps {
                 withAWS(credentials: 'aws-credentials', region: "${AWS_REGION}") {
                  sh '''
                      set -e

                      echo "Logging into Amazon ECR..."
                      aws ecr get-login-password --region $AWS_REGION | \
                      docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                      echo "✅ Successfully logged into ECR."
                      
                      '''
                }
            }
        }    
    }
}
