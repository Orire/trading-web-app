# Deployment Guide

Complete guide to deploy the Trading Web App (Frontend, Backend, and Mobile).

## Table of Contents

1. [Frontend (Next.js) - Vercel](#frontend-vercel)
2. [Backend (FastAPI) - Railway/Render](#backend-railwayrender)
3. [Mobile (React Native) - Expo](#mobile-expo)
4. [Environment Variables](#environment-variables)
5. [Post-Deployment Checklist](#post-deployment-checklist)
6. [Isolated VM Deployment (Tenant: TradingAPP_Ri)](#isolated-vm-deployment-tenant-tradingapp_ri)

---

## Frontend (Next.js) - Vercel

### Prerequisites
- GitHub account
- Vercel account (free tier available)

### Steps

1. **Push code to GitHub** (already done ✅)
   ```bash
   # Already pushed to: https://github.com/orire-dev/trading-web-app
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com
   - Click "Add New Project"
   - Import from GitHub: `orire-dev/trading-web-app`
   - Select the repository

3. **Configure Project**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install`

4. **Set Environment Variables**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   NEXT_PUBLIC_WS_URL=wss://your-backend-url.railway.app
   ```

5. **Deploy**
   - Click "Deploy"
   - Vercel will automatically deploy on every push to `main` branch

### Custom Domain (Optional)
- Go to Project Settings → Domains
- Add your custom domain
- Update DNS records as instructed

---

## Backend (FastAPI) - Railway

### Option 1: Railway (Recommended)

#### Prerequisites
- Railway account (free tier available)
- GitHub account

#### Steps

1. **Install Railway CLI** (optional, can use web UI)
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Create New Project**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `orire-dev/trading-web-app`

3. **Configure Service**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   ```
   ETORO_API_KEY=your_api_key
   ETORO_API_SECRET=your_api_secret
   ETORO_BASE_URL=https://api.etoro.com
   PORT=8000
   ```

5. **Deploy**
   - Railway will auto-deploy
   - Get your public URL from the service settings

### Option 2: Render

#### Steps

1. **Create Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repo: `orire-dev/trading-web-app`

3. **Configure**
   - **Name**: `trading-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables** (same as Railway)

5. **Deploy**
   - Click "Create Web Service"
   - Render will deploy automatically

### Option 3: Vercel Serverless Functions

If you want everything on Vercel:

1. **Create API Routes**
   - Move FastAPI routes to `frontend/app/api/` directory
   - Convert to Next.js API routes
   - Use Vercel's serverless functions

2. **Deploy with Frontend**
   - Everything deploys together
   - Note: WebSocket support requires Vercel Pro plan

---

## Mobile (React Native) - Expo

### Prerequisites
- Expo account (free)
- EAS CLI (for building)

### Steps

1. **Install EAS CLI**
   ```bash
   npm install -g eas-cli
   eas login
   ```

2. **Configure EAS**
   ```bash
   cd mobile
   eas build:configure
   ```

3. **Update app.json**
   ```json
   {
     "expo": {
       "extra": {
         "apiUrl": "https://your-backend-url.railway.app",
         "wsUrl": "wss://your-backend-url.railway.app"
       }
     }
   }
   ```

4. **Build for iOS**
   ```bash
   eas build --platform ios
   ```
   - Requires Apple Developer account ($99/year)
   - Or use Expo Go for testing

5. **Build for Android**
   ```bash
   eas build --platform android
   ```
   - Free to build
   - Requires Google Play Developer account ($25 one-time)

6. **Submit to App Stores**
   ```bash
   # iOS
   eas submit --platform ios
   
   # Android
   eas submit --platform android
   ```

### Quick Testing with Expo Go

1. **Start Development Server**
   ```bash
   cd mobile
   npm install
   npx expo start
   ```

2. **Scan QR Code**
   - Install Expo Go app on your phone
   - Scan QR code from terminal
   - App loads on your device

---

## Isolated VM Deployment (Tenant: TradingAPP_Ri)

Use this when deploying on a shared machine where this project must remain isolated.

### Isolation model

- Linux user/group: `tradingapp_ri`
- App root: `/opt/tradingapp-ri`
- Env dir: `/etc/tradingapp-ri`
- Logs: `/var/log/tradingapp-ri`
- Services:
  - `tradingapp-ri-backend.service`
  - `tradingapp-ri-frontend.service`

### Files added in this repo

- `ops/vm/install-tradingapp-ri.sh`
- `ops/vm/deploy-tradingapp-ri.sh`
- `ops/vm/tradingapp-ri-backend.service`
- `ops/vm/tradingapp-ri-frontend.service`
- `ops/vm/nginx-tradingapp-ri.conf`
- `ops/vm/backend.env.example`
- `ops/vm/frontend.env.example`

### Quick steps

```bash
cd /opt/tradingapp-ri/repo
sudo bash ops/vm/install-tradingapp-ri.sh
```

Then create env files in `/etc/tradingapp-ri/` and restart services:

```bash
sudo systemctl restart tradingapp-ri-backend.service tradingapp-ri-frontend.service
```

Use nginx config template in `ops/vm/nginx-tradingapp-ri.conf` for public ingress.

---

## Environment Variables

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_WS_URL=wss://your-backend.railway.app
```

### Backend (.env)
```bash
ETORO_API_KEY=your_api_key_here
ETORO_API_SECRET=your_api_secret_here
ETORO_BASE_URL=https://api.etoro.com
ETORO_ENVIRONMENT=production
```

### Mobile (app.json or .env)
```json
{
  "expo": {
    "extra": {
      "apiUrl": "https://your-backend.railway.app",
      "wsUrl": "wss://your-backend.railway.app"
    }
  }
}
```

---

## Post-Deployment Checklist

### Backend
- [ ] Health check endpoint works: `https://your-backend.railway.app/health`
- [ ] API docs accessible: `https://your-backend.railway.app/docs`
- [ ] WebSocket connection tested
- [ ] CORS configured for frontend domain
- [ ] Environment variables set correctly

### Frontend
- [ ] Site loads: `https://your-app.vercel.app`
- [ ] API calls work (check browser console)
- [ ] WebSocket connects
- [ ] All pages accessible
- [ ] Mobile responsive

### Mobile
- [ ] App builds successfully
- [ ] API connection works
- [ ] WebSocket connects
- [ ] All screens functional
- [ ] Tested on real device

### Security
- [ ] CORS restricted to production domains
- [ ] API keys secured (not in code)
- [ ] HTTPS enabled everywhere
- [ ] Rate limiting configured
- [ ] Authentication implemented (if needed)

---

## Quick Deploy Script

Create a deployment script for easy updates:

```bash
#!/bin/bash
# deploy.sh

echo "🚀 Deploying Trading App..."

# Frontend (Vercel auto-deploys on push)
echo "📦 Pushing to GitHub..."
git push origin main

# Backend (Railway auto-deploys on push)
echo "✅ Backend will auto-deploy on Railway"

# Mobile (manual build)
echo "📱 To build mobile app:"
echo "   cd mobile && eas build --platform all"

echo "✨ Deployment initiated!"
```

---

## Troubleshooting

### Backend Issues

**Problem**: CORS errors
**Solution**: Update `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Problem**: WebSocket not working
**Solution**: 
- Railway: WebSocket supported by default
- Render: Enable WebSocket in service settings
- Vercel: Requires Pro plan for WebSocket

### Frontend Issues

**Problem**: API calls fail
**Solution**: Check `NEXT_PUBLIC_API_URL` is set correctly

**Problem**: Build fails
**Solution**: Check Node.js version (should be 18+)

### Mobile Issues

**Problem**: Can't connect to API
**Solution**: Update `app.json` with correct API URL

**Problem**: Build fails
**Solution**: Check Expo SDK version compatibility

---

## Cost Estimates

### Free Tier (Development)
- **Vercel**: Free (hobby plan)
- **Railway**: $5/month free credit
- **Render**: Free tier available
- **Expo**: Free for development

### Production Costs
- **Vercel Pro**: $20/month (if needed)
- **Railway**: ~$5-20/month (based on usage)
- **Render**: ~$7/month (starter plan)
- **Apple Developer**: $99/year (iOS)
- **Google Play**: $25 one-time (Android)

---

## Next Steps

1. **Deploy Backend First**
   - Get the backend URL
   - Test API endpoints

2. **Deploy Frontend**
   - Use backend URL in environment variables
   - Test full integration

3. **Build Mobile App**
   - Update API URLs
   - Test on device
   - Submit to stores (optional)

4. **Monitor & Optimize**
   - Set up error tracking (Sentry)
   - Add analytics
   - Monitor performance

---

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Expo Docs**: https://docs.expo.dev
- **Project Repo**: https://github.com/orire-dev/trading-web-app
