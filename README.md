# Trading Web Interface - "Trading for Dummies"

A beginner-friendly web application for eToro trading with educational content, real-time market data, trading signals, and goal-based strategy building.

## Features

- 📊 **Real-time Dashboard**: Monitor positions, signals, and performance
- 🎯 **Goal-Based Trading**: Set targets (e.g., "Make $1000 from $500 in 20 days") and get recommendations
- 📚 **Educational Hub**: Learn trading basics, indicators, and strategies
- 📈 **Market Explorer**: Browse instruments and view detailed market data
- 💡 **AI-Powered Advice**: Get personalized recommendations
- 🔔 **Real-time Updates**: WebSocket support for live data

## Tech Stack

### Frontend
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Recharts for visualizations
- Socket.IO client for real-time updates

### Backend
- FastAPI
- Python 3.9+
- WebSocket support
- Integration with eToro trading bot

## Project Structure

```
trading-web-app/
├── frontend/          # Next.js frontend application
├── backend/           # FastAPI backend
└── shared/            # Shared TypeScript types
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+
- eToro API credentials (optional for development)

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

The backend API will be available at `http://localhost:8000`

### Environment Variables

Create `.env` files in both `frontend/` and `backend/` directories:

**frontend/.env:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=http://localhost:8000
```

**backend/.env:**
```
ETORO_API_KEY=your_api_key_here
ETORO_API_SECRET=your_api_secret_here
ETORO_BASE_URL=https://api.etoro.com
```

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Vercel will auto-detect Next.js
3. Set environment variables in Vercel dashboard
4. Deploy automatically on push

### Backend (Railway/Render)

1. Connect your GitHub repository
2. Set environment variables
3. Deploy FastAPI application
4. Configure WebSocket support

### Isolated Azure VM (single-tenant)

This repo includes isolated VM deployment assets under `ops/vm/`.

- Uses dedicated tenant paths/service names:
  - `/opt/tradingapp-ri`
  - `/etc/tradingapp-ri`
  - `tradingapp-ri-backend.service`
  - `tradingapp-ri-frontend.service`
- Does not share runtime paths with any other project on the same machine.

See `ops/vm/README.md` for full setup.

## API Documentation

Once the backend is running, visit:
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## License

MIT
