# transform/normalize_posts.py

from transform.utils import (
  resolve_field,
  normalize_id,
  normalize_text,
  normalize_email,
  make_timestamp
)

def create_report():
    return {
        "processed": 0,
        "skipped": 0,
        "skip_reasons": []
    }

def normalize_posts(posts, valid_user_ids):
  """
  Returns a clean list of normalized posts
  posts: the list of posts that need to be normalized
  valid_user_ids: list of valid user_ids that user_id can map to
  """
  normalized_posts = []
  report = create_report()

  for post in posts:
    normalized_post, reason = normalize_post(post, valid_user_ids)

    if normalized_post:
      normalized_posts.append(normalized_post)
      report["processed"] += 1
    else:
      report["skipped"] += 1
      if reason:
          report["skip_reasons"].append(reason)

  return normalized_posts, report

def normalize_post(post, valid_user_ids):
  """
  Returns an object representing a post with all attribute normalized
  post: the post being normalized
  valid_user_ids: list of valid user_ids that user_id can map to
  """
  try:
    user_id = normalize_id(
      resolve_field(post, ["user_id", "authorId", "userId"])
    )

    post_id = normalize_id(
      resolve_field(post, ["id"])
    )

    content_text = normalize_text(
      resolve_field(post, ["body", "content", "text"])
    )

  # Validate required fields. If invalid skip the record
    if not post_id:
        return None, "missing_post_id"

    if not user_id:
        return None, f"post_id={post_id} missing_user_id"

    if user_id not in valid_user_ids:
        return None, f"post_id={post_id} invalid_user_id={user_id}"

    return {
      "id": post_id,
      "user_id": user_id,
      "created_at": make_timestamp(),
      "content_text": content_text
    }, None

  except Exception as e:
      return None, f"post_id={post.get('id')} exception={str(e)}"

# Testing
# if __name__ == "__main__":
#   import json

#   with open("../legacy-data/posts.json") as f:
#     posts = json.load(f)

#   normalized_posts = normalize_posts(posts)

#   print(normalized_posts[:2])