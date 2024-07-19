/**********************************************************************************************************
*Metodo que permite leer el json del payload y retorna un string con el valor correspondiente
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
        return result.pull_request.head.ref
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
def gitCheckout(Map pipelineParams = [:]) {
    stage('checkout') {
        checkout([
            $class: 'GitSCM',
            branches: [[name: pipelineParams.branch]], //Especifica la rama que deseas clonar
            extensions: [[
                $class: 'CloneOption',
                noTags: false,
                reference: '',
                shallow: false
            ]],
            userRemoteConfigs:  [[
                credentialsId: 'github_nicolas',
                url: pipelineParams.repo
            ]]
        ])
    }
}
 
 