node {

    try {
//         stage 'Checkout'
//             checkout scm

//             sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
//             def lastChanges = readFile('GIT_CHANGES')
//             slackSend color: "warning", message: "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges}"

        stage 'Test'
            sh 'virtualenv env -p python3.9'
            sh '. env/bin/activate'
            sh 'env/bin/pip install -r requirements.txt'
//             sh 'env/bin/python3.9 manage.py test --testrunner=djtrump.tests.test_runners.NoDbTestRunner'

        stage 'Deploy'
//             sh './deployment/deploy_prod.sh'
//             sh 'pip3 install django'
//             sh 'python3 manage.py runserver 8080'
               sh '''gunicorn testDjango.wsgi:application \\
                   --bind 0.0.0.0:8082 \\
                   --workers 1 \\
                   --daemon'''

//         stage 'Publish results'
//             slackSend color: "good", message: "Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
    }

    catch (err) {
//         slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        throw err
    }

}
