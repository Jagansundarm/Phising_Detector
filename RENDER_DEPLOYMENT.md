# 🚀 Render Deployment Guide (Both Frontend & Backend)

This guide will help you deploy both your frontend and backend on Render.

---

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Render account (sign up at [render.com](https://render.com))
- ✅ Your code pushed to GitHub

---

## 🔧 Step 1: Deploy Backend to Render

### 1.1 Prepare Backend

Your backend is already configured! Just ensure these files exist:
- ✅ `backend/requirements.txt`
- ✅ `backend/app/main.py`
- ✅ `backend/models/phishing_model.pkl`

### 1.2 Create Web Service on Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Click "New +" → "Web Service"**

3. **Connect Your GitHub Repository**
   - Authorize Render to access your GitHub
   - Select your `Phising_Detector` repository

4. **Configure the Backend Service:**

   | Setting | Value |
   |---------|-------|
   | **Name** | `phishing-detection-backend` (or your choice) |
   | **Region** | Choose closest to you |
   | **Branch** | `main` |
   | **Root Directory** | `backend` |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | **Instance Type** | `Free` |

5. **Environment Variables** (Optional - click "Advanced")
   
   Add these if needed:
   ```
   PORT = 8000
   LOG_LEVEL = info
   ```

6. **Click "Create Web Service"**

7. **Wait for Deployment** (3-5 minutes)
   - Watch the logs for any errors
   - Once deployed, you'll get a URL like: `https://phishing-detection-backend.onrender.com`

### 1.3 Test Your Backend

Open your browser or use curl:
```bash
https://your-backend-name.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "API is operational",
  "version": "2.0.0",
  "model_loaded": true
}
```

**🎉 Backend is now live! Copy this URL for the next step.**

---

## 🌐 Step 2: Deploy Frontend to Render

### 2.1 Update Frontend Configuration

1. **Create `.env.production` in the `frontend/` folder:**

```env
VITE_API_URL=https://your-backend-name.onrender.com
```

Replace `your-backend-name` with your actual backend URL from Step 1.

2. **Commit and push this file:**

```bash
git add frontend/.env.production
git commit -m "Add production environment variables"
git push origin main
```

### 2.2 Create Static Site on Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Click "New +" → "Static Site"**

3. **Select Your Repository**

4. **Configure the Frontend Service:**

   | Setting | Value |
   |---------|-------|
   | **Name** | `phishing-detection-frontend` (or your choice) |
   | **Branch** | `main` |
   | **Root Directory** | `frontend` |
   | **Build Command** | `npm install && npm run build` |
   | **Publish Directory** | `dist` |

5. **Environment Variables** (Click "Advanced")
   
   Add:
   ```
   VITE_API_URL = https://your-backend-name.onrender.com
   ```
   
   Replace with your actual backend URL!

6. **Click "Create Static Site"**

7. **Wait for Deployment** (2-3 minutes)
   - You'll get a URL like: `https://phishing-detection-frontend.onrender.com`

### 2.3 Test Your Frontend

1. Open the frontend URL in your browser
2. Try scanning a URL
3. Verify it connects to your backend

**🎉 Frontend is now live!**

---

## ✅ Post-Deployment Checklist

- [ ] Backend health check passes: `https://your-backend.onrender.com/health`
- [ ] Frontend loads correctly
- [ ] Can scan URLs and get results
- [ ] No CORS errors in browser console
- [ ] Both services show "Active" in Render dashboard

---

## 🔄 Auto-Deployment

Both services will automatically redeploy when you push to GitHub:
- Push to `main` branch → Automatic deployment
- Check deployment status in Render dashboard

---

## 🐛 Troubleshooting

### Backend Issues

**Problem: Model file not found**
```
Error: FileNotFoundError: models/phishing_model.pkl
```

**Solution:**
Ensure `backend/models/phishing_model.pkl` is committed to Git:
```bash
git add backend/models/phishing_model.pkl
git commit -m "Add model file"
git push
```

**Problem: Build fails**

Check Render logs:
1. Go to your service in Render dashboard
2. Click "Logs" tab
3. Look for error messages

Common fixes:
- Update `requirements.txt` versions
- Ensure Python 3.9+ compatibility

### Frontend Issues

**Problem: API connection fails (CORS error)**

**Solution:**
1. Check backend CORS settings in `backend/app/main.py`
2. Verify `VITE_API_URL` is set correctly
3. Ensure backend URL doesn't have trailing slash

**Problem: Environment variable not working**

**Solution:**
1. Go to Render dashboard → Your static site → Environment
2. Verify `VITE_API_URL` is set
3. Trigger manual redeploy

**Problem: 404 on routes**

**Solution:**
Add `vercel.json` or configure Render redirects for SPA routing.

---

## 💰 Cost

| Service | Plan | Cost |
|---------|------|------|
| Backend (Web Service) | Free | $0/month |
| Frontend (Static Site) | Free | $0/month |
| **Total** | | **$0/month** |

**Free Tier Limits:**
- Backend: 750 hours/month (always on)
- Frontend: 100 GB bandwidth/month
- Auto-sleep after 15 min inactivity (free tier)

**Note:** Free tier backend may sleep after inactivity. First request after sleep takes ~30 seconds to wake up.

---

## 🚀 Upgrade Options (Optional)

If you need better performance:

### Paid Plans ($7/month per service)
- No auto-sleep
- Faster builds
- More resources
- Custom domains

---

## 📊 Monitoring

### View Logs

**Backend:**
```
Render Dashboard → phishing-detection-backend → Logs
```

**Frontend:**
```
Render Dashboard → phishing-detection-frontend → Logs
```

### Check Status

Both services show status in dashboard:
- 🟢 Active
- 🟡 Building
- 🔴 Failed

---

## 🔐 Security Recommendations

Before sharing publicly:

1. **Add Rate Limiting** to backend
2. **Implement API Keys** for production
3. **Enable HTTPS** (automatic on Render)
4. **Add Input Validation**
5. **Monitor Usage** via Render analytics

---

## 📝 Environment Variables Reference

### Backend (.env)
```env
PORT=8000
HOST=0.0.0.0
MODEL_PATH=models/phishing_model.pkl
LOG_LEVEL=info
ALLOWED_ORIGINS=*
```

### Frontend (.env.production)
```env
VITE_API_URL=https://your-backend-name.onrender.com
```

---

## 🎯 Next Steps

After deployment:

1. **Test thoroughly** with various URLs
2. **Share your app** with others
3. **Monitor logs** for errors
4. **Add to portfolio** with live demo link
5. **Consider custom domain** (optional)

---

## 📞 Support

If deployment fails:

1. **Check Render logs** for specific errors
2. **Verify all files** are in Git repository
3. **Test locally** first: `npm run dev` / `uvicorn app.main:app`
4. **Render Community**: [community.render.com](https://community.render.com)

---

**🎉 Congratulations! Your phishing detection system is now live on Render!**

**Your Live URLs:**
- Backend API: `https://your-backend-name.onrender.com`
- Frontend App: `https://your-frontend-name.onrender.com`
