pipeline {
    agent any

    stages{
            
        stage('Read Code From BitBucket'){
            steps{
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], browser: [$class: 'BitbucketWeb', repoUrl: 'https://bitbucket.org/icanpe-code-repo/short-url/src/master/'], extensions: [], userRemoteConfigs: [[credentialsId: '96765b53-030a-4256-9a9d-53655ab0835e', url: 'https://Raunak0604@bitbucket.org/icanpe-code-repo/short-url.git']]])
            }
        }
        
        stage('Version.txt'){
            steps{
                script{
                    sh 'echo """Version: $(TAG)""" >> version.txt'
                    sh 'echo """--------------------------------""" >> version.txt'
                    sh 'echo """Build date: $(DATE)""" >> version.txt'
                    sh 'echo """SHA1: $(SHA1)""" >> version.txt'
                    sh 'echo """Branch: $(BRANCH)""" >> version.txt'
                    sh 'echo """Code diff: Behind-Ahead --> $(DIFF)""" >> version.txt'
                    sh 'echo """--------------------------------""" >> version.txt'
                }
            }
        }
        
        stage('Build docker Image'){
            steps{
                script{
                    sh 'docker build -t icanpe/short-url:master- .'
                }
            }
        }
        
        stage('Push Image to Docker-Hub'){
            steps{
                script{
                    withCredentials([string(credentialsId: 'DockerHub-PWD', variable: 'dockerhubpwd')]) {
                        sh 'docker login -u icanpe -p ${dockerhubpwd}'
                    }
                    sh 'docker push icanpe/short-url:master-'
                }
            }
        }

    }
    
} 