import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def download_image(url, folder_path, image_name):
    response = requests.get(url)
    with open(os.path.join(folder_path, image_name), 'wb') as file:
        file.write(response.content)

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    profile_path = "/Users/alexanderqueiroz/Library/Application Support/Google/Chrome/Default"
    chrome_options.add_argument(f"user-data-dir={profile_path}")

    return webdriver.Chrome(options=chrome_options)

driver = initialize_driver()
driver.get("https://www.instagram.com/")
profile = input("Digite o perfil do Instagram para buscar as imagens: ")

try:
    driver.get(f"https://www.instagram.com/{profile}/")
except:
    driver.quit()
    driver = initialize_driver()
    driver.get(f"https://www.instagram.com/{profile}/")

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height
    except:
        driver.quit()
        driver = initialize_driver()
        driver.get(f"https://www.instagram.com/{profile}/")
        driver.execute_script(f"window.scrollTo(0, {last_height});")

images = driver.find_elements(By.CSS_SELECTOR, "article img")
folder_name = profile

if not os.path.exists(folder_name):
    os.mkdir(folder_name)

with open(f"links_{profile}.txt", "w") as file:
    delay = 1
    for i, img in enumerate(images):
        image_link = img.get_attribute('src')
        
        if image_link:
            print(f"Imagem {i+1}: {image_link}")
            file.write(image_link + '\n')
            image_name = f"image_{i+1}.jpg"
            download_image(image_link, folder_name, image_name)
            time.sleep(delay)
            delay += 1.5
        else:
            print(f"Imagem {i+1} não tem um link SRC válido. Aguardando 1 segundo e seguindo para a próxima.")
            time.sleep(1)

print(f"Links salvos em links_{profile}.txt e imagens baixadas para a pasta {folder_name}/")
driver.quit()
