from sqlalchemy import Column , Boolean , String , Integer, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

class Posts(Base):
    __tablename__ = "posts_alchemy"
    
    id = Column(Integer , primary_key=True , nullable=False)
    title = Column(String , nullable=False)
    content = Column(String , nullable=False)
    published = Column(Boolean , server_default='TRUE')
    rating = Column(Integer , nullable=True)
    owner_id = Column(Integer , ForeignKey("users.id") , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text("now()"))
    
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer , primary_key=True , nullable=False)
    email = Column(String , nullable=False , unique=True)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text("now()"))
    
class Vote(Base):
    __tablename__ = "votes"
    
    post_id = Column(Integer , ForeignKey("posts_alchemy.id") , primary_key=True)
    user_id = Column(Integer , ForeignKey("users.id") , primary_key=True)