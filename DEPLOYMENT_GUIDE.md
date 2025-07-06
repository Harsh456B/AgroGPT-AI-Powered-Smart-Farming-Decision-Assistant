# AgroGPT Web - Free Deployment Guide

## Overview
This guide covers deployment options for your Django-based AgroGPT Web application on free platforms.

## **Option 1: Railway (Recommended)**

### Why Railway?
- Free tier with 500 hours/month
- Automatic deployments from GitHub
- Built-in PostgreSQL database
- Easy environment variable management

### Steps:
1. **Prepare your repository:**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your AgroGPT repository
   - Railway will automatically detect Django and deploy

3. **Configure Environment Variables:**
   - Go to your project settings in Railway
   - Add these environment variables:
     ```
     SECRET_KEY=your-secret-key-here
     DEBUG=False
     ```

4. **Database Setup:**
   - Railway provides PostgreSQL automatically
   - Update settings.py to use PostgreSQL (optional)

## **Option 2: Render (Alternative)**

### Why Render?
- Free tier with 750 hours/month
- Automatic deployments
- Custom domains
- Good for Django apps

### Steps:
1. **Create render.yaml:**
   ```yaml
   services:
     - type: web
       name: agrogpt-web
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn agrogpt_web.wsgi:application
       envVars:
         - key: SECRET_KEY
           generateValue: true
         - key: DEBUG
           value: false
   ```

2. **Deploy:**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Render will use the render.yaml file

## **Option 3: Vercel (For Frontend-Heavy Apps)**

### Why Vercel?
- Excellent for static sites
- Great performance
- Automatic deployments

### Steps:
1. **Create vercel.json:**
   ```json
   {
     "builds": [
       {
         "src": "agrogpt_web/wsgi.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "agrogpt_web/wsgi.py"
       }
     ]
   }
   ```

2. **Deploy:**
   - Install Vercel CLI: `npm i -g vercel`
   - Run: `vercel`

## **Option 4: PythonAnywhere (Educational)**

### Why PythonAnywhere?
- Free tier available
- Good for learning
- Python-focused

### Steps:
1. **Sign up at pythonanywhere.com**
2. **Upload your code via Git or file upload**
3. **Configure WSGI file**
4. **Set up virtual environment**
5. **Install dependencies**

## **Option 5: Heroku (Legacy Free Tier Ended)**

### Note: Heroku no longer offers free tier
- Paid plans start at $7/month
- Still excellent for Django apps

## **Pre-Deployment Checklist**

### ✅ Files Created:
- [x] requirements.txt (updated)
- [x] Procfile
- [x] runtime.txt
- [x] settings.py (production-ready)

### ✅ Next Steps:
1. **Test locally:**
   ```bash
   python manage.py collectstatic
   python manage.py migrate
   gunicorn agrogpt_web.wsgi
   ```

2. **Create .gitignore:**
   ```
   *.pyc
   __pycache__/
   .env
   .venv/
   db.sqlite3
   staticfiles/
   media/
   ```

3. **Generate new SECRET_KEY:**
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

## **Recommended Approach**

**For your AgroGPT project, I recommend Railway because:**
1. **Free tier is generous** (500 hours/month)
2. **Automatic deployments** from GitHub
3. **Built-in database** support
4. **Easy environment management**
5. **Good for ML applications** like yours

## **Post-Deployment Tasks**

1. **Set up custom domain** (optional)
2. **Configure email settings** for contact forms
3. **Monitor application logs**
4. **Set up backups** for your ML models
5. **Configure SSL certificates** (automatic on most platforms)

## **Troubleshooting**

### Common Issues:
1. **Static files not loading:** Ensure `collectstatic` was run
2. **Database errors:** Check if migrations are applied
3. **ML models not found:** Ensure model files are in the repository
4. **Memory issues:** Optimize model loading for production

### Performance Tips:
1. **Cache ML models** in memory
2. **Use CDN** for static files
3. **Optimize database queries**
4. **Compress static files**

## **Security Considerations**

1. **Never commit SECRET_KEY** to repository
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** (automatic on most platforms)
4. **Regular security updates**
5. **Backup your data** regularly

---

**Ready to deploy? Choose Railway for the best free experience!** 