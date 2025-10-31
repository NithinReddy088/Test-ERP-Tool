# Healthcare Manufacturing ERP - Netlify Deployment

## 🚀 Quick Deploy to Netlify

### Option 1: One-Click Deploy
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/your-username/healthcare-erp)

### Option 2: Manual Deployment

1. **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

2. **Login to Netlify**
```bash
netlify login
```

3. **Deploy from this directory**
```bash
cd /home/nithin/pro/Test-ERP-Tool
netlify deploy --prod
```

### Option 3: Git-based Deployment

1. **Initialize Git repository**
```bash
git init
git add .
git commit -m "Initial commit: Healthcare Manufacturing ERP"
```

2. **Push to GitHub**
```bash
git remote add origin https://github.com/your-username/healthcare-erp.git
git push -u origin main
```

3. **Connect to Netlify**
- Go to [Netlify Dashboard](https://app.netlify.com)
- Click "New site from Git"
- Connect your GitHub repository
- Set build settings:
  - Build command: `npm run build`
  - Publish directory: `dist`

## 📁 Deployment Structure

```
Test-ERP-Tool/
├── dist/                    # Static frontend files
│   └── index.html          # Main application
├── netlify/
│   └── functions/          # Serverless API functions
│       ├── work-orders.js  # Work Orders API
│       ├── trace.js        # Traceability API
│       └── kpis.js         # KPIs API
├── netlify.toml            # Netlify configuration
└── package.json            # Dependencies
```

## 🌐 Live URLs (after deployment)

- **Main Application**: `https://your-site-name.netlify.app`
- **Work Orders API**: `https://your-site-name.netlify.app/api/work-orders`
- **Traceability API**: `https://your-site-name.netlify.app/api/trace/serial/SER001`
- **KPIs API**: `https://your-site-name.netlify.app/api/kpis`

## ✨ Features Available on Netlify

### ✅ **Working Features**
- **Interactive Dashboard** - Production, Quality, Finance metrics
- **Work Order Management** - View and create work orders
- **Traceability System** - Serial/batch tracking APIs
- **KPI Analytics** - Real-time performance metrics
- **Responsive Design** - Works on all devices
- **API Documentation** - Complete endpoint documentation

### ⚠️ **Limitations (Serverless)**
- **No Database Persistence** - Uses in-memory data
- **No File Uploads** - Limited to static content
- **No Real-time Updates** - No WebSocket support
- **Function Timeout** - 10-second execution limit

## 🔧 Configuration

### Environment Variables (Optional)
Set in Netlify Dashboard > Site Settings > Environment Variables:

```
API_BASE_URL=https://your-site-name.netlify.app/api
SITE_NAME=Healthcare Manufacturing ERP
```

### Custom Domain (Optional)
1. Go to Netlify Dashboard > Domain Settings
2. Add custom domain: `healthcare-erp.yourdomain.com`
3. Configure DNS records as instructed

## 📊 Analytics & Monitoring

### Netlify Analytics
- **Page Views**: Track user engagement
- **API Calls**: Monitor function usage
- **Performance**: Load times and errors

### Function Logs
```bash
netlify functions:log
```

## 🔒 Security Features

- **HTTPS by Default** - SSL certificate included
- **CORS Headers** - Cross-origin requests handled
- **Input Validation** - API parameter validation
- **Rate Limiting** - Built-in Netlify protection

## 🚀 Performance Optimizations

- **CDN Distribution** - Global edge locations
- **Static Asset Caching** - Automatic optimization
- **Function Caching** - Reduced cold starts
- **Gzip Compression** - Faster load times

## 📱 Mobile Support

The ERP system is fully responsive and works on:
- **Desktop** - Full dashboard experience
- **Tablet** - Optimized layout
- **Mobile** - Touch-friendly interface

## 🔄 Updates & Maintenance

### Automatic Deployments
- **Git Push** - Auto-deploy on commit
- **Branch Previews** - Test before production
- **Rollback** - One-click previous version

### Manual Updates
```bash
# Update functions
netlify functions:build

# Deploy changes
netlify deploy --prod
```

## 📞 Support

- **Netlify Docs**: https://docs.netlify.com
- **Function Logs**: Check Netlify dashboard
- **Status Page**: https://netlifystatus.com

---

**Your Healthcare Manufacturing ERP is now ready for global deployment! 🌍**