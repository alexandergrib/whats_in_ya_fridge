node {

    try {
//         stage 'Checkout'
//             checkout scm

//             sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
//             def lastChanges = readFile('GIT_CHANGES')
//             slackSend color: "warning", message: "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges}"

        stage 'Test'
//             git 'https://github.com/alexandergrib/testDjango.git'
//             sh 'pip install virtualenv'
// //             sh 'PATH=/var/lib/jenkins/.local/bin'
//             sh 'virtualenv env -p python3.9'
// //             sh '. /var/lib/jenkins/.local/bin/activate'
//
//             cd /home/alex/bin
// //             cd .virtualenvs/alex/bin
//             source activate
//             sh 'pip install -r requirements.txt'
//             sh 'env/bin/python3.9 manage.py test --testrunner=djtrump.tests.test_runners.NoDbTestRunner'

        stage 'Deploy'
//                sh  'docker run hello-world'
//             sh './deployment/deploy_prod.sh'
//             sh 'pip3 install django'
//             sh 'python3 manage.py runserver 8080'
//                sh '''gunicorn testDjango.wsgi:application \\
//                    --bind 0.0.0.0:8082 \\
//                    --workers 1 \\
//                    --daemon'''

//         stage 'Publish results'
//             slackSend color: "good", message: "Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        stage('my_stage'){
            steps{
                script{
                    withPythonEnv('/var/lib/jenkins/.local/bin'){
                        sh 'pip install -r requirements.txt'
                        sh 'python3 manage.py runserver 8080'
    }
    }
    }

    catch (err) {
//         slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        throw err
    }

}
