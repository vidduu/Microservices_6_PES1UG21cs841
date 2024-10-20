pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the GitHub repository
                 git branch: 'main', url: 'https://github.com/vidduu/PES1UG21CS841_Jenkins'
                bat 'echo "Hello, git completed"'
                bat 'dir'
            }
        }
        stage('Deploy nginx') {
            steps {
                // Deploy nginx using kubectl
                bat 'kubectl apply -f nginx-deployment.yaml' 
                bat 'kubectl apply -f nginx-service.yaml'
            }
        }
        stage('Build and Deploy Microservices') {
            steps {
                // Build Docker images for each microservice
                dir('users-microservice'){
                   bat 'docker build -t users-microservice:4 .'
                    bat 'kubectl apply -f nginx-deployment-orders.yaml'
                    bat 'kubectl apply -f nginx-service-orders.yaml'
                    sleep time: 60, unit: 'SECONDS'
                }

                dir('products-microservice'){
                    bat 'docker build -t products-microservice:3 .'
                    bat 'kubectl apply -f nginx-deployment-products.yaml'
                    bat 'kubectl apply -f nginx-service-products.yaml'
                    sleep time: 60, unit: 'SECONDS'

                }

                dir('orders-microservice'){
                    bat 'docker build -t orders-microservice:3 .'
                    bat 'kubectl apply -f nginx-deployment-orders.yaml'
                    bat 'kubectl apply -f nginx-service-orders.yaml'
                    sleep time: 60, unit: 'SECONDS'
                }            
            }
        }
//         stage('Port Forwarding') {
//             steps {
//                 // Port forward each microservice for local testing
//                 bat 'kubectl port-forward services/users-microservice 7070:7070'
//                 bat 'kubectl port-forward services/products-microservice 8080:8080'
//                 bat 'kubectl port-forward services/orders-microservice 9090:9090'
//             }
//         }
//         stage('Port Forwarding') {
            
//                 // Run steps in parallel within the same stage
//                 parallel {
//                     stage('Port 7070') {
//                         steps {
//                             // Run step 1sleep time: 300, unit: 'SECONDS'
//                             bat 'kubectl port-forward services/users-microservice 7070:7070'
//                         }
//                     }
//                     stage('Port 8080') {
//                         steps {
//                             // Run step 2
//                             bat 'kubectl port-forward services/products-microservice 8080:8080'
//                         }
//                     }
//                     stage('Port 9090') {
//                         steps {
//                             // Run step 3
//                             bat 'kubectl port-forward services/orders-microservice 9090:9090'
//                         }
//                     }
//                 }
            
//         }
    }

//     post {
//         always {
//             // Clean up port forwarding processes
//             bat 'pkill -f "kubectl port-forward"'
//         }
//     }
}