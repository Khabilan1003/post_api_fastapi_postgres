from jose import JWTError , jwt
from datetime import datetime , timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import database, models
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp" : expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key , settings.algorithm)
    
    return encoded_jwt

def verify_access_token(token: str , credentials_exception):
    try:
        payload = jwt.decode(token , settings.secret_key , settings.algorithm)
        
        id: int = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        
        return id
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_schema) , db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"Could Not Validate Credentials" , headers={"WWW-Authenticate": "Bearer"})
    
    user_id = verify_access_token(token , credentials_exception=credentials_exception)
    
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    
    return user