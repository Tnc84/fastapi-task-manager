# Angular Integration Guide

## Update Your Angular App to Work with FastAPI

### 1. Update Angular Environment Files

**`frontend/src/environments/environment.ts`** (Development)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'  // For development with ng serve
};
```

**`frontend/src/environments/environment.prod.ts`** (Production/Desktop)
```typescript
export const environment = {
  production: true,
  apiUrl: '/api/v1'  // Relative path - served from same origin in desktop app
};
```

---

### 2. Update angular.json Build Configuration

Make sure your `angular.json` has correct output path:

```json
{
  "projects": {
    "your-app-name": {
      "architect": {
        "build": {
          "options": {
            "outputPath": "dist/browser",
            ...
          }
        }
      }
    }
  }
}
```

Or for older Angular versions:
```json
"outputPath": "dist"
```

---

### 3. Create API Service (if you don't have one)

**`frontend/src/app/services/api.service.ts`**
```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  // Tasks
  getTasks(): Observable<any> {
    return this.http.get(`${this.apiUrl}/tasks`);
  }

  createTask(task: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/tasks`, task);
  }

  updateTask(id: number, task: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/tasks/${id}`, task);
  }

  deleteTask(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/tasks/${id}`);
  }

  // Users
  login(credentials: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/login`, credentials);
  }

  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/users/register`, userData);
  }
}
```

---

### 4. Add HttpClient to app.config.ts (Angular 17+)

**`frontend/src/app/app.config.ts`**
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient()  // Add this
  ]
};
```

Or for older Angular (app.module.ts):
```typescript
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [
    HttpClientModule,  // Add this
    ...
  ]
})
```

---

### 5. Build Commands

**Development (with live reload):**
```bash
cd frontend
ng serve
# Opens at http://localhost:4200
# Backend runs separately on http://localhost:8000
```

**Production (for desktop app):**
```bash
cd frontend
ng build --configuration production
# Output in frontend/dist/ or frontend/dist/browser/
```

**Quick rebuild:**
```bash
ng build --configuration production --output-path=dist
```

---

### 6. Handle Authentication (if using JWT)

**`frontend/src/app/interceptors/auth.interceptor.ts`**
```typescript
import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('access_token');
  
  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }
  
  return next(req);
};
```

Add to `app.config.ts`:
```typescript
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor]))
  ]
};
```

---

### 7. Testing the Integration

**Test 1: Check if backend is reachable**
```typescript
// In any component
ngOnInit() {
  this.http.get('http://localhost:8000/health').subscribe(
    data => console.log('Backend is running:', data),
    error => console.error('Backend connection failed:', error)
  );
}
```

**Test 2: Get tasks**
```typescript
this.apiService.getTasks().subscribe(
  tasks => console.log('Tasks:', tasks),
  error => console.error('Error:', error)
);
```

---

### 8. Common Issues & Solutions

**CORS Error:**
- ✅ Already configured in FastAPI (ports 3000, 4200, 8080)
- If you need more, update `app/core/config.py`

**404 on refresh:**
- ✅ Fixed - FastAPI serves index.html for all non-API routes
- Angular routing will handle the rest

**Assets not loading:**
- Check that `frontend/dist/assets/` exists
- FastAPI mounts `/assets` automatically

**API calls failing:**
- Make sure `environment.prod.ts` uses relative path `/api/v1`
- Check browser DevTools Network tab

---

### 9. Folder Structure

Your Angular project should be organized like this:

```
frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   ├── services/
│   │   │   └── api.service.ts
│   │   ├── interceptors/
│   │   │   └── auth.interceptor.ts
│   │   ├── app.component.ts
│   │   └── app.config.ts
│   ├── environments/
│   │   ├── environment.ts
│   │   └── environment.prod.ts
│   └── index.html
├── dist/           # Generated after build
│   └── browser/   # Or just dist/ for older Angular
├── angular.json
├── package.json
└── tsconfig.json
```

---

### 10. Quick Checklist

Before running the desktop app:

- [ ] Angular project is in `frontend/` folder
- [ ] Environment files are configured
- [ ] `ng build --configuration production` completes successfully
- [ ] `frontend/dist/` or `frontend/dist/browser/` exists
- [ ] `index.html` exists in the dist folder
- [ ] Backend dependencies installed: `pip install -r requirements.txt`
- [ ] Desktop dependencies installed: `pip install pywebview pythonnet`

Then run:
```bash
python launch_desktop.py
```

---

## 🎉 You're Done!

Your Angular frontend will now work perfectly with the desktop app!

