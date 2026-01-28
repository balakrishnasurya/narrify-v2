# Project Journey

This document traces the steps, commands, and major changes made during the development of the Narratify PDF Text Extractor project.

---

## 1. Backend Setup

1. Create and activate Python virtual environment

   ```powershell
   cd "D:\workspace\Narratify - v2"
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r backend/requirements.txt
   ```

2. Installed dependencies (FastAPI, Uvicorn, PyMuPDF, python-multipart, Pydantic).

3. Created `backend/app.py` and implemented:
   - `/api/extract` FastAPI endpoint
   - Temporary file handling
   - `parse_pages_spec` utility for page range validation
   
4. Run backend server:

   ```powershell
   cd backend
   uvicorn app:app --host 127.0.0.1 --port 8000
   ```

---

## 2. Frontend Setup

1. Navigate to frontend folder and install packages

   ```powershell
   cd "D:\workspace\Narratify - v2\frontend\angular-app"
   npm install
   ```

2. Scaffold Angular standalone application

   ```bash
   ng new angular-app --standalone
   ```

3. Serve frontend during development:

   ```bash
   npm start
   ng serve
   ```

---

## 3. PDF Extract Feature

1. Generated standalone component for PDF extraction:

   ```bash
   ng generate component pdf-extract --standalone --inline-style --inline-template
   ```

2. Implemented in `src/app/pdf-extract/pdf-extract.ts`:
   - File upload control
   - PDF preview via `<embed>`
   - Page selection and range input
   - Text extraction display and copy-to-clipboard
   - Extended UI to show combined extracted text in a single textarea and added "Copy All Text" and "Download All Text" buttons for convenience

4. Created service in `src/app/services/pdf-extract.service.ts`:
   ```typescript
   extract(file: File, pages: string): Observable<{ pages, extracted_text, warnings }> {
     const formData = new FormData();
     formData.append('file', file, file.name);
     formData.append('pages', pages);
     return this.http.post('/api/extract', formData);
   }
   ```

---

## 4. Routing & Providers

1. Configured lazy-loaded route in `src/app/app.routes.ts`:
   ```typescript
   export const routes: Route[] = [
     {
       path: '',
       loadComponent: () => import('./pdf-extract/pdf-extract').then(m => m.PdfExtract)
     }
   ];
   ```

2. Setup application providers in `src/app/app.config.ts`:
   ```typescript
   providers: [
     importProvidersFrom(BrowserModule),
     provideHttpClient(),
     provideRouter(routes, withEnabledBlockingInitialNavigation())
   ]
   ```

---

## 5. Security & Sanitization

- Resolved XSS error for blob URLs using Angular's `DomSanitizer`
- Updated in component:
  ```typescript
  this.sanitizedPdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(URL.createObjectURL(this.selectedFile));
  ```

---

## 6. Documentation

- Created `CODEBASE.md` summarizing architecture and code structure.
- Generated this `JOURNEY.md` to capture full development history.

---

## 7. Major Commands Summary

| Purpose                 | Command                                                                                              |
|-------------------------|------------------------------------------------------------------------------------------------------|
| Create venv             | `python -m venv .venv`                                                                                |
| Activate venv           | `.\.venv\Scripts\Activate.ps1`                                                                     |
| Install backend deps    | `pip install -r backend/requirements.txt`                                                            |
| Run backend             | `uvicorn app:app --host 127.0.0.1 --port 8000`                                                       |
| Scaffold Angular app    | `ng new angular-app --standalone`                                                                    |
| Install frontend deps   | `npm install`                                                                                        |
| Serve frontend          | `npm start` / `ng serve`                                                                             |
| Generate component      | `ng generate component pdf-extract --standalone`                                                     |

---

## 8. Next Steps

1. Add CORS middleware in `backend/app.py`:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(
       CORSMiddleware,
       allow_origins=['http://localhost:4200'],
       allow_methods=['*'],
       allow_headers=['*'],
   )
   ```

2. Write end-to-end integration tests between Angular service and FastAPI endpoint.

---

*Document created on August 23, 2025*