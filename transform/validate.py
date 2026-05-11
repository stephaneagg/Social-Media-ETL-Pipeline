# transform/validate.py

def validate_data(users, posts, comments):
    report = {
        "valid": True,
        "errors": []
    }

    user_ids = {u["id"] for u in users}
    post_ids = {p["id"] for p in posts}
    comment_ids = set()


    # Duplicate ID checks
    if len(user_ids) != len(users):
        report["valid"] = False
        report["errors"].append("duplicate_user_ids_detected")

    if len(post_ids) != len(posts):
        report["valid"] = False
        report["errors"].append("duplicate_post_ids_detected")


    # FK check
    for post in posts:
        if post["user_id"] not in user_ids:
            report["valid"] = False
            report["errors"].append(
                f"invalid_post_user_id post_id={post['id']} user_id={post['user_id']}"
            )


    # Comment integrity
    for comment in comments:

        # Duplicate check
        if comment["id"] in comment_ids:
            report["valid"] = False
            report["errors"].append(f"duplicate_comment_id={comment['id']}")
        comment_ids.add(comment["id"])

        # FK checks
        if comment["user_id"] not in user_ids:
            report["valid"] = False
            report["errors"].append(
                f"invalid_comment_user_id comment_id={comment['id']} user_id={comment['user_id']}"
            )

        if comment["post_id"] not in post_ids:
            report["valid"] = False
            report["errors"].append(
                f"invalid_comment_post_id comment_id={comment['id']} post_id={comment['post_id']}"
            )

    return report