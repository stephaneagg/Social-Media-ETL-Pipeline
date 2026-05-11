# transform/normalize_uers.py

from transform.utils import (
  resolve_field,
  normalize_id,
  normalize_text,
  normalize_email,
  make_timestamp
)

def get_default_comment_user():
  return {
    "id": 0,
    "created_at": make_timestamp(),
    "username": "legacy_user",
    "display_name": "Mysterious User",
    "email": "legacy@system.local",
    "password_hash": "LEGACY_SYSTEM_ACCOUNT",
    "role": "USER"
  }

def create_report():
  """
  returns a blank normalization report
  """
  return {
    "processed": 0,
    "skipped": 0,
    "skip_reasons": []
  }

def normalize_users(users):
  """
  Returns a clean list of normalized users
  users: the list of users that need to be normalized
  """
  normalized_users = []
  report = create_report()

  for user in users:
    normalized_user, reason = normalize_user(user)

    if normalized_user:
      normalized_users.append(normalized_user)
      report["processed"] += 1
    else:
      report["skipped"] += 1
      if reason:
          report["skip_reasons"].append(reason)

  normalized_users.append(get_default_comment_user())
  return normalized_users, report

def normalize_user(user):
  """
  Returns an object representing a user with all attribute normalized
  user: the user being normalized
  """
  # print(user["id"])
  try:
  # Grab all fields (user_id, username, display_name, email)
    user_id = normalize_id(
      resolve_field(user, ["id"])
    )

    username = normalize_text(
      resolve_field(user, ["username", "handle", "userName"])
    )

    display_name = normalize_text(
      resolve_field(user, ["name", "full_name", "displayName"])
    )

    email = normalize_email(
      resolve_field(user, ["email", "emailAddress"])
    )

  # Validate required fields. If invalid skip the record
    if not user_id:
        return None, "missing_or_invalid_id"
    if not username:
        return None, f"user_id={user.get('id')} missing_username"
    if not email:
        return None, f"user_id={user.get('id')} missing_email"

  # return normalized user as JSON object
    return {
      "id" : user_id,
      "created_at": make_timestamp(),
      "username": username,
      "display_name": display_name,
      # "profile_image_url": None,
      # "bio": None,
      "email": email,
      "password_hash": "LEGACY_MIGRATION_PLACEHOLDER",
      "role": "USER"
    }, None

  except Exception as e:
      return None, f"user_id={user.get('id')} exception={str(e)}"

# Testing
# if __name__ == "__main__":
#   import json

#   with open("../legacy-data/users.json") as f:
#     users = json.load(f)

#   normalized_users, user_report = normalize_users(users)

#   print(normalized_users[:2])
#   print(user_report)