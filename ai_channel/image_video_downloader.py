import os
import requests
from bs4 import BeautifulSoup
import docx  # For reading .docx files

def download_images_from_bing(query, num_images, folder):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Bing search URL for images
    search_url = f"https://www.bing.com/images/search?q={query}&FORM=HDRSC2"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find image elements
    image_elements = soup.find_all('img', {'class': 'mimg'})

    os.makedirs(folder, exist_ok=True)  # Ensure the folder exists

    image_count = 0
    for i, img_element in enumerate(image_elements):
        if image_count >= num_images:
            break

        img_url = img_element.get('src') or img_element.get('data-src')

        if img_url and 'http' in img_url:
            try:
                img_data = requests.get(img_url).content
                with open(f"{folder}/{query.replace(' ', '_')}_{i + 1}.jpg", 'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded {query.replace(' ', '_')}_{i + 1}.jpg")
                image_count += 1
            except Exception as e:
                print(f"Failed to download image {i + 1}: {e}")

    print(f"Downloaded {image_count} images for '{query}'.")

def read_names_from_docx(docx_file):
    # Read the .docx file and extract text content
    doc = docx.Document(docx_file)
    queries = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            queries.append(text)  # Collect non-empty lines

    return queries

def download_images_for_all_queries(docx_file, num_images_per_query, folder="visual"):
    # Read queries from the .docx file
    queries = read_names_from_docx(docx_file)

    # Download images for each query
    for query in queries:
        print(f"Downloading images for: {query}")
        download_images_from_bing(query, num_images_per_query, folder)
    print("All downloads complete.")

# Usage
# Specify the path to your .docx file and the number of images per query
docx_file = "Cooking_Script_2025-01-03.docx"  # Replace with your actual file
num_images_per_query = 10  # Number of images to download per query

# All images will be downloaded to a folder named "visual"
download_images_for_all_queries(docx_file, num_images_per_query)
