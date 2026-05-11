from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.document import Document
from app.core.redis_client import publish_event

import time
import fitz


@celery_app.task(bind=True)
def process_document(self, doc_id: int):

    db = SessionLocal()

    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()

        if not doc:
            return

        # ---------------- PROCESS STEPS ----------------

        steps = [
            ("job_started", 10),
            ("parsing", 30),
            ("extracting", 60),
            ("saving", 90),
            ("completed", 100),
        ]

        for step, progress in steps:

            doc.status = step
            db.commit()

            publish_event(
                f"document_{doc_id}",
                {
                    "doc_id": doc_id,
                    "status": step,
                    "progress": progress,
                },
            )

            print(f"{doc_id}: {step}")

            time.sleep(1)

        # ---------------- REAL PDF EXTRACTION ----------------

        file_path = f"uploads/{doc.filename}"

        text = ""

        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        # ---------------- GENERIC EXTRACTION ----------------

        extracted = {
            "filename": doc.filename,
            "pages": len(pdf),
            "total_characters": len(text),
            "text_preview": text[:3000],
            "document_type": detect_document_type(text),
            "status": "Processed Successfully",
        }

        doc.extracted_data = extracted

        db.commit()

        # ---------------- FINAL EVENT ----------------

        publish_event(
            f"document_{doc_id}",
            {
                "doc_id": doc_id,
                "status": "completed",
                "progress": 100,
                "data": extracted,
            },
        )

        print(f"Document {doc_id} processed successfully")

    except Exception as e:

        print("PROCESSING ERROR:", e)

        doc.status = "failed"
        doc.error_message = str(e)

        db.commit()

        publish_event(
            f"document_{doc_id}",
            {
                "doc_id": doc_id,
                "status": "failed",
                "error": str(e),
            },
        )

    finally:
        db.close()


# ---------------- DOCUMENT TYPE DETECTION ----------------

def detect_document_type(text):

    text = text.lower()

    if "education" in text or "skills" in text:
        return "Resume"

    elif "invoice" in text or "bill" in text:
        return "Invoice"

    elif "report" in text:
        return "Report"

    elif "certificate" in text:
        return "Certificate"

    else:
        return "General Document"