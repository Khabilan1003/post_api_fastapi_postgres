from fastapi import status , HTTPException , Response , Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import schemas, models, database, oauth2

router = APIRouter(prefix="/posts" , tags=["Posts"])

@router.get("/" , response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(database.get_db),
                  limit: int = 10 , skip: int = 0, search: Optional[str] = ""):
    
    posts = db.query(models.Posts , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote , models.Vote.post_id == models.Posts.id , isouter=True).group_by(models.Posts.id).filter(
            models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}" , response_model=schemas.PostOut)
def get_post(id: int , db: Session = Depends(database.get_db)):
    post = db.query(models.Posts , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote , models.Vote.post_id == models.Posts.id , isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Post id : {id} is not found")
    
    return post

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.ResponsePost)
def add_new_post(post: schemas.CreatePost , db: Session = Depends(database.get_db) , current_user: models.Users = Depends(oauth2.get_current_user)):
    
    new_post = models.Posts(owner_id = current_user.id , **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int , db: Session = Depends(database.get_db) , current_user: models.Users = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id).first()
        
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Id : {id} is not found")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"post id : {deleted_post.id} is not yours")
    
    db.delete(deleted_post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}" , response_model=schemas.ResponsePost)
def update_post(id: int , updated_post: schemas.CreatePost , db: Session = Depends(database.get_db) , current_user: models.Users = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Id : {id} is not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"post id : {post.id} is not yours")
    
    post_dict = updated_post.model_dump()
    post_dict["id"] = post.id
    post_dict["created_at"] = post.created_at
    post_dict["owner_id"] = post.owner_id
    post_query.update(post_dict, synchronize_session=False)
    db.commit()

    return post_dict