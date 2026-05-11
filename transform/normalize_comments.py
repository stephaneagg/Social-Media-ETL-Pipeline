# transform/normalize_comments.py

from transform.utils import (
  resolve_field,
  normalize_id,
  normalize_text,
  make_timestamp
)

DEFAULT_COMMENT_USER_ID = 0

def create_report():
    """
    returns a blank normalization report
    """
    return {
        "processed": 0,
        "skipped": 0,
        "skip_reasons": []
    }

def normalize_comments(comments, valid_user_ids, valid_post_ids):
  """
  Returns a clean list of normalized comments
  valid_user_ids: list of valid user_ids that user_id can map to
  valid_post_ids: list of valid post_ids that post_id can map to
  """
  normalized_comments = []
  report = create_report()

  for comment in comments:
    normalized_comment, reason = normalize_comment(comment, valid_user_ids, valid_post_ids)

    if normalized_comment:
      normalized_comments.append(normalized_comment)
      report["processed"] += 1
    else:
        report["skipped"] += 1
        if reason:
            report["skip_reasons"].append(reason)


  return normalized_comments, report


def normalize_comment(comment, valid_user_ids, valid_post_ids):
  """
  Returns an object representing a comment with all attributes normalized
  valid_user_ids: list of valid user_ids that user_id can map to
  valid_post_ids: list of valid post_ids that post_ids can map to
  """

  try:

    comment_id = normalize_id(
      resolve_field(comment, ["id"])
    )

    post_id = normalize_id(
      resolve_field(comment, ["postId", "post_id"])
    )

    user_id = normalize_id(
      resolve_field(comment, ["userId", "user_id"])
    )

    content = normalize_text(
      resolve_field(comment, ["body", "content", "text"])
    )

    if not comment_id:
        return None, "missing_comment_id"

    if not post_id:
        return None, f"comment_id={comment_id} missing_post_id"

    if post_id not in valid_post_ids:
        return None, f"comment_id={comment_id} invalid_post_id={post_id}"

    # User_id will always be None since legacy data does not include it. Use to default user id
    if user_id is None:
        user_id = DEFAULT_COMMENT_USER_ID

    if user_id not in valid_user_ids:
        return None, f"comment_id={comment_id} invalid_user_id={user_id}"

    if not content:
        return None, f"comment_id={comment_id} missing_content"

    return {
      "id": comment_id,
      "post_id": post_id,
      "user_id": user_id,
      "created_at": make_timestamp(),
      "content": content
    }, None

  except Exception as e:
      return None, f"comment_id={comment.get('id')} exception={str(e)}"



# Testing
# if __name__ == "__main__":
#   import json

#   with open("../legacy-data/comments.json") as f:
#     comments = json.load(f)

#   normalized_comments, report = normalize_comments(
#     comments,
#     {0, 1, 2},
#     {1, 2, 3}
#   )

#   print(normalized_comments[:2])
#   print(report)