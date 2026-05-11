# transform/validate.py

# Required schema fields for each entity.
REQUIRED_USER_FIELDS = {
    "id",
    "created_at",
    "username",
    "email",
    "password_hash",
    "role"
}

REQUIRED_POST_FIELDS = {
    "id",
    "user_id",
    "created_at",
    "content_text"
}

REQUIRED_COMMENT_FIELDS = {
    "id",
    "post_id",
    "user_id",
    "created_at",
    "content"
}

def validate_required_fields(records, required_fields, entity_name, report):
    """
    returns None
    records: the list of normalized records being validated
    required_fields: the set of required keys for the entity
    entity_name: the name of the entity being validated
    report: the validation report being updated
    """
    for record in records:
        missing = required_fields - record.keys()

        if missing:
            report["valid"] = False
            report["errors"].append(
                f"{entity_name}_id={record.get('id')} missing_fields={list(missing)}"
            )

def validate_data(users, posts, comments):
    """
    returns a validation report describing dataset integrity
    users: the normalized list of users
    posts: the normalized list of posts
    comments: the normalized list of comments
    """
    report = {
        "valid": True,
        "errors": []
    }

    user_ids = {u["id"] for u in users}
    post_ids = {p["id"] for p in posts}
    comment_ids = set()

    # -----------------------
    # Required field checks
    # -----------------------
    validate_required_fields(
        users,
        REQUIRED_USER_FIELDS,
        "user",
        report
    )

    validate_required_fields(
        posts,
        REQUIRED_POST_FIELDS,
        "post",
        report
    )

    validate_required_fields(
        comments,
        REQUIRED_COMMENT_FIELDS,
        "comment",
        report
    )

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