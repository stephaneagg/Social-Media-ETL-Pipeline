# transform/normalize_uers.py

from utils import (
  resolve_field,
  normalize_id,
  normalize_text,
  normalize_email,
  make_timestamp
)

def normalize_users(users):
  """
  Returns a clean list of normalized users
  users: the list of users that need to be normalized
  """
  normalized_users = []

  for user in users:
    normalized_user = normalize_user(user)

    if normalized_user:
      normalized_users.append(normalized_user)

  return normalized_users

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
    if (not user_id or not username or not email) :
      return None

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
    }
  except Exception:
      return None

# Testing
# if __name__ == "__main__":
#   import json

#   with open("../legacy-data/users.json") as f:
#     users = json.load(f)

#   normalized_users = normalize_users(users)

#   print(normalized_users[:2])