from sqlalchemy import Column, String, Integer, ForeignKey
from db import Base, SessionLocal
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) # Email unique hona chahiye
    password = Column(String) # Yahan plain password nahi, balki hashed password save hoga

    # Ek user ke bohot saare tasks ho sakte hain (One-to-Many relationship)
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__="tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    owner_id= Column(Integer, ForeignKey("users.id"))

    owner= relationship("User", back_populates="tasks")

    # # ek single task ko represent karne ka Blueprint
    # def __init__(self,id,name):
    #     self.id= id
    #     self.name= name

# class TaskManager:
    # def __init__(self):
    #     # SessionLocal ke aage () lagayein taaki ek naya session create ho
    #     self.db= SessionLocal()

    # # # Tasks ki list aur operation(Add View) manage karne ke liye
    # # def __init__(self):
    # #     self.tasks=[]
    # #     self.next_id=1

    # def add_task(self,name):
    #     new_task= Task(name=name)
    #     self.db.add(new_task)
    #     self.db.commit()
    #     self.db.refresh(new_task)
        

    # def view_task(self):
    #     # Database se saare tasks fetch kiye
    #     return self.db.query(Task).all()