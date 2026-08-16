from fastapi.testclient import TestClient
from main import app
import random
import string

# FastAPI ka inbuilt TestClient humari app ka ek nakli (virtual) server bana dega
client = TestClient(app)

def test_login_wrong_credentials():
    """Test karna ki galat password dalne par API sahi error de rahi hai ya nahi"""
    
    # Hum galat email aur password ke sath login request bhejenge
    response = client.post("/login", data={"username": "wrong@user.com", "password": "wrongpassword"})
    
    # 'assert' ka matlab hai "Main dawa karta hu ki..."
    # 1. Main dawa karta hu ki status code 403 (Forbidden/Error) aana chahiye
    assert response.status_code == 403
    
    # 2. Main dawa karta hu ki response mein "Invalid Credentials" likha hona chahiye
    assert response.json()["detail"] == "Invalid Credentials"

def test_unauthorized_task_access():
    """Test karna ki bina token ke tasks access karne par block ho jaye"""
    
    # Bina login/token ke /tasks/ par GET request bhejenge
    response = client.get("/tasks/")
    
    # Kyunki yeh secured endpoint hai, status code 401 (Unauthorized) aana chahiye
    assert response.status_code == 401


    # second test

# ... (Aapke upar ke purane tests) ...

def test_create_user_login_and_create_task():
    """End-to-End Test: User banayein, Token lein, aur Task create karein"""
    
    # 1. Ek random aur unique email banana (taaki baar-baar test run karne par error na aaye)
    random_string = ''.join(random.choices(string.ascii_lowercase, k=6))
    test_email = f"testuser_{random_string}@gmail.com"
    test_password = "supersecretpassword"

    # ==========================================
    # STEP 1: CREATE USER
    # ==========================================
    response_user = client.post(
        "/users/", 
        json={"email": test_email, "password": test_password}
    )
    # Check karein ki user successfully ban gaya (Status 200)
    assert response_user.status_code == 200, "User create nahi hua"
    
    # ==========================================
    # STEP 2: LOGIN & GET TOKEN
    # ==========================================
    # Note: FastAPI ka OAuth2 login 'json' nahi, balki Form 'data' accept karta hai
    response_login = client.post(
        "/login", 
        data={"username": test_email, "password": test_password}
    )
    assert response_login.status_code == 200, "Login fail ho gaya"
    
    # Response se token nikalna
    token = response_login.json().get("access_token")
    assert token is not None, "Token generate nahi hua"

    # ==========================================
    # STEP 3: CREATE TASK (Secure Endpoint)
    # ==========================================
    # Token ko HTTP Headers mein 'Bearer' ke sath add karna
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Task ka data
    task_data = {"name": "Test integration task for portfolio"}
    
    response_task = client.post(
        "/tasks/", 
        json=task_data, 
        headers=headers
    )
    
    # Check karein ki task securely ban gaya
    assert response_task.status_code == 200, "Secure task create nahi hua"
    
    # Check karein ki jo task humne bheja tha, wahi save hua hai
    assert response_task.json()["name"] == "Test integration task for portfolio"
    
    print("Integration Test Passed! User created, logged in, and task saved.")