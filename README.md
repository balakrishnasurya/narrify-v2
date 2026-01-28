# Narratify — PDF Copy MVP

This repository contains an MVP for extracting text from PDFs by page and a simple Angular integration example.

Structure
- `backend/` - FastAPI app and requirements
- `frontend/angular-sample/` - Angular example snippets (service + component)
- `frontend/static_preview/` - quick static HTML preview to call the API
- `PLANNING.md` - project plan and roadmap

## Getting Started

### Backend

1. Navigate to the backend directory:

```powershell
cd backend
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the FastAPI server:

```powershell
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

#### Why Uvicorn?
Uvicorn is a fast ASGI server that runs your FastAPI application. The command options mean:
- `app:app`: the Python module (`app.py`) and the ASGI `app` instance to serve.
- `--reload`: auto-restarts the server on code changes during development.
- `--host` and `--port`: specify the network interface and port to listen on.

#### Alternative Startup Options
- **Run directly via Python**: add at the bottom of `backend/app.py`:
  ```python
  if __name__ == "__main__":
      import uvicorn
      uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
  ```
  Then start with:
  ```powershell
  python backend/app.py
  ```
- **Use Python module flag** (same as `uvicorn` CLI):
  ```powershell
  python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
  ```

### Frontend

1. Navigate to the Angular app directory:

```powershell
cd frontend/angular-app
```

2. Install Node.js dependencies:

```powershell
npm install
```

3. Start the development server:

```powershell
npm start
```

The app will be available at http://localhost:4200 by default.

Notes
- For scanned PDFs you'll need OCR (Tesseract) in a future iteration. The current extractor uses PyMuPDF (fitz) and looks for text on the page.
