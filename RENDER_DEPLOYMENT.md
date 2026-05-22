# Render Deployment Guide

## Deploying to Render (Completely Free)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (easiest option)
3. Authorize Render to access your GitHub

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repo: `erichayrapetyanart-art/ASDS_DataVisualisation_Project`
3. Fill in the details:
   - **Name:** `womens-clothing-dashboard` (or any name)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -b 0.0.0.0:$PORT --workers 4 app:server`

### Step 3: Configure Environment
- Leave environment variables blank (not needed for this project)
- Instance Type: **Free** ($0/month)

### Step 4: Deploy
- Click "Create Web Service"
- Render will automatically:
  - Clone your repo
  - Install dependencies from `requirements.txt`
  - Start the app with the Procfile command
  - Assign a public URL

### Step 5: Get Your Live Link
- Dashboard will be accessible at: `https://your-service-name.onrender.com`
- It may take 2-5 minutes for initial deployment
- You'll see a "Live" status when ready

---

## Common Render Settings

### For Best Performance:
- **Memory:** 512 MB (default for free tier)
- **CPU:** Shared (free tier)
- **Restart Policy:** Always (default)

### Monitor Deployment:
- Click "Logs" to see deployment progress
- Look for "Dash is running on" message
- If error, check logs for python/import errors

---

## Troubleshooting Render Deployment

### Issue: "ModuleNotFoundError"
**Solution:** Render installs from requirements.txt. Verify:
```bash
# Locally, check if requirements.txt has all package
source venv/bin/activate
pip freeze | grep -E "dash|plotly|pandas|gunicorn"
```

### Issue: "Cannot find app:server"
**Solution:** Make sure you have this in `app.py`:
```python
server = app.server  # This line exports Flask server for deployment
```
✓ Already done in your code!

### Issue: "Build failed" or "ImportError"
**Solution:** Check Render logs for exact error, then:
1. Fix locally
2. Commit and push to GitHub
3. Render auto-redeploys

### Issue: Dashboard loads but charts don't show
**Solution:** Check browser console (F12 → Console tab) for JavaScript errors

---

## After Deployment

### Your Dashboard Live URLs:
- **Local:** http://localhost:8050 (for testing)
- **Live:** https://your-service-name.onrender.com (for presentation)

### Share with Professor/Class:
Send them the Render URL: `https://your-service-name.onrender.com`

---

## Auto-Redeploy on Push

Render automatically redeploys whenever you push to `main` branch:
```bash
git push origin main
# Render will detect changes and redeploy automatically (2-5 min)
```

---

## Keeping Your Dashboard Running

**Free Tier Notes:**
- Service spins down after 15 mins of inactivity
- First request after spindown takes ~30 seconds to load
- For production, upgrade to paid plan (~$7/month)
- For a class presentation, free tier is perfect

---

## Need to Stop Deployment?

1. Go to Render Dashboard
2. Select your service
3. Click "Suspend" or "Delete"
4. No ongoing charges on free tier

---

## Summary: Deployment Steps

```
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"
4. Select your GitHub repo
5. Set Start Command: gunicorn -b 0.0.0.0:$PORT --workers 4 app:server
6. Click "Create Web Service"
7. Wait 2-5 minutes
8. Get live URL from Render dashboard
9. Share URL before presentation
```

That's it! Your dashboard will be live! 🚀
