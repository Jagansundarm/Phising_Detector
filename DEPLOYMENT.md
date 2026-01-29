# 🚀 Deployment Guide

## Quick Deployment Checklist

### ✅ Prerequisites
- [ ] GitHub account
- [ ] Render account (free tier)
- [ ] Vercel account (free tier)
- [ ] Code pushed to GitHub repository

---

## 📦 Backend Deployment (Render)

### Step 1: Prepare Repository

Ensure your repository has:
- `backend/` folder with all files
- `backend/requirements.txt`
- `backend/app/` folder
- `backend/models/phishing_model.pkl`

### Step 2: Deploy to Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Click "New +" → "Web Service"**

3. **Connect GitHub Repository**
   - Select your repository
   - Root directory: `backend`

4. **Configure Service:**
   ```
   Name: phishing-detection-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Click "Create Web Service"**

6. **Wait for deployment** (2-3 minutes)

7. **Your API is live!** 
   - URL: `https://phishing-detection-api.onrender.com`
   - Test: `https://your-app.onrender.com/health`

### Step 3: Test Deployed API

```bash
curl https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "API is operational",
  "version": "1.0.0"
}
```

---

## 🌐 Frontend Deployment (Vercel)

### Step 1: Update API URL

Create `.env.production` in `frontend/`:

```env
VITE_API_URL=https://your-app.onrender.com
```

### Step 2: Deploy to Vercel

**Option A: Vercel CLI**

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

**Option B: Vercel Dashboard**

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```
5. Add Environment Variable:
   ```
   VITE_API_URL = https://your-backend.onrender.com
   ```
6. Click "Deploy"

### Step 3: Access Your App

Your frontend will be live at:
```
https://your-project.vercel.app
```

---

## 🐳 Docker Deployment (Alternative)

### Build and Run Locally

```bash
# Backend
cd backend
docker build -t phishing-api .
docker run -p 8000:8000 phishing-api

# Frontend (create Dockerfile first)
cd frontend
docker build -t phishing-frontend .
docker run -p 3000:80 phishing-frontend
```

### Deploy to Cloud

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Fly.io:**
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

---

## 🔧 Environment Variables

### Backend (.env)
```env
# Optional
MODEL_PATH=models/phishing_model.pkl
LOG_LEVEL=info
```

### Frontend (.env.production)
```env
VITE_API_URL=https://your-backend.onrender.com
```

---

## ✅ Post-Deployment Checklist

- [ ] Backend health check passes
- [ ] Frontend loads correctly
- [ ] API connection works
- [ ] URL scanning functions
- [ ] Results display properly
- [ ] History saves correctly
- [ ] Mobile responsive
- [ ] HTTPS enabled

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Model file not found
```bash
# Solution: Ensure model is in backend/models/
cp ml_engine/models/phishing_model.pkl backend/models/
```

**Problem:** Dependencies fail
```bash
# Solution: Update requirements.txt versions
pip freeze > requirements.txt
```

### Frontend Issues

**Problem:** API connection fails
```bash
# Solution: Check CORS settings in backend/app/main.py
# Ensure your frontend URL is in allow_origins
```

**Problem:** Build fails
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 📊 Monitoring

### Render Logs
```
Dashboard → Your Service → Logs
```

### Vercel Logs
```
Dashboard → Your Project → Deployments → View Function Logs
```

---

## 🔄 Continuous Deployment

### Auto-deploy on Git Push

**Render:**
- Automatically enabled when connected to GitHub
- Push to main branch → auto-deploys

**Vercel:**
- Automatically enabled
- Push to any branch → preview deployment
- Push to main → production deployment

---

## 💰 Cost Estimate

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Render** | ✅ Yes | 750 hours/month |
| **Vercel** | ✅ Yes | 100 GB bandwidth |
| **Total** | **$0/month** | Sufficient for portfolio |

---

## 🎯 Production Recommendations

### Before Going Live:

1. **Security**
   - [ ] Add rate limiting
   - [ ] Implement API keys
   - [ ] Enable HTTPS only
   - [ ] Add input sanitization

2. **Performance**
   - [ ] Enable caching
   - [ ] Add CDN for frontend
   - [ ] Optimize model size
   - [ ] Add database for history

3. **Monitoring**
   - [ ] Set up error tracking (Sentry)
   - [ ] Add analytics (Google Analytics)
   - [ ] Monitor API usage
   - [ ] Set up alerts

4. **Scaling**
   - [ ] Consider Redis for caching
   - [ ] Add load balancer
   - [ ] Use managed database
   - [ ] Implement queue system

---

## 📞 Support

If deployment fails:
1. Check logs in Render/Vercel dashboard
2. Verify all files are committed to Git
3. Ensure environment variables are set
4. Test locally first

---

**🎉 Congratulations! Your app is now live and accessible worldwide!**
