from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends
from ..database import get_db
from fastapi import APIRouter

router = APIRouter(
    tags=['Posts']
)

@router.get("/posts", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)

    return results

@router.get("/post/{id}", response_model=schemas.PostBase)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    else:
        return post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostBase)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/post/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/post/{id}", response_model=schemas.PostBase)
def update_post(id: int, updated_post: schemas.PostBase,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict())
    db.commit()

    return post_query.first()
