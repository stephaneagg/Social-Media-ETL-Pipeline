import requests
import json
from pathlib import Path

BASE_URL = "https://jsonplaceholder.typicode.com"

def fetch(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    response.raise_for_status()
    return response.json()

def save(data, filename):
    Path("../data").mkdir(exist_ok=True)
    with open(f"../data/{filename}", "w") as f:
        json.dump(data, f, indent=2)

def main():
    users = fetch("users")
    posts = fetch("posts")
    comments = fetch("comments")

    save(users, "users.json")
    save(posts, "posts.json")
    save(comments, "comments.json")

    print("Data extracted successfully")

if __name__ == "__main__":
    main()
