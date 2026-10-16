from fastapi import APIRouter, HTTPException
from app.schemas import FeedbackInput
from app.services.feedback import save_feedback

router = APIRouter()

@router.post("/feedback",status_code=201)
def submit_feedback(payload: FeedbackInput):
  try:
    saved = save_feedback(payload.model_dump())
  except Exception:
    raise HTTPException(status_code=500,detail = "could not save feed back try again")
  if not saved:
    raise HTTPException(status_code=409,detail = "feedback already submitted for this prediction")
  return {"message":"thank you your feedback saved"}
        