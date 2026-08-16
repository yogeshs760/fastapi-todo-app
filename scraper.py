from playwright.sync_api import sync_playwright
import requests

# API Details
API_URL = "http://127.0.0.1:8000"
USER_EMAIL = "test@mail.com"  # Apna test email yahan daalein
USER_PASSWORD = "1234"         # Apna test password yahan daalein

def get_api_token():
    """1. API me login karke JWT token lena"""
    print("Logging into API...")
    login_data = {"username": USER_EMAIL, "password": USER_PASSWORD}
    response = requests.post(f"{API_URL}/login", data=login_data)
    
    if response.status_code == 200:
        print("Login Successful!")
        return response.json().get("access_token")
    else:
        print("Login Failed:", response.text)
        return None

def scrape_and_save(token):
    """2. Playwright se data scrape karna aur API me bhejna"""
    # Token ko HTTP Headers mein set karna (Security mechanism)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("Starting Playwright Scraper...")
    with sync_playwright() as p:
        # Browser open karna (headless=False se aapko browser khulta hua dikhega)
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        
        # Test website par jana
        page.goto("http://quotes.toscrape.com/")
        
        # Elements ko locate karna aur text nikalna
        quotes = page.locator(".text").all_inner_texts()
        
        print(f"Found {len(quotes)} items. Saving to Database via API...")
        
        # Shuru ke 5 quotes ko as a Task save karna
        for quote in quotes[:5]:
            # Hamari API schemas.TaskCreate ke hisaab se sirf 'name' expect karti hai
            task_data = {"name": quote} 
            
            # API par POST request bhejna secure headers ke sath
            res = requests.post(f"{API_URL}/tasks/", json=task_data, headers=headers)
            
            if res.status_code == 200:
                print(f"Saved: {quote[:30]}...")
            else:
                print(f"Error saving: {res.text}")
                
        browser.close()
        print("Data Extraction Complete!")

# Script ko chalane ka main flow
if __name__ == "__main__":
    jwt_token = get_api_token()
    
    if jwt_token:
        scrape_and_save(jwt_token)