pipeline {
    agent any
        environment {
            sonarURL = 'http://localhost:9000' // URL del servidor SonarQube
            sonarToken = 'sonarqube' // ID de credencial en Jenkins
        }
        stages {
            stage('Verificacion de payload Webhook') {
                when {
                    expression {
                        // Verifica si el webhook fue activado por un push a la rama develop
                        return env.WEBHOOK_BRANCH == 'develop'
                    }
                }
            }

        stage('Inicio') {
            steps {
                script {
                    env.branch = gitUtils.infoPayload('branch') // devuelve la rama desde donde se hizo el pull request
                    env.repo = gitUtils.infoPayload('urlRepo') // devuelve la url del repositorio en protocolo https
                    env.environment = gitUtils.infoPayload('environment') // devuelve la rama hacia donde se hizo el pull request
                    env.nameProject = gitUtils.infoPayload('nameProject') // devuelve el nombre del repositorio/proyecto
                    env.userGit = gitUtils.infoPayload('user') // devuelve el usuario que abrió el pull request
                    env.issue = gitUtils.infoPayload('issue') // devuelve el número de solicitud pull
                    env.title = gitUtils.infoPayload('title') // devuelve el título de la solicitud pull request
                    
                    // Checkout del repositorio Git
                    gitUtils.gitCheckout(
                        branch: env.branch,
                        repo: env.repo
                    )
                }
            }
        }

        stage('Pruebas Unitarias') {
            steps {
                script {
                    docker.image('python:alpine3.20').inside {
                    // Instala las dependencias necesarias
                    sh 'pip install -r requirements.txt'
                    sh 'python3 -m pytest test_pruebaTecnica.py'
                    }
                }
            }
        }

        stage('Sonar scan') {
            steps {
                script {
                    withCredentials([string(credentialsId: "${env.sonarToken}", variable: 'token')]) {
                        // Verificar si el proyecto ya existe en SonarQube
                        def projectExists = sh(
                            script: """
                                curl -s -o /dev/null -w "%{http_code}" -u ${token}: \${env.sonarURL}/api/projects/search?projects=${env.nameProject}
                            """,
                            returnStdout: true
                        ).trim() == '200'

                        // Crear proyecto en SonarQube si no existe
                        if (!projectExists) {
                            sh """
                                curl -X POST -u ${token}: \
                                ${env.sonarURL}/api/projects/create?project=${env.nameProject}&name=${env.nameProject}
                            """
                        }
                        withSonarQubeEnv('sonarqube') {
                            sh """
                                sonar-scanner \
                                -Dsonar.host.url=${env.sonarURL} \
                                -Dsonar.projectKey=${env.nameProject} \
                                -Dsonar.projectName=${env.nameProject} \
                                -Dsonar.login=${token} \
                            """
                            //-Dsonar.exclusions=**/tests/**,**/docs/**
                        }

                        timeout(time: 2, unit: 'MINUTES') {
                            def qualityGate = waitForQualityGate()
                            if (qualityGate.status != 'OK') {
                                env.sonarqubeState = "failed"
                                error "Pipeline aborted due to quality gate failure: ${qualityGate.status}"
                            }
                        }
                    }
                }
            }
        }
    
        stage('Construir y Subir Imagen Docker') {
            steps {
                script {
                    def imageName = 'coco1995/nexos'
                    def version = env.BUILD_NUMBER // Usa el ID del build como la versión

                    // Construir la imagen Docker,se tiene que tener el pluggin Docker Pipeline instalado en Jenkins
                    docker.build("${imageName}:${version}", '.')

                    // Subir la imagen Docker al repositorio en DockerHub
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image("${imageName}:${version}").push()
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Pipeline ejecutado exitosamente!'
        }
        failure {
            echo 'El pipeline ha fallado - se requiere intervención.'
        }
    }
}
