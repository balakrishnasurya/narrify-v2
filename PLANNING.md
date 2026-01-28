# Narratify — Project Plan & Design

## Summary

Short: Browser-based app to extract text from documents (PDF now, EPUB later) by page or chapter, then let users send selected text with a prompt to an LLM that reforms the text for TTS consumption.

This document contains the MVP scope, tech stack recommendations, architecture, API contract, frontend UX, and a phased roadmap.

## MVP Scope
- Upload PDF in browser
- Enter page number(s) or ranges (e.g. `1`, `1,3,5`, `2-4`, `1,3-5`)
- Backend extracts text for requested pages and returns JSON
- Frontend displays per-page text; allows copy-to-clipboard and download
- UI includes optional prompt textarea for future LLM step

## Chosen Tech for MVP
- Frontend: Angular (TypeScript)
- Backend: Python + FastAPI
- PDF parsing: PyMuPDF (fitz) recommended; pdfplumber as alternative

## Architecture

- Browser (Angular app)
  - Upload PDF via multipart/form-data to backend
  - Enter page spec and call /api/extract
  - Show results and provide copy/download and optional prompt

- Backend (FastAPI)
  - POST /api/extract: accepts file + pages string, returns JSON mapping pages to text
  - Optional OCR path (Tesseract) for scanned PDFs in later phases

## API Contract

POST /api/extract
- Content-Type: multipart/form-data
- Form fields:
  - file: PDF file (required)
  - pages: string e.g. "1", "1,3,5", "2-5", "1,3-5" (required)

Response 200 JSON:
```
{
  "filename": "sample.pdf",
  "pages": { "1": "text...", "3": "text..." },
  "extracted_text": "...",
  "warnings": []
}
```

Errors: 400 for invalid input, 500 for server error.

## Frontend UX
- Upload control (drag & drop + browse)
- Page selector input
- Extract button
- Results: per-page card with text and copy/download
- Prompt textarea (optional) for future LLM processing

## Dev decisions & tradeoffs
- FastAPI vs Flask: FastAPI chosen for modern API, async support, and automatic docs.
- PyMuPDF recommended for speed and robustness.

## Roadmap
- Phase 1 (MVP): Extract by page, Angular frontend, FastAPI backend
- Phase 2: OCR, batch processing, background jobs
- Phase 3: LLM integration (prompt + processing)
- Phase 4: TTS generation and audio management
- Phase 5: Auth, storage, production deploy

## Next steps for implementation (immediate)
1. Implement FastAPI endpoint that extracts pages using PyMuPDF
2. Implement Angular component/service to upload and call endpoint
3. Add README and run instructions

---
