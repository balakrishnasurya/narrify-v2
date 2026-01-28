# Narratify - v2 Project Documentation

This project is a web application designed to extract text from PDF documents based on user-specified page ranges. It consists of a Python-based backend using FastAPI and an Angular-based frontend.

## Overall Architecture

The application is split into two main components:
1.  **Backend API**: Handles PDF processing and text extraction logic.
2.  **Frontend UI**: Provides an interactive interface for file selection, preview, and results display.

### Workflow
1.  **User Interaction**: The user uploads a PDF file via the frontend interface.
2.  **Preview**: The frontend generates a local preview of the PDF using a blob URL.
3.  **Page Selection**: The user specifies which pages to extract (supporting ranges like "1, 3-5").
4.  **API Request**: The frontend sends the file and page specifications to the backend endpoint `/api/extract`.
5.  **Processing**:
    *   The backend validates the file type.
    *   It parses the page specification string.
    *   It uses `PyMuPDF` to load the PDF and extract text from the requested pages.
6.  **Response**: The backend returns the extracted text (both per-page and concatenated) along with any warnings.
7.  **Display**: The frontend displays the extracted text and allows the user to copy or download it.

---

## Backend

The backend is built with **Python** and **FastAPI**. It serves as a RESTful API provider.

### Key Files
*   `backend/app.py`: The main entry point. Defines the FastAPI application, CORS settings, and the extraction logic.
*   `backend/requirements.txt`: Lists all Python dependencies.

### API Endpoints
*   `POST /api/extract`: Accepts a file upload (`file`) and page range string (`pages`). Returns JSON containing filename, extracted text keyed by page number, a concatenated text string, and a list of warnings.

### Libraries Used
| Library | Version | Purpose |
| :--- | :--- | :--- |
| **fastapi** | 0.95.2 | High-performance web framework for building APIs. |
| **uvicorn[standard]** | 0.22.0 | ASGI server implementation to run the application. |
| **PyMuPDF** | 1.22.5 | (Imported as `fitz`) Robust PDF parsing and rendering library used here for text extraction. |
| **python-multipart** | 0.0.6 | A parse for multipart/form-data, required for file uploads in FastAPI. |
| **pydantic** | 1.10.11 | Data validation and settings management using python type hinting. |

---

## Frontend

The frontend is a Single Page Application (SPA) built with **Angular (v20)**.

### Key Files
*   `frontend/angular-app/src/app/pdf-extract/pdf-extract.ts`: The main component logic. Handles file selection, UI state (loading, error, success), and user actions (extract, copy, download).
*   `frontend/angular-app/src/app/services/pdf-extract.service.ts`: An Angular Injectable service that handles HTTP communication with the backend.

### Key Features
*   **PDF Preview**: Securely sanitizes and displays the uploaded PDF in an embedded frame.
*   **Range Parsing Input**: Accepts complex page ranges from the user.
*   **Clipboard Integration**: One-click copying of extracted text.
*   **File Download**: Generates a `.txt` file blob in the browser for downloading results.

### Libraries Used
| Library | Version | Purpose |
| :--- | :--- | :--- |
| **@angular/core** | ^20.1.0 | The core framework for the frontend application. |
| **@angular/common** | ^20.1.0 | Common directives and pipes (used for HTTP client, etc.). |
| **@angular/forms** | ^20.1.0 | Handling form inputs (ngModel). |
| **@angular/router** | ^20.1.0, | Routing capabilities (though mainly a single view here). |
| **rxjs** | ~7.8.0 | Reactive Extensions for streaming async data (HTTP responses). |
| **typescript** | ~5.8.2 | The primary language used for development. |
