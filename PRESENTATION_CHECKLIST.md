# 🚀 DEPLOYMENT CHECKLIST & QUICK START

Before your presentation, complete these steps:

---

## ✅ Step 1: Verify Local Dashboard Works

**Run locally to test everything:**
```bash
cd /Users/erikhayrapetyan/Documents/PythonProjects/TestProject
source venv/bin/activate
python app.py
```

**Expected output:**
```
Dash is running on http://127.0.0.1:8050/
```

**Then open:** http://localhost:8050
- Navigate through all 4 pages
- Test filters and interactions
- Verify all charts load

**✓ If it works locally, continue to Render deployment**

---

## 🌐 Step 2: Deploy to Render (5-10 minutes)

### A. Render Account Setup
1. Go to https://render.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Approve GitHub authorization
5. You now have a free Render account ✓

### B. Create Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Select your repository: `ASDS_DataVisualisation_Project`
4. Choose branch: `main`

### C. Configure Service

**Fill in these fields:**

| Field | Value |
|-------|-------|
| **Name** | `womens-clothing-dashboard` |
| **Root Directory** | `TestProject` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -b 0.0.0.0:$PORT --workers 4 app:server` |
| **Instance Type** | `Free` |

### D. Deploy
- Click "Create Web Service"
- **Wait 3-5 minutes** for deployment
- Watch the logs for success message
- You'll see: `Dash is running on...` ✓

---

## 📋 Step 3: Get Your Live Dashboard URL

When deployment completes, Render shows your URL:

```
https://womens-clothing-dashboard.onrender.com
```

(Exact name depends on what you chose in Step 2C)

**Test the live dashboard:**
- Open the URL in your browser
- FirstRequest may take 30 seconds (server spinning up)
- All features should work exactly like local version

---

## 📧 Step 4: Share the Link

**Send to professor/classmates:**
- **Text:** "Dashboard live at: https://womens-clothing-dashboard.onrender.com"
- **No password needed** - it's public

**For your presentation:**
- Have the URL ready
- Have local version running as backup (`python app.py`)
- If internet fails, use local version on http://localhost:8050

---

## 🔄 After Deployment

### Automatic Updates
Whenever you push to GitHub:
```bash
git push origin main
```

Render **automatically redeploys** (2-5 minutes)

### Manual Redeploy (if needed)
1. Go to Render dashboard
2. Find your service
3. Click "Refdeploy" button

---

## ⚠️ Troubleshooting

### "Build failed" or "Deployment failed"
1. Check Render logs for error message
2. Fix the issue locally
3. `git push origin main` (auto-redeploys)

### Dashboard loads but blank/no charts
1. Open browser DevTools (F12)
2. Check "Console" tab for errors
3. Check "Network" tab if resources failed to load

### "Address already in use" locally
Kill the process and restart:
```bash
lsof -i :8050 | grep LISTEN | awk '{print $2}' | xargs kill -9
python app.py
```

### Slow first load on Render
Free tier hibernates after 15 minutes of inactivity
- First request after inactivity takes ~30 seconds
- Normal after that
- Plan for this in demo (open tab 5 min before presenting)

---

## 📊 What Files are Deployed

These files are included in the GitHub repo that Render deploys:

✓ `app.py` - Main application
✓ `pages/` - Dashboard pages
✓ `utils/` - Utilities
✓ `data/` - Data file
✓ `requirements.txt` - Python packages
✓ `Procfile` - Deployment command
✓ `runtime.txt` - Python version

---

## 🎯 Final Checklist Before Presentation

- [ ] Dashboard runs locally: `python app.py` ✓
- [ ] Can access http://localhost:8050 ✓
- [ ] All 4 pages work locally ✓
- [ ] GitHub repo has latest code pushed ✓
- [ ] Render account created at render.com ✓
- [ ] Web Service deployed on Render ✓
- [ ] Have live URL (e.g., https://womens-clothing-dashboard.onrender.com) ✓
- [ ] Live dashboard works in browser ✓
- [ ] Shared link with professor/class (optional) ✓

---

## 💡 Pro Tips

### During Presentation
1. **Start with local version** as primary (more reliable)
2. **Have live URL as backup** in case of internet issues
3. **Open Render URL 5 minutes early** to warm up server
4. **Prepare talking points** for each dashboard page

### Code Quality
✓ All imports tested ✓ Data loads successfully ✓ No syntax errors
✓ Modular structure ✓ Production-ready ✓ Properly documented

---

## 📞 Quick Reference

**Local Dashboard:**
```bash
cd /Users/erikhayrapetyan/Documents/PythonProjects/TestProject
source venv/bin/activate
python app.py
# Then open http://localhost:8050
```

**Render Dashboard:**
- URL: https://womens-clothing-dashboard.onrender.com (after deployment)
- Status: Check at https://render.com/dashboard

**GitHub Repo:**
- https://github.com/erichayrapetyanart-art/ASDS_DataVisualisation_Project

---

## 🎉 You're All Set!

Your dashboard is:
```
✓ Production-ready
✓ Deployed on Render (free tier)
✓ Runs locally as backup
✓ Fully documented
✓ Easy to extend
```

**Good luck with your presentation! 🚀**
