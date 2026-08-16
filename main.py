from fastapi import HTTPException, BackgroundTasks
from models import Task,User
from db import Base,engine, SessionLocal, get_db
from fastapi import FastAPI,Depends
import models
import schemas
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm
import oauth2 # Apni nayi file import karein
import time

# Yeh line check karegi ki 'tasks' table bani hai ya nahi, nahi bani toh bana degi-----
# # Database tables create karna
Base.metadata.create_all(bind=engine)
app= FastAPI(title= "to-do-api")

# Ek function jo pichhe (background mein) chalega
def write_backup_log(task_name: str, user_email: str):
    # Asliyat mein yeh file Drive pe ya S3 bucket pe upload hogi, 
    # abhi hum isko wait karke aur file mein likh kar simulate kar rahe hain
    time.sleep(5)  # 5 second rukega
    with open("task_backup_log.txt", mode="a") as log_file:
        log_file.write(f"User {user_email} added task: {task_name}\n")

# 5. CREATE User (User Registration)
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,db: Session= Depends(get_db)):
    #1. Plain password ko hash(encrypt) karna
    hashed_password= Hash.bcrypt(user.password)

    # 2. Database ke liye naya user object banana (hashed password ke sath)
    new_user = User(email=user.email, password=hashed_password)

    # 3. Save karna
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# 6. LOGIN User (Token Return karega)
@app.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Database mein user ko uske email (FastAPI default me isko 'username' kehta hai) se dhundo
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # Agar user na mile
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
        
    # 2. Agar user mil jaye, toh uske password ka hash check karo
    if not Hash.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
        
    # 3. Agar password sahi hai, toh Token generate karo 
    # Hum token mein user ki ID bhej rahe hain ("user_id")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    # 4. Standard format mein token return karo
    return {"access_token": access_token, "token_type": "bearer"}

# Apne CREATE Task wale endpoint ko update karein
@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate, 
    background_tasks: BackgroundTasks, # NAYA: FastAPI ko bola ek background task worker do
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    new_task = models.Task(name=task.name, owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # API response dene se pehle, us kaam ko background mein laga diya
    background_tasks.add_task(write_backup_log, new_task.name, current_user.email)
    
    return new_task

# 2. VIEW Tasks (Secure - Sirf apne tasks dekhne ke liye)
@app.get("/tasks/", response_model=list[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user) # NAYA: Security Guard
):
    # Database se sirf wahi tasks nikalenge jinka owner_id current user ki id se match kare
    user_tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return user_tasks




# # 1. ADD Task (POST Request)
# @app.post("/tasks/", response_model=schemas.TaskResponse)
# def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
#     new_task = Task(name=task.name)
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
#     return new_task

# # 2. VIEW Tasks (GET Request)
# @app.get("/tasks/", response_model=list[schemas.TaskResponse])
# def get_tasks(db: Session = Depends(get_db)):
#     return db.query(Task).all()



# # 3. UPDATE Task (PUT Request)
# @app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
# def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
#     # First, find the task in the database
#     db_task = db.query(Task).filter(Task.id == task_id).first()
    
#     # If the task doesn't exist, return a 404 error
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     # Update the task's data
#     db_task.name = updated_task.name
    
#     # Save changes to the database
#     db.commit()
#     db.refresh(db_task)
#     return db_task

# # 4. DELETE Task (DELETE Request)
# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int, db: Session = Depends(get_db)):
#     # Find the task
#     db_task = db.query(Task).filter(Task.id == task_id).first()
    
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     # Delete the task from the database
#     db.delete(db_task)
#     db.commit()
    
#     # Return a simple success message
#     return {"message": f"Task {task_id} deleted successfully"}

