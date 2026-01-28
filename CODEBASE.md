# Narratify v2 Codebase Documentation

## Overview
This document provides a detailed summary of the commands used, modules imported, and key functions implemented in the Narratify v2 project. It serves as a reference for future development and maintenance.

---

## Setup Commands

### Python Backend
```powershell
# Create and activate virtual environment
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# Install FastAPI dependencies
pip install -r backend/requirements.txt

# Run development server
uvicorn --app-dir backend app:app --reload --host 127.0.0.1 --port 8000
```

### Angular Frontend
```powershell
# Install dependencies
cd frontend\angular-app; npm install

# Serve development build
ng serve --port 4200
```

---

## Backend Modules & Functions
| Module               | Version               | Purpose                                                              |
|----------------------|-----------------------|----------------------------------------------------------------------|
| fastapi              | 0.95.2                | Web framework for defining API endpoints                             |
| uvicorn              | 0.22.0                | ASGI server to run FastAPI                                           |
| PyMuPDF (fitz)       | 1.22.5                | PDF parsing and text extraction                                       |
| python-multipart     | 0.0.6                 | Handle multipart/form-data for file uploads                          |
| pydantic             | 1.10.11               | Data validation and settings management                              |
| starlette            | 0.27.0                | Underlying toolkit for FastAPI                                       |

### Key Function
- `extract_pdf_text(file: UploadFile, pages: str) -> JSON`:
  - Reads uploaded PDF
  - Parses specified pages or ranges
  - Returns JSON with extracted text and warnings

---

## Frontend Modules & Components
| Angular Module             | Purpose                                                |
|----------------------------|--------------------------------------------------------|
| BrowserModule              | Core module providing browser rendering                |
| HttpClientModule           | HTTP client for API communication                      |
| RouterModule (provideRouter) | Client-side routing configuration                     |
| FormsModule                | Template-driven forms and `ngModel` support            |
| CommonModule               | Common Angular directives (ngIf, ngFor, etc.)          |

### Standalone Components
- **App** (`app.ts`)
  - Root standalone component
  - Imports `RouterOutlet`, `FormsModule`, `HttpClientModule`
  - Bootstrapped via `bootstrapApplication`

- **PdfExtract** (`pdf-extract.ts`)
  - Uploads PDF and displays preview
  - Uses Angular's `DomSanitizer` to secure blob URL
  - Calls `PdfExtractService` to extract text
  - Displays extracted pages and copy-to-clipboard functionality

### Service
- **PdfExtractService** (`pdf-extract.service.ts`)
  - Provides `extract(file: File, pages: string): Observable<any>`
  - Sends multipart POST to `/api/extract`

---

## Routing Configuration
- Defined in `app.routes.ts` using `loadComponent` for lazy-loading:
  ```ts
  export const routes: Routes = [
    {
      path: '',
      loadComponent: () => import('./pdf-extract/pdf-extract').then(m => m.PdfExtract)
    }
  ];
  ```
- Embedded with `RouterOutlet` in `app.html`
- Initial navigation enabled via `withEnabledBlockingInitialNavigation()`

---

## Usage
1. Start backend: `uvicorn --app-dir backend app:app --reload`
2. Start frontend: `ng serve`
3. Open browser at `http://localhost:4200`
4. Upload a PDF and specify pages to extract

---

## Future Reference
- To add new features (text-to-speech, EPUB import), extend FastAPI endpoint and Angular component.
- For production, configure CORS in FastAPI and build Angular with `ng build --prod`.
