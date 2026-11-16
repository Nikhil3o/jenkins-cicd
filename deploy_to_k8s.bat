@echo off
echo ========================================================
echo  Deploying Application to Kubernetes...
echo ========================================================
kubectl apply -f k8s/deployment-local.yaml
kubectl apply -f k8s/service.yaml
echo.
echo Waiting for pods to roll out...
kubectl rollout status deployment/flask-k8s-deployment --timeout=60s
echo.
echo ========================================================
echo  Pods Status:
kubectl get pods -l app=flask-k8s-app
echo.
echo  Service Status:
kubectl get svc flask-k8s-service
echo ========================================================
echo.
echo Forwarding port 8080 to service...
echo Open your browser at: http://localhost:8080
kubectl port-forward svc/flask-k8s-service 8080:8080
pause
