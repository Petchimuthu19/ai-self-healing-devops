#!/bin/bash

set -e

IMAGE="your-dockerhub/my-app:latest"
CONTAINER="my-app"
LOG_FILE="/home/ec2-user/deploy.log"

exec > $LOG_FILE 2>&1

echo "🚀 Starting deployment..."

echo "📥 Pulling latest image..."
docker pull $IMAGE

echo "🛑 Stopping old container..."
docker stop $CONTAINER || true
docker rm $CONTAINER || true

echo "🚀 Starting new container with logging..."

docker run -d \
  --name $CONTAINER \
  -p 80:5000 \
  --restart unless-stopped \
  --log-driver=awslogs \
  --log-opt awslogs-region=ap-south-1 \
  --log-opt awslogs-group=/my-app/syslog \
  --log-opt awslogs-stream=my-app-$(date +%s) \
  $IMAGE

echo "⏳ Waiting for container..."
sleep 5

echo "🔍 Checking container status..."
if ! docker ps | grep $CONTAINER > /dev/null; then
    echo "❌ Deployment failed!"
    exit 1
fi

echo "✅ Deployment successful!"
