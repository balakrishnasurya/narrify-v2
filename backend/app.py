from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import fitz  # PyMuPDF
import tempfile
import os
import re

app = FastAPI(title="Narratify PDF Extractor")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # adjust as needed
    allow_methods=["*"],
    allow_headers=["*"],
)


def parse_pages_spec(spec: str, max_page: int) -> List[int]:
    """Parse a page spec string like "1,3-5,8" into sorted unique page numbers (1-based).

    Raises HTTPException on invalid spec.
    """
    if not spec:
        raise HTTPException(status_code=400, detail="pages spec is required")
    spec = spec.replace(' ', '')
    parts = spec.split(',')
    pages = set()
    for part in parts:
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            if not a.isdigit() or not b.isdigit():
                raise HTTPException(status_code=400, detail=f"invalid range: {part}")
            a_i = int(a)
            b_i = int(b)
            if a_i < 1 or b_i < 1 or a_i > b_i:
                raise HTTPException(status_code=400, detail=f"invalid range: {part}")
            for i in range(a_i, b_i + 1):
                if i <= max_page:
                    pages.add(i)
        else:
            if not part.isdigit():
                raise HTTPException(status_code=400, detail=f"invalid page number: {part}")
            p = int(part)
            if p >= 1 and p <= max_page:
                pages.add(p)
    if not pages:
        raise HTTPException(status_code=400, detail="no valid pages requested")
    return sorted(pages)


@app.post("/api/extract")
async def extract_pdf(file: UploadFile = File(...), pages: str = Form(...)):
    # validate file content-type loosely
    filename = file.filename
    if not filename.lower().endswith('.pdf'):   
        raise HTTPException(status_code=400, detail="only PDF files are supported")

    # write to temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        doc = fitz.open(tmp_path)
        max_page = doc.page_count
        try:
            pages_list = parse_pages_spec(pages, max_page)
        except HTTPException:
            doc.close()
            os.unlink(tmp_path)
            raise

        result: Dict[str, str] = {}
        warnings: List[str] = []
        concatenated = []
        for p in pages_list:
            page = doc.load_page(p - 1)  # 0-based
            text = page.get_text("text")
            if not text.strip():
                warnings.append(f"page {p} seems empty or scanned; consider OCR")
            result[str(p)] = text
            concatenated.append(text)

        doc.close()
        os.unlink(tmp_path)

        return JSONResponse({
            "filename": filename,
            "pages": result,
            "extracted_text": "\n\n".join(concatenated),
            "warnings": warnings,
        })
    except Exception as e:
        # try to clean temp file
        try:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=str(e))
    




if __name__ == "__main__":
      import uvicorn
      uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
