from pydantic import BaseModel

# user jab naya task bayega, tub hum sirf name maange
class TaskCreate(BaseModel):
    name: str

# jab hum api se responce bhegenje , tab id aur naam  dono denge
class TaskResponse(BaseModel):
    id: int
    name: str

    # class Config:
    #        from_attributes = True  # Yeh Pydantic ko batata hai ki SQLAlchemy model ko kaise read karna hai

class UserCreate(BaseModel):
    email:str
    password:str

# API se wapas bheje jane wala user data (Isme password nahi bhejenge, security ke liye)
class UserResponse(BaseModel):
    id:int
    email:str

    class Config:
        from_attributes = True 