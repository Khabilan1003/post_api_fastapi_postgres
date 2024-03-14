from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2

router = APIRouter(prefix="/vote", tags=["Votes"])

@router.post("/")
def make_vote(vote: schemas.VoteBody , db: Session = Depends(database.get_db) , current_user: models.Users = Depends(oauth2.get_current_user)):
    vote_in_database_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user.id)
    
    vote_in_database = vote_in_database_query.first()
    
    if vote.dir == 1:
        
        if vote_in_database:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"User with user_id : {current_user.id} have already voted the post with post_id : {vote.post_id}")
        
        new_vote = models.Vote(**{
            "post_id" : vote.post_id,
            "user_id" : current_user.id
        })
        
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        
        return new_vote
    else:
        if not vote_in_database:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"User with user_id : {current_user.id} have not voted the post with post_id : {vote.post_id}")
        
        vote_in_database_query.delete()
        db.commit()
        
        return {"message" : f"Vote for post_id : {vote.post_id} is deleted successfully"} 