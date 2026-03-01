#!/bin/bash
# Quick deployment script

set -e

echo "🚀 Trading App Deployment Script"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ Error: Please run this script from the project root"
    exit 1
fi

echo -e "${BLUE}📋 Deployment Checklist:${NC}"
echo ""
echo "1. Frontend (Next.js) → Vercel"
echo "   - Push to GitHub (auto-deploys)"
echo ""
echo "2. Backend (FastAPI) → Railway/Render"
echo "   - Configure in Railway/Render dashboard"
echo ""
echo "3. Mobile (React Native) → Expo"
echo "   - Build with: cd mobile && eas build"
echo ""

read -p "Do you want to push to GitHub now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}📦 Pushing to GitHub...${NC}"
    git add .
    git commit -m "Deployment updates" || true
    git push origin main
    echo -e "${GREEN}✅ Pushed to GitHub${NC}"
    echo ""
    echo "Vercel will auto-deploy the frontend"
    echo "Railway/Render will auto-deploy the backend"
fi

echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo ""
echo "1. Frontend (Vercel):"
echo "   - Go to: https://vercel.com"
echo "   - Import repo: orire-dev/trading-web-app"
echo "   - Set root: frontend"
echo "   - Add env vars: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_WS_URL"
echo ""
echo "2. Backend (Railway):"
echo "   - Go to: https://railway.app"
echo "   - New project from GitHub"
echo "   - Set root: backend"
echo "   - Add env vars: ETORO_API_KEY, ETORO_API_SECRET, etc."
echo ""
echo "3. Mobile (Expo):"
echo "   - cd mobile"
echo "   - npm install"
echo "   - eas build:configure"
echo "   - eas build --platform all"
echo ""
echo -e "${GREEN}✨ Deployment guide: See DEPLOYMENT.md${NC}"
