from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import Response, status, HTTPException, Depends
from ..database import get_db
from fastapi import APIRouter

router = APIRouter(
    tags=['Posts']
)

@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()  # this is just the sql statement!
    return posts

@router.get("/post/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    else:
        return post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)  # setting a manual status code and specific response model
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())  # ** is shortcut to unpack key/value from the dict of the Pydantic Post object
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return post


@router.delete("/post/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/post/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict())
    db.commit()

    return post_query.first()
