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
    }
}
