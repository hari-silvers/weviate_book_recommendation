import os
import csv
import weaviate
from pathlib import Path
from time import sleep
from dotenv import load_dotenv

env_var = Path(__file__).resolve().parent.parent
load_dotenv(env_var/ '.env')

WEAVIATE_CLUSTER_URL = os.getenv('WEAVIATE_CLUSTER_URL')
WEAVIATE_API_KEY = os.getenv('WEAVIATE_API_KEY')
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

client = weaviate.Client(
    url=WEAVIATE_CLUSTER_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),
    additional_headers={"X-Cohere-Api-Key": COHERE_API_KEY})

# client.schema.delete_class("Book")

class_obj = {
    "class": "Book",
    "vectorizer": "text2vec-cohere",
      
}

# client.schema.create_class(class_obj)

# Open the CSV file for reading
input_file_path = "C:\\Users\\Trainee\\PycharmProjects\\weaviate_recommendation\\BookRecs\\data-pipeline\\7k-books-kaggle.csv"
csvfile = open(input_file_path, "r", encoding='utf-8') 
initial = 1100
try:
    with client.batch as batch:
        batch.configure(batch_size=10)
        reader = csv.reader(csvfile)
        for count, book in enumerate(reader, start=1):
            # Assuming the CSV columns are as you described
            properties = {
                "isbn13": book[0],
                "isbn10": book[1],
                "title": book[2],
                "subtitle": book[3],
                "authors": book[4],
                "categories": book[5],
                "thumbnail": book[6],
                "description": book[7],
                "published_year": book[8],
                "average_rating": (book[9]),  # Assuming average_rating is a float
                "num_pages": (book[10]),  # Assuming num_pages is an integer
                "ratings_count": (book[11])  # Assuming ratings_count is an integer
            }
            if count < initial:
                continue
            if count == initial + 100:
                break
            else:
                batch.add_data_object(properties, class_name="Book")
                print(f"{book[2]}: {count}")
        sleep(60)
        initial += 100

except Exception as e:
    print(f"Something happened: {e}. Failure at book {count}")

# Close the CSV file
csvfile.close()
