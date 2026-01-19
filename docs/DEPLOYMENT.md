# Deploying to the Internet (Free & Easy!)

This guide will help you deploy your Immigration Advisory System so anyone can access it with a simple link - no login required!

## What You'll Get

- **Frontend URL**: `https://your-app.vercel.app` (shareable with anyone)
- **Backend API**: Automatically hosted and connected
- **Cost**: 100% FREE for moderate family use
- **Setup Time**: ~10 minutes

---

## Option 1: Deploy to Vercel + Railway (RECOMMENDED - Easiest)

### Step 1: Deploy Frontend to Vercel

1. **Create a Vercel account** (free):
   - Go to https://vercel.com/signup
   - Sign up with your GitHub account

2. **Import your project**:
   - Click "Add New..." → "Project"
   - Select "Import Git Repository"
   - Choose `ImmigrationClaude`
   - **Important**: Set "Root Directory" to `frontend`

3. **Configure build settings**:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Add environment variable**:
   - Click "Environment Variables"
   - Name: `VITE_API_URL`
   - Value: (we'll add this after deploying backend - use `https://PLACEHOLDER` for now)
   - Click "Deploy"

5. **Copy your URL**: After deployment, copy the URL (like `https://immigration-advisory-xyz.vercel.app`)

### Step 2: Deploy Backend to Railway

1. **Create a Railway account** (free):
   - Go to https://railway.app/
   - Sign in with GitHub

2. **Create new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `ImmigrationClaude`
   - Railway will detect it's a Python app

3. **Configure the service**:
   - Click on the deployed service
   - Go to "Settings" → "Root Directory"
   - Set to: `backend`
   - Click "Save"

4. **Add environment variables**:
   - Go to "Variables" tab
   - Add these variables:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     ENVIRONMENT=production
     DEBUG=false
     CORS_ORIGINS=https://your-vercel-url.vercel.app
     ```
   - Replace with your actual Anthropic API key and Vercel URL

5. **Generate domain**:
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - Copy the URL (like `https://immigrationclaude-production.up.railway.app`)

### Step 3: Connect Frontend to Backend

1. **Update Vercel environment variable**:
   - Go back to Vercel dashboard
   - Select your project → "Settings" → "Environment Variables"
   - Edit `VITE_API_URL`
   - Change value to your Railway URL (from Step 2.5)
   - Click "Save"

2. **Redeploy frontend**:
   - Go to "Deployments" tab
   - Click "..." on latest deployment
   - Click "Redeploy"

### Step 4: Test Your Live Site! 🎉

Visit your Vercel URL and try the immigration assessment!

**Share this link with family** - they can access it from any device, no login needed!

---

## Option 2: Deploy to Render (Alternative - Also Free)

### Frontend on Vercel (same as above)

### Backend on Render:

1. Go to https://render.com/ and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Name: immigration-backend
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt && playwright install chromium`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Railway)
6. Click "Create Web Service"

---

## Important Notes

### Free Tier Limits (Railway):
- 500 hours/month (plenty for family use)
- $5 credit/month
- Sleeps after inactivity (wakes up automatically when visited)

### Free Tier Limits (Vercel):
- Unlimited bandwidth for personal use
- 100GB bandwidth/month
- No sleep - always instant

### Free Tier Limits (Render):
- Free web services sleep after 15 min of inactivity
- 750 hours/month

### API Costs:
Your Anthropic API key will be used when family members use the site. Monitor usage at https://console.anthropic.com/

**Typical costs for moderate family use**: $5-20/month depending on usage

---

## Automatic Updates

After initial setup, any time you want to update:

1. Make changes to code on your computer
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Updated features"
   git push
   ```
3. Vercel and Railway automatically redeploy! ✨

---

## Troubleshooting

**Frontend shows but can't connect to backend:**
- Check CORS_ORIGINS includes your Vercel URL
- Check VITE_API_URL is set correctly
- Check backend service is running (not sleeping)

**Backend errors:**
- Check ANTHROPIC_API_KEY is set correctly
- Check logs in Railway/Render dashboard

**"This site can't be reached":**
- Backend might be sleeping (Railway free tier)
- First visit after inactivity takes 30 seconds to wake up

---

## Making It Faster (Optional Upgrade)

If you want to prevent sleep and make it instant for family:

**Railway**: Add a payment method (still likely free with $5 credit)
**Render**: Upgrade to paid plan ($7/month for always-on)

But for moderate family use, free tier is perfect!

---

Need help? The deployment should be straightforward, but let me know if you hit any issues!
