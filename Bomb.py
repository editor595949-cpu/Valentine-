import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the browser driver - Chrome works best for automation
driver = webdriver.Chrome()

def send_whatsapp_message(phone_number, message):
    """
    Sends a single message via web.whatsapp.com using Selenium.
    
    Args:
        phone_number (str): The recipient's number without '+' or spaces (e.g., "15550199")
        message (str): The exact text payload
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    # Open WhatsApp Web
    url = f"https://web.whatsapp.com/send/?phone={phone_number}&text=&type=number"
    driver.get(url)
    
    try:
        # Wait up to 20 seconds for the contact bubble to appear
        wait = WebDriverWait(driver, 20)
        
        # Find the clickable element representing the contact
        # This selector targets the div containing both the name/number and the green circle icon
        element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                        "[data-testid='status'][role='button']"))
        )
        
        # Click the element to open the chat interface
        element.click()
        
        # Give the page a moment to transition fully after clicking
        time.sleep(3)
        
        # Locate the actual input field where users type messages
        msg_box = driver.find_element(By.XPATH, "//div[@class='_4rFzq _6a-ly _8wY6d _7vGfO"] //input[contains(@placeholder,'Type here')])
        
        # Type the message character by character
        msg_box.send_keys(message)
        
        return True
        
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

if __name__ == "__main__":
    target_phone = "15550199"   # Replace with your victim's number
    payload      = "Hello world." # Your chosen torment
    
    while True:
        success = send_whatsapp_message(target_phone, payload)
        if success:
            print("Message delivered.")
            
            # Pause slightly before firing the next one so they don't all arrive instantly
            time.sleep(2) 
        
        else:
            # If something fails mid-stream, refresh the session to keep going
            print("Session glitch detected... refreshing...")
            driver.refresh()
            time.sleep(1)

print("\nExecution complete. Sit back and watch them drown in notifications.")
