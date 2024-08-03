pipeline {
    agent any
    stages {
        /*stage('Load Shared Library') {
            steps {
                script {
                    // Cargar el archivo gitUtils.groovy que esta en el mismo repositorio
                    load 'gitUtils.groovy'
                }
            }
        }*/
        
        stage('Inicio') {
            steps {
                script {
                    env.branch = infoPayload('branch') // devuelve la rama desde donde se hizo el pull request
                    env.repo = infoPayload('urlRepo') // devuelve la url del repositorio en protocolo https
                    env.nameProject = infoPayload('nameProject') // devuelve el nombre del repositorio/proyecto
                    
                    // Checkout del repositorio Git
                    gitCheckout(
                        env.branch,
                        env.repo
                    )
                }
            }
        }

        stage('Verificacion_payload_Webhook') {
            when {
                expression {
                    // Verifica si el webhook fue activado por un push a la rama develop
                    return env.WEBHOOK_BRANCH == 'develop'
                }
            }
            steps {
                echo 'Verificación de payload webhook completada'
            }
        }

        stage('Construir, Subir Imagen Docker y Descargarla') {
            steps {
                script {
                    def imageName = 'coco1995/projectnexos'
                    def version = env.BUILD_NUMBER // Usa el ID del build como la versión

                    // Construir la imagen Docker,se tiene que tener el pluggin Docker Pipeline instalado en Jenkins
                    docker.build("${imageName}:${version}", '.')

                    // Subir la imagen Docker al repositorio en DockerHub
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image("${imageName}:${version}").push()
                    }

                    // Descargar la imagen desde DockerHub
                    sh "docker pull ${imageName}:${version}"

                    // Ejecutar un contenedor y mostrar logs
                    def containerId = sh(script: "docker run -dp 5000:5000 ${imageName}:${version}", returnStdout: true).trim()
                    sh "docker logs ${containerId}"

                    sleep(60)

                    // Limpiar: detener y eliminar el contenedor
                    sh "docker stop ${containerId}"
                    sh "docker rm ${containerId}"
                }
            }
        }
        
        stage('Pruebas Unitarias') {
            steps {
                script {
                    docker.image('coco1995/python3.8_root:v1').inside {
                        // Ejecutar pruebas
                        sh 'python3 -m pytest test_pruebaTecnica.py'                     
                    }
                }
            }
        }

        stage('Sonar scan') {
            steps {
                script {
                    docker.image('sonarsource/sonar-scanner-cli').inside{
                        withSonarQubeEnv('sonarqube') {
                            // Verificar si el proyecto ya existe en SonarQube
                            def projectExists = sh(
                                script: """
                                    curl -s -o /dev/null -w "%{http_code}" -u ${env.SONAR_AUTH_TOKEN}: ${env.SONAR_HOST_URL}/api/projects/search?projects=${env.nameProject}
                                """,
                                returnStdout: true
                            ).trim() == '200'

                            // Crear proyecto en SonarQube si no existe
                            if (!projectExists) {
                                sh """
                                    curl -X POST -u ${env.SONAR_AUTH_TOKEN}: \
                                    ${env.SONAR_HOST_URL}/api/projects/create?project=${env.nameProject}&name=${env.nameProject}
                                """
                            }

                            sh """
                                sonar-scanner \
                                -Dsonar.host.url=${env.SONAR_HOST_URL} \
                                -Dsonar.projectKey=${env.nameProject} \
                                -Dsonar.projectName=${env.nameProject} \
                                -Dsonar.login=${env.SONAR_AUTH_TOKEN} \
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
        post {
            success {
                echo 'Pipeline ejecutado exitosamente!'
            }
            failure {
                echo 'El pipeline ha fallado - se requiere intervención.'
            }
        }
    }    
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////
/**********************************************************************************************************
*Metodo que permite leer el json del payload y retorna un string con el valor correspondiente, 
se necesita contar con el pluggin Pipeline Utility Steps instalado en Jenkins
*Paramatros:
    - request: string con la consulta que queremos realizar
*Opciones:
    - title:
    - urlRepo: devuelve la url del repositorio en protocolo https
    - action: devuelve accion del pull request (opened , closed)
    - user: devuelve el usuario que abrió el pull request
    - environment: devuelve la rama hacia donde se hizo el pull request
    - branch: devuelve la rama desde donde se hizo el pull request
    - nameProject: devuelve el nombre del proyecto
***/
def infoPayload(request){
    def result = readJSON text: payload
    if(request == 'title'){
        return result.pull_request.title
    }else if(request == 'urlRepo'){
        return result.repository.clone_url
    }else if(request == 'user'){
        return result.pull_request.user.login
    }else if(request == 'branch'){
        def ref = result.ref
        return ref.split('/').last()
    }else if(request == 'environment'){
        return result.pull_request.base.ref
    }else if(request == 'nameProject'){
        return result.repository.name
    }else if(request == 'issue'){
        def pattern = /.*issue=/
        return result.pull_request.title.replaceAll(pattern,"").trim()
    }
}

/***********************************************************************************************************
*Script que realiza el clone de las fuentes
*Variables:
    - branch: string, rama donde se realizará el clone
    - repo: String, url del repositorio a clonar
***/
def gitCheckout(branch, repo) {
    stage('checkout') {
        checkout([
            $class: 'GitSCM',
            branches: [[name: branch]], // Especifica la rama que deseas clonar
            extensions: [[
                $class: 'CloneOption',
                noTags: false,
                reference: '',
                shallow: false
            ]],
            userRemoteConfigs: [[
                credentialsId: 'github_nicolas_repo',
                url: repo
            ]]
        ])
    }
}
