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
               AWS_REGION = 'eu-north-1'               // Change as per your region
               AWS_ACCOUNT_ID = '543855656055'         // Replace with your AWS account ID
            }
            steps {
               withCredentials([usernamePassword(
                   credentialsId: 'aws-credentials',
                   usernameVariable: 'AWS_ACCESS_KEY_ID',
                   passwordVariable: 'AWS_SECRET_ACCESS_KEY'
               )]) {
                   sh '''
                       set -e

                       echo "Configuring AWS CLI..."
                       aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                       aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                       aws configure set region $AWS_REGION

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
