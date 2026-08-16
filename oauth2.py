from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import SessionLocal, get_db
import models

# 1. OAuth2 ka scheme setup (Yeh batata hai ki login URL kya hai)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 2. JWT Setup Variables (Security Keys)
SECRET_KEY = "ek_bahut_lamba_aur_secure_secret_key" # Real apps mein isko hide karte hain
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token 30 minute baad expire ho jayega

# 3. Token Generate karne ka function
def create_access_token(data: dict):
    # Data ki copy banai
    to_encode = data.copy()
    
    # Expiry time set kiya
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # JWT library se token create kiya
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 4. Token Validate karne ka function (Dependency)
# Har secured endpoint is function ko use karega check karne ke liye ki user logged in hai ya nahi
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Token ko open (decode) karo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    # Database se user find karo aur return karo
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
        
    return user