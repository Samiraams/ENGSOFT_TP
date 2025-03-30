# app/routers/annotations.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
notation)

@router.get("/by_sample/{sample_id}", response_model=List[schemas.AnnotationRead])
def list_annotations_by_sample(
    sample_id: int,
    db: Session = Depends(get_db_session)
) -> List[schemas.AnnotationRead]:
    return crud.get_annotations_by_sample(db, sample_id)

@router.get("/by_evaluator/{evaluator_email}", response_model=List[schemas.AnnotationRead])
def list_annotations_by_evaluator(
    evaluator_email: str,
    db: Session = Depends(get_db_session)
) -> List[schemas.AnnotationRead]:
    return crud.get_annotations_by_evaluator(db, evaluator_email)

@router.delete("/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_annotation(
    annotation_id: int,
    db: Session = Depends(get_db_session)
):
    deleted = crud.delete_annotation(db, annotation_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Annotation not found")
    return
