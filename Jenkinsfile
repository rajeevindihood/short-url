pipeline {
    agent any

    stages{
            
        stage('Read Code From BitBucket'){
            steps{
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], browser: [$class: 'BitbucketWeb', repoUrl: 'https://bitbucket.org/icanpe-code-repo/short-url/src/master/'], extensions: [], userRemoteConfigs: [[credentialsId: '96765b53-030a-4256-9a9d-53655ab0835e', url: 'https://Raunak0604@bitbucket.org/icanpe-code-repo/short-url.git']]])
            }
        }
        
        stage('Build docker Image'){
            steps{
                script{
                    sh 'docker build -t icanpe/short-url .'
                }
            }
        }
        
        stage('Push Image to Docker-Hub'){
            steps{
                script{
                    withCredentials([string(credentialsId: 'DockerHub-PWD', variable: 'dockerhubpwd')]) {
                        sh 'docker login -u icanpe -p ${dockerhubpwd}'
                    }
                    sh 'docker push icanpe/short-url'
                }
            }
        }

    }
    
} 