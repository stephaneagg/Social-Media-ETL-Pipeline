# transform/normalize_posts.py

from utils import (
  resolve_field,
  normalize_id,
  normalize_text,
  normalize_email
)

def normalize_posts(posts):
  """
  Returns a clean list of normalized posts
  posts: the list of posts that need to be normalized
  """
  normalized_posts = []

  for post in posts:
    normalized_post = normalize_post(post)

    if normalized_post:
      normalized_posts.append(normalized_post)

  return normalized_posts

def normalize_post(post):
  """
  Returns an object representing a post with all attribute normalized
  post: the post being normalized
  """
  try:
    user_id = normalize_id(
      resolve_field(post, ["user_id", "authorId", "userId"])
    )

    post_id = normalize_id(
      resolve_field(post, ["id"])
    )

    content_text = normalize_text(
      resolve_field(post, ["body"])
    )

    if not user_id or not post_id:
      return None

    return {
      "id": post_id,
      "user_id": user_id,
      "content": content_text
    }

  except Exception:
    return None


if __name__ == "__main__":
  import json

  with open("../legacy-data/posts.json") as f:
    posts = json.load(f)

  normalized_posts = normalize_posts(posts)

  print(normalized_posts[:2])