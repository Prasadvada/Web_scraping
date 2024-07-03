

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
# Add any desired options to chrome_options

# Create a Service object for ChromeDriver
# chrome_service = Service(ChromeDriverManager(version="latest").install())

driver = webdriver.Chrome(ChromeDriverManager(version="87.0.4280.88").install())
driver.get("https://www.google.com")



# Create a WebDriver instance using the Service object and options
# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
# url = "https://www.example.com/download-link"  # Replace with the actual download URL
# driver.get(url)
# Remember to quit the driver when you're done
driver.quit()
# Now you can use the 'driver' instance as before
