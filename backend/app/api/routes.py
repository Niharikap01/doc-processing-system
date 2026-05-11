from fastapi import (
    APIRouter,
    UploadFile,
    File,
    WebSocket,
    Depends
)

from fastapi.responses import (
    StreamingResponse,
    FileResponse
)

from sqlalchemy.orm import Session

import csv
import json
import os
from io import StringIO

from app.core.database import SessionLocal
from app.models.document import Document
from app.workers.tasks import process_document
from app.core.ws_manager import manager


router = APIRouter()


# ---------------- DATABASE ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- UPLOAD ----------------


import os

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # create uploads folder
    os.makedirs("uploads", exist_ok=True)

    # save actual file
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # save metadata in db
    doc = Document(
        filename=file.filename,
        file_type=file.content_type,
        status="queued"
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    # START processing
    process_document.delay(doc.id)

    return {
        "id": doc.id,
        "filename": doc.filename,
        "status": doc.status
    }


# ---------------- STATUS ----------------
@router.get("/status/{doc_id}")
def get_status(
    doc_id: int,
    db: Session = Depends(get_db)
):

    doc = db.query(Document).filter(
        Document.id == doc_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    return {
        "id": doc.id,
        "status": doc.status
    }


# ---------------- WEBSOCKET ----------------
@router.websocket("/ws/{doc_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    doc_id: int
):
    await manager.connect(doc_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except Exception:
        manager.disconnect(doc_id, websocket)


# ---------------- LIST DOCUMENTS ----------------
@router.get("/documents")
def list_documents(
    db: Session = Depends(get_db)
):

    docs = db.query(Document).all()

    return [
        {
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "status": d.status,
            "created_at": str(d.created_at),
        }
        for d in docs
    ]


# ---------------- GET DOCUMENT ----------------
@router.get("/documents/{doc_id}")
def get_document(
    doc_id: int,
    db: Session = Depends(get_db)
):

    doc = db.query(Document).filter(
        Document.id == doc_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    return {
        "id": doc.id,
        "filename": doc.filename,
        "status": doc.status,
        "extracted_data": doc.extracted_data,
        "reviewed_data": doc.reviewed_data,
        "is_finalized": doc.is_finalized
    }


# ---------------- UPDATE DOCUMENT ----------------
@router.put("/documents/{doc_id}")
def update_document(
    doc_id: int,
    data: dict,
    db: Session = Depends(get_db)
):

    doc = db.query(Document).filter(
        Document.id == doc_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    doc.reviewed_data = data

    db.commit()

    return {
        "message": "Updated successfully"
    }


# ---------------- FINALIZE ----------------
@router.post("/documents/{doc_id}/finalize")
def finalize_document(
    doc_id: int,
    db: Session = Depends(get_db)
):

    doc = db.query(Document).filter(
        Document.id == doc_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    doc.is_finalized = True
    doc.status = "finalized"

    db.commit()

    return {
        "message": "Document finalized"
    }


# ---------------- RETRY ----------------
@router.post("/documents/{doc_id}/retry")
def retry_document(
    doc_id: int,
    db: Session = Depends(get_db)
):

    doc = db.query(Document).filter(
        Document.id == doc_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    doc.status = "queued"

    doc.retry_count = (
        doc.retry_count or 0
    ) + 1

    doc.error_message = None

    db.commit()

    process_document.delay(doc.id)

    return {
        "message": "Retry started"
    }


# ---------------- EXPORT JSON ----------------
@router.get("/documents/{doc_id}/export/json")
def export_json(
    doc_id: int,
    db: Session = Depends(get_db)
):

    doc = db.query(Document).filter(
        Document.id == doc_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    data = (
        doc.reviewed_data
        or doc.extracted_data
        or {}
    )

    os.makedirs("exports", exist_ok=True)

    file_path = f"exports/document_{doc_id}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return FileResponse(
        path=file_path,
        filename=f"document_{doc_id}.json",
        media_type="application/json"
    )


# ---------------- EXPORT CSV ----------------
@router.get("/documents/{doc_id}/export/csv")
def export_csv(
    doc_id: int,
    db: Session = Depends(get_db)
):

    doc = db.query(Document).filter(
        Document.id == doc_id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    data = (
        doc.reviewed_data
        or doc.extracted_data
        or {}
    )

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow(data.keys())
    writer.writerow(data.values())

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=export.csv"
        }
    )