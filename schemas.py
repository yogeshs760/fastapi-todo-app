from pydantic import BaseModel, ConfigDict

# user jab naya task bayega, tub hum sirf name maange
class TaskCreate(BaseModel):
    name: str

# jab hum api se responce bhegenje , tab id aur naam  dono denge
class TaskResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #        from_attributes = True  # Yeh Pydantic ko batata hai ki SQLAlchemy model ko kaise read karna hai

class UserCreate(BaseModel):
    email:str
    password:str

# API se wapas bheje jane wala user data (Isme password nahi bhejenge, security ke liye)
class UserResponse(BaseModel):
    id:int
    email:str

    model_config = ConfigDict(from_attributes=True)