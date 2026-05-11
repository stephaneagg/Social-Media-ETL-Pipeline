

from transform.normalize_users import normalize_users
from transform.normalize_posts import normalize_posts
from transform.normalize_comments import normalize_comments
from extract.extract import extract


raw_users = extract("legacy-data/users.json")
raw_posts = extract("legacy-data/posts.json")
raw_comments = extract("legacy-data/comments.json")


users, user_report = normalize_users(raw_users)
valid_user_ids = {u["id"] for u in users}

posts, post_report = normalize_posts(raw_posts, valid_user_ids)

post_ids = {p["id"] for p in posts}

comments, comment_report = normalize_comments(
    raw_comments,
    valid_user_ids,
    post_ids
)

print(user_report)
print(post_report)
print(comment_report)
