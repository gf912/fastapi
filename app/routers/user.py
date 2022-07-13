from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import status, Depends, HTTPException, APIRouter
from ..database import get_db
from .. import utils

router = APIRouter(
    tags=['Users'] # group the routes together in doc
)

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):

    # hash the password and re-store into the User pydametic model

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())  # ** is shortcut to unpack key/value from the dict of the Pydantic Post object
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    else:
        return user