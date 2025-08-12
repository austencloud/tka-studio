# 🚀 TKA Web Applications Port Configuration

## 📋 Port Allocation

| **Application** | **Port** | **Location** | **Purpose** |
|---|---|---|---|
| **Website** | `5173` | `src/website/` | Main website/animator app (default Vite port) |
| **Legacy Web App** | `5175` | `src/web_app/legacy_web/` | Legacy Svelte application |
| **Modern Web App** | `5177` | `src/web_app/modern_web/` | Modern Svelte 5 + Runes application |

## 🔧 Development Commands

### **Modern Web App (Port 5177)**
```bash
cd src/web_app/modern_web
npm run dev
# Opens at: http://localhost:5177
```

### **Legacy Web App (Port 5175)**
```bash
cd src/web_app/legacy_web
npm run dev
# Opens at: http://localhost:5175
```

### **Website (Port 5173)**
```bash
cd src/website
npm run dev
# Opens at: http://localhost:5173
```

## ✅ Benefits of This Configuration

- **No Port Conflicts**: Each app runs on a distinct port
- **Simultaneous Development**: Run multiple apps at once for testing
- **Clear Separation**: Easy to identify which app you're working with
- **Consistent URLs**: Predictable ports for each application

## 🎯 Quick Access URLs

- **Modern Web App**: http://localhost:5177
- **Modern Web Test Page**: http://localhost:5177/simple-test
- **Legacy Web App**: http://localhost:5175  
- **Website**: http://localhost:5173

## 📝 Configuration Files Updated

- `src/web_app/modern_web/package.json` - Set port 5177
- `src/web_app/legacy_web/vite.config.ts` - Set port 5175
- `src/website/vite.config.ts` - Set port 5173 (explicit)

---

*This configuration ensures clean separation between all TKA web applications and prevents any URL conflicts during development.*
