# 🚀 RENDER DEPLOYMENT - STEP BY STEP

You signed up! Now follow these exact steps:

---

## Step 1: Click "New +" Button

1. On Render dashboard, click the **"New +"** button in the top right
2. A dropdown menu appears
3. Click **"Web Service"**

---

## Step 2: Connect Your GitHub Repo

When the page loads:

1. **Under "Connect a repository"**
   - If you see a search box, search for: `ASDS_DataVisualisation_Project`
   - If you see GitHub repos listed, find: `ASDS_DataVisualisation_Project`

2. Click **"Connect"** next to your repo

✓ Render now has access to your GitHub

---

## Step 3: Fill in the Configuration Form

You'll see a form. Fill in **EXACTLY** as shown:

### Service Name
```
womens-clothing-dashboard
```

### Root Directory
```
TestProject
```
(This tells Render where your app is in the repo)

### Runtime
```
Python 3
```
(Should auto-select)

### Region
```
Oregon (or your closest region)
```

### Branch
```
main
```
(Should auto-select)

### Build Command
```
pip install -r requirements.txt
```
(Copy exactly)

### Start Command
```
gunicorn -b 0.0.0.0:$PORT --workers 4 app:server
```
(Copy exactly - this is critical!)

### Environment Variables
```
(Leave BLANK - skip this)
```

### Instance Type
```
Free
```
(To keep it $0/month)

---

## Step 4: Click "Create Web Service"

1. Click the **"Create Web Service"** button at the bottom
2. Render now starts deploying your app
3. You'll see logs appearing in real-time

---

## Step 5: Wait for Deployment to Complete

**In the logs, look for:**

```
⠙ Building...
⠋ Running build command: pip install -r requirements.txt
...
✓ Build successful
✓ Starting service...
Dash is running on http://127.0.0.1:8050
```

**Total wait time: 3-5 minutes**

---

## Step 6: Get Your Live Dashboard URL

Once deployment completes:

1. At the top of the page, Render shows your **live URL**
2. It looks like: `https://womens-clothing-dashboard.onrender.com`
3. Copy this URL

---

## Step 7: Test Your Live Dashboard

1. **Open the URL in a new browser tab**
2. **First load takes ~30 seconds** (server warming up - normal!)
3. **You should see your dashboard**
4. Test all 4 pages:
   - Overview
   - Customer Behavior
   - Product Insights
   - Correlations & Trends
5. Test filters and interactions

✓ If everything works - **you're done!**

---

## ✅ Success Indicators

- [ ] See "Live" badge in Render dashboard (green checkmark)
- [ ] Dashboard loads at the Render URL
- [ ] All pages work
- [ ] Filters/interactions work
- [ ] Charts display correctly

---

## 🔗 SAVE YOUR LIVE URL

Your dashboard is now live at:

```
https://womens-clothing-dashboard.onrender.com
```

**Share this URL with:**
- Your professor
- Classmates
- Anyone who wants to see your project

**They can just click and view - no installation needed!**

---

## 🎯 Next Checklist

- [ ] Signed up to Render ✓
- [ ] Connected GitHub repo
- [ ] Created Web Service
- [ ] Deployment completed
- [ ] Tested live dashboard
- [ ] Have your live URL saved
- [ ] Ready for presentation!

---

## ⚠️ If Something Goes Wrong

### Logs Show Error Like "ModuleNotFoundError"
1. Check the error message in the logs
2. It's probably in the requirements.txt or imports
3. Fix it locally and push to GitHub:
   ```bash
   git push origin main
   ```
4. Render auto-redeploys (2-5 minutes)

### Dashboard Won't Load / Blank Page
1. Open DevTools (F12)
2. Check the Network tab
3. Check the Console tab for errors
4. Wait 30 seconds (first load can be slow)

### Still Having Issues?
1. Check `RENDER_DEPLOYMENT.md` in your repo for troubleshooting
2. Check Render logs for exact error message

---

## 💡 Pro Tips

1. **First request is slow** (30 sec) - this is normal
2. **After 15 mins inactivity, server hibernates** - that's why it's slow on first request
3. **Auto-redeploys on push** - any GitHub push redeploys automatically
4. **Monitor with Render Dashboard** - you can always check status there
5. **Free tier is perfect for projects** - no credit card needed, $0/month

---

## 🎉 You're Now Live!

Your dashboard is deployed and accessible to anyone with the link!

**Next: Share your URL for the presentation!**

---

## 📞 Quick Reference

**To check deployment status:**
- Go to https://render.com/dashboard
- Find your "womens-clothing-dashboard" service
- See the status and logs there

**To redeploy manually:**
1. Go to Render dashboard
2. Find your service
3. Click "Manual Deploy" → "Deploy Latest"

**Every time you push to GitHub:**
```bash
git push origin main
```
Render automatically redeploys in 2-5 minutes!

---

**Let me know once you see "Live" status and have the URL!** 🚀
