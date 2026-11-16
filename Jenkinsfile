pipeline {
    agent any

    environment {
        // Change to your Docker Hub username and repository name
        DOCKER_HUB_USER         = 'nikhilchowdary'
        IMAGE_NAME              = 'flask-k8s-app'
        IMAGE_TAG               = "${env.BUILD_NUMBER}"
        DOCKER_IMAGE            = "${DOCKER_HUB_USER}/${IMAGE_NAME}"

        // Jenkins Credentials IDs configured in Jenkins -> Manage Credentials
        DOCKER_HUB_CREDENTIALS  = 'dockerhub-credentials' // Username & Password credentials
        KUBECONFIG_CREDENTIALS  = 'k8s-kubeconfig'         // Secret file credentials for kubeconfig
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo '=== Stage 1: Checking out source code ==='
                checkout scm
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo '=== Stage 2: Running Unit Tests ==='
                // Use python/pytest to validate application logic before containerizing
                sh '''
                    python3 -m venv venv || python -m venv venv
                    . venv/bin/activate || . venv/Scripts/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest test_app.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "=== Stage 3: Building Docker Image: ${DOCKER_IMAGE}:${IMAGE_TAG} ==="
                sh """
                    docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .
                    docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                echo '=== Stage 4: Pushing Docker Image to Registry ==='
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_HUB_CREDENTIALS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    """
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo '=== Stage 5: Deploying Application to Kubernetes Cluster ==='
                // Uses Kubeconfig credentials or local cluster config
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS}", variable: 'KUBECONFIG')]) {
                    sh """
                        # Substitute image placeholders with current build tag
                        sed -i "s|REPLACE_IMAGE_NAME:REPLACE_IMAGE_TAG|${DOCKER_IMAGE}:${IMAGE_TAG}|g" k8s/deployment.yaml

                        # Apply Kubernetes manifests
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                    """
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '=== Stage 6: Verifying Deployment Rollout ==='
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS}", variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl rollout status deployment/flask-k8s-deployment --timeout=120s
                        kubectl get pods -l app=flask-k8s-app
                        kubectl get svc flask-k8s-service
                    """
                }
            }
        }
    }

    post {
        always {
            echo '=== Cleaning up workspace and temporary resources ==='
            cleanWs()
        }
        success {
            echo "Pipeline succeeded! Application deployed successfully at version ${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed! Please inspect logs above for troubleshooting."
        }
    }
}
