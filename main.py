import requests
from bs4 import BeautifulSoup
import re
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from urllib.parse import urljoin


# URL of the page
url = "https://nailib.com/ia-sample/ib-math-ai-sl"

# Sending an HTTP GET request to the website
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Checking if the request was successful
if response.status_code == 200:
    print("Page fetched successfully!")
    html_content = response.text
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# print(soup.prettify())  # Print the HTML to identify relevant elements (for debugging)

# Finding all sample items (by adjusting the class or tag based on the website)
sample_cards = soup.find_all("a", class_="sample_sample__fWsLe")  

data_list = []

# Loop through each sample card
for card in sample_cards:
    # Extract the title (adjust the tag based on the website structure)
    title = card.find("h3").text.strip() if card.find("h3") else "N/A"
   
    # Extract the description (adjust the tag)
    description = card.find("p").text.strip() if card.find("p") else "N/A"
    
    # Extract the content link (adjust the tag)
    content_link = card["href"] if card else "N/A" 
    
    # Define category and subject
    subject = "Math AI SL IA"
    category = "IA" if "IA" in subject else "EE"  #for IA category

    
    # Extracting wordcount , here there are 8 <div> elements within same class
    # Extract all <div> elements with the same class name
    divs = card.find("div", class_="sample_sample__right__stat__5Dbqa").text.strip() if card.find("div", class_="sample_sample__right__stat__5Dbqa") else "N/A"

    #print(divs)  #for debugging

    # Access the 5th <div> (index 4 because Python uses 0-based indexing) as word count is in 4th div
    fifth_div = divs[4] if len(divs) > 4 else None  # Check if at least 5 divs exist
    # Extract the word count (e.g., "4171 words")
    
    match = re.search(r"(\d+)\s*words", divs)  # Look for a number followed by "words"

    if match:
        word_count = match.group(1)  # Extract the numeric part




    # Extracting estimated read time  
    fourth_div = divs[3] if len(divs) > 3 else None  
    # Extract the time (e.g., "21 mins")
    
    match1 = re.search(r"(\d+\s*mins)", divs)  # Look for a number followed by "mins"

    if match1:
        time_count = match1.group(1)  # Extract the numeric part





    # Extract published date
    # Extract the 7th and 8th divs
    match2 = re.search(r"(?:[A-Z][a-z]+)?([A-Z][a-z]+)(\d{4})", divs) # regex pattern

    if match2:
        # Extract the month and year
        month = match2.group(1)
        year = match2.group(2)
        
    
        
    
    # Create a dictionary for this item
    data = {
        "title": title,
        "description": description,
        "content": content_link,
        "category": category,
        "subject": subject,
        "wordcount": word_count,
        "TimeEstimate": time_count,
        "PublicationDate": f"{month} {year}",
        
    }

    
    
    # Append the data to the list
    data_list.append(data)

# Print the extracted data ( for debugging)
for item in data_list:
    print(item)





#importing in the form of json

with open("math_ai_sl_samples.json", "w") as file:
    json.dump(data_list, file, indent=4)






#Connecting the json file to MongoDB database

# Step 1: Read the JSON file
with open('math_ai_sl_samples.json', 'r') as file:  
    data = json.load(file)  # Load the JSON content into a Python list/dictionary

# Step 2: Connect to MongoDB
client = MongoClient("mongodb+srv://user2:user@cluster0.tgkri9n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  #  MongoDB URL
db = client.IB_Samples  # Database name
collection = db.Math_AI_SL  # Collection name

# Step 3: Insert the data into MongoDB
# If you are inserting multiple records (like in the example JSON)
if isinstance(data, list):  # Check if data is a list (i.e., multiple records)
    collection.insert_many(data)
else:  # In case it's a single JSON object
    collection.insert_one(data)

print("Data inserted successfully.")








# To remove duplicate values in MongoDB
# Step 1: Find duplicates based on the field (e.g., "title")
duplicates = collection.aggregate([
    {"$group": {
        "_id": "$title",  # Group by the "title" field (can change to the field we want to check for duplicates)
        "count": {"$sum": 1},
        "docs": {"$push": "$_id"}
    }},
    {"$match": {"count": {"$gt": 1}}}  # Match only documents with duplicates (count > 1)
])

# Step 2: Loop through the duplicates and delete the extra entries
for duplicate in duplicates:
    # Keep the first document and delete the others
    docs_to_delete = duplicate["docs"][1:]  # Keep the first one and delete the rest
    for doc_id in docs_to_delete:
        # Remove duplicates using deleteOne (you can use deleteMany for multiple deletions)
        collection.delete_one({"_id": ObjectId(doc_id)})

