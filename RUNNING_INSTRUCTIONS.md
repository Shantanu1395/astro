# 🚀 Vedic Astrology Journey - Running Instructions

## 📋 **Prerequisites**

### **System Requirements**
- **Node.js 18+** (for frontend development)
- **Python 3.8+** (for backend API)
- **Git** (for version control)
- **Modern Browser** (Chrome, Firefox, Safari, Edge)

### **Check Prerequisites**
```bash
# Check Node.js version
node --version
# Should output: v18.x.x or higher

# Check Python version
python --version
# Should output: Python 3.8.x or higher

# Check npm version
npm --version
# Should output: 8.x.x or higher
```

## 🛠️ **Installation & Setup**

### **Step 1: Install Frontend Dependencies**
```bash
# Navigate to project root
cd /path/to/your/project

# Install all frontend dependencies
npm install

# This will install:
# - React + TypeScript
# - Three.js + React Three Fiber
# - Framer Motion
# - Tailwind CSS
# - D3.js
# - Zustand
# - And all other dependencies
```

### **Step 2: Verify Backend Setup**
```bash
# Ensure your existing FastAPI backend is ready
# Your backend should have the /api/predict endpoint

# Test backend health (if running)
curl http://localhost:8000/health
# or
python -c "import requests; print(requests.get('http://localhost:8000/health').status_code)"
```

## 🚀 **Running the Application**

### **Method 1: Automated Script (Recommended)**
```bash
# Run the automated development script
python scripts/run_vedic_journey.py

# This script will:
# 1. Check and install dependencies if needed
# 2. Start the backend server (if not running)
# 3. Start the frontend development server
# 4. Open browser automatically
# 5. Display all access URLs
```

### **Method 2: Manual Setup**
```bash
# Terminal 1: Start Backend (if not already running)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend
npm run dev

# The frontend will start on http://localhost:3000
# The backend will be on http://localhost:8000
```

### **Method 3: Production Build**
```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Serve with a static server
npx serve dist
```

## 🌐 **Access Points**

Once running, you can access:

- **🎨 Frontend Application:** http://localhost:3000
- **🔧 Backend API:** http://localhost:8000
- **📚 API Documentation:** http://localhost:8000/docs
- **🔍 API Redoc:** http://localhost:8000/redoc

## 🎯 **Testing the Application**

### **Step 1: Verify Frontend Load**
1. Open http://localhost:3000
2. You should see the cosmic-themed loading screen
3. The application should initialize with the first learning module
4. Navigation sidebar should show available modules

### **Step 2: Test 3D Visualization**
1. The main area should display a 3D celestial scene
2. You should see Earth at the center with a blue atmosphere
3. Planets should be positioned around Earth
4. Zodiac signs (rashis) should be visible in the outer ring
5. Try rotating the view with mouse drag
6. Test zoom with mouse wheel

### **Step 3: Test 2D Traditional Charts**
1. Click the "Traditional" view mode button
2. You should see a classic Vedic birth chart
3. Houses should be numbered 1-12
4. Planets should be positioned in their respective houses
5. Zodiac signs should be around the outer edge

### **Step 4: Test Interactive Learning**
1. Navigate through different modules in the sidebar
2. Read the content in the bottom panel
3. Try the interactive tutorial (Help button)
4. Test the navigation controls

### **Step 5: Test API Integration**
1. Check browser console for API calls
2. Verify data is loading from your backend
3. Test with different birth data if available

## 🐛 **Troubleshooting**

### **Common Issues & Solutions**

#### **Frontend Won't Start**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for port conflicts
lsof -ti:3000
# Kill process if needed: kill -9 <PID>
```

#### **Backend Connection Issues**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check for port conflicts
lsof -ti:8000

# Restart backend
python -m uvicorn main:app --reload --port 8000
```

#### **3D Visualization Not Loading**
1. Check browser console for WebGL errors
2. Ensure your browser supports WebGL 2.0
3. Try disabling browser extensions
4. Check if hardware acceleration is enabled

#### **API Integration Issues**
1. Check CORS settings in your backend
2. Verify the /api/predict endpoint is working
3. Check network tab in browser dev tools
4. Ensure request/response formats match

### **Browser Compatibility**
- **Chrome 90+** ✅ Fully supported
- **Firefox 88+** ✅ Fully supported  
- **Safari 14+** ✅ Fully supported
- **Edge 90+** ✅ Fully supported

### **Performance Tips**
- Use Chrome DevTools Performance tab to monitor FPS
- Reduce animation speed if performance is poor
- Close other browser tabs for better performance
- Ensure hardware acceleration is enabled

## 📊 **Development Commands**

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run type checking
npm run type-check

# Run linting
npm run lint

# Install new dependency
npm install <package-name>

# Update dependencies
npm update
```

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the project root:
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Development Settings
VITE_DEV_MODE=true
VITE_ENABLE_CONSOLE_LOGS=true

# Feature Flags
VITE_ENABLE_3D_VISUALIZATION=true
VITE_ENABLE_TUTORIAL_MODE=true
```

### **Vite Configuration**
The `vite.config.ts` file includes:
- Proxy setup for API calls
- Build optimization
- Development server configuration

### **Tailwind Configuration**
The `tailwind.config.js` includes:
- Cosmic color palette
- Custom animations
- Responsive breakpoints

## 📱 **Mobile Testing**

### **Local Mobile Testing**
```bash
# Find your local IP
ipconfig getifaddr en0  # macOS
hostname -I  # Linux
ipconfig  # Windows

# Access from mobile device
http://YOUR_LOCAL_IP:3000
```

### **Mobile-Specific Features**
- Touch gestures for 3D navigation
- Responsive layout adaptation
- Mobile-optimized controls
- Touch-friendly interactive elements

## 🚀 **Deployment**

### **Frontend Deployment**
```bash
# Build for production
npm run build

# Deploy to Vercel
npx vercel

# Deploy to Netlify
npx netlify deploy --prod --dir=dist

# Deploy to GitHub Pages
npm run build
# Then upload dist/ folder
```

### **Backend Integration**
Ensure your production backend:
- Has CORS configured for your frontend domain
- Serves the /api/predict endpoint
- Has proper error handling
- Uses HTTPS in production

## 📞 **Support**

If you encounter issues:

1. **Check the console** for error messages
2. **Verify prerequisites** are installed correctly
3. **Test API endpoints** independently
4. **Check network connectivity** between frontend and backend
5. **Review browser compatibility** requirements

## 🎯 **Next Steps**

Once Phase 1 is running successfully:
1. Test all interactive features
2. Verify API integration with real data
3. Check performance on different devices
4. Review user experience flow
5. Prepare for Phase 2 development

---

**Happy coding! 🌟 Your Vedic Astrology Journey awaits!** ✨
