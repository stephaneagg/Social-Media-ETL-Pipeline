# transform/normalize_comments.py

from utils import (
  resolve_field,
  normalize_id,
  normalize_text,
  normalize_email,
  make_timestamp
)

DEFAULT_COMMENT_USER_ID = 0

def normalize_comments(comments):
  normalized_comments = []

  for comment in comments:
    normalized_comment = normalize_comment(comment)

    if normalized_comment:
      normalized_comments.append(normalized_comment)

  return normalized_comments


def normalize_comment(comment):

  try:

    comment_id = normalize_id(
      resolve_field(comment, ["id"])
    )

    post_id = normalize_id(
      resolve_field(comment, ["postId"])
    )

    content = normalize_text(
      resolve_field(comment, ["body"])
    )

    if not comment_id or not post_id:
      return None

    return {
      "id": comment_id,
      "post_id": post_id,
      "user_id": DEFAULT_COMMENT_USER_ID,
      "created_at": make_timestamp(),
      "content": content
    }

  except Exception:
    return None

# Testing
if __name__ == "__main__":
  import json

  with open("../legacy-data/comments.json") as f:
    comments = json.load(f)

  normalized_comments = normalize_comments(comments)

  print(normalized_comments[:2])