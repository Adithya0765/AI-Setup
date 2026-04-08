#!/bin/bash
# AWS EC2 Instance Manager
# Helps you start/stop/check your instance from local machine

# Configuration - UPDATE THESE
INSTANCE_ID="i-xxxxxxxxxxxxx"  # Your instance ID from AWS console
KEY_PATH="marketing-ai-key.pem"  # Path to your SSH key
REGION="us-east-1"  # Your AWS region

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to get instance status
get_status() {
    aws ec2 describe-instances \
        --instance-ids $INSTANCE_ID \
        --region $REGION \
        --query 'Reservations[0].Instances[0].State.Name' \
        --output text
}

# Function to get instance IP
get_ip() {
    aws ec2 describe-instances \
        --instance-ids $INSTANCE_ID \
        --region $REGION \
        --query 'Reservations[0].Instances[0].PublicIpAddress' \
        --output text
}

# Function to start instance
start_instance() {
    echo -e "${YELLOW}Starting instance...${NC}"
    aws ec2 start-instances --instance-ids $INSTANCE_ID --region $REGION
    
    echo "Waiting for instance to start..."
    aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION
    
    IP=$(get_ip)
    echo -e "${GREEN}Instance started!${NC}"
    echo -e "IP: ${GREEN}$IP${NC}"
    echo -e "Connect: ${GREEN}ssh -i $KEY_PATH ubuntu@$IP${NC}"
}

# Function to stop instance
stop_instance() {
    echo -e "${YELLOW}Stopping instance...${NC}"
    aws ec2 stop-instances --instance-ids $INSTANCE_ID --region $REGION
    
    echo "Waiting for instance to stop..."
    aws ec2 wait instance-stopped --instance-ids $INSTANCE_ID --region $REGION
    
    echo -e "${GREEN}Instance stopped! No more charges.${NC}"
}

# Function to check status
check_status() {
    STATUS=$(get_status)
    IP=$(get_ip)
    
    echo -e "Instance ID: ${YELLOW}$INSTANCE_ID${NC}"
    echo -e "Status: ${YELLOW}$STATUS${NC}"
    
    if [ "$STATUS" = "running" ]; then
        echo -e "IP: ${GREEN}$IP${NC}"
        echo -e "Connect: ${GREEN}ssh -i $KEY_PATH ubuntu@$IP${NC}"
    fi
}

# Function to connect via SSH
connect_ssh() {
    STATUS=$(get_status)
    
    if [ "$STATUS" != "running" ]; then
        echo -e "${RED}Instance is not running. Start it first.${NC}"
        exit 1
    fi
    
    IP=$(get_ip)
    echo -e "${GREEN}Connecting to $IP...${NC}"
    ssh -i $KEY_PATH ubuntu@$IP
}

# Function to get cost estimate
cost_estimate() {
    # Get instance uptime
    START_TIME=$(aws ec2 describe-instances \
        --instance-ids $INSTANCE_ID \
        --region $REGION \
        --query 'Reservations[0].Instances[0].LaunchTime' \
        --output text)
    
    echo -e "${YELLOW}Cost Estimate (g5.xlarge spot @ $0.35/hour):${NC}"
    echo "Note: Check AWS Billing Dashboard for actual costs"
}

# Main menu
case "$1" in
    start)
        start_instance
        ;;
    stop)
        stop_instance
        ;;
    status)
        check_status
        ;;
    connect)
        connect_ssh
        ;;
    cost)
        cost_estimate
        ;;
    *)
        echo "AWS EC2 Instance Manager"
        echo ""
        echo "Usage: $0 {start|stop|status|connect|cost}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the EC2 instance"
        echo "  stop    - Stop the EC2 instance (IMPORTANT: saves money!)"
        echo "  status  - Check instance status"
        echo "  connect - SSH into the instance"
        echo "  cost    - Estimate costs"
        echo ""
        echo "Before using, update INSTANCE_ID in this script!"
        exit 1
        ;;
esac
