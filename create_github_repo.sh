#!/bin/bash
# Script to create GitHub repository and push code

REPO_NAME="trading-web-app"
DESCRIPTION="Trading for Dummies - Beginner-friendly eToro trading web interface"

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "Using GitHub CLI..."
    gh repo create "$REPO_NAME" --public --description "$DESCRIPTION" --source=. --remote=origin --push
else
    echo "GitHub CLI not found. Please create the repository manually:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Description: $DESCRIPTION"
    echo "4. Choose Public or Private"
    echo "5. DO NOT initialize with README, .gitignore, or license"
    echo "6. Click 'Create repository'"
    echo ""
    echo "Then run these commands:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
fi
