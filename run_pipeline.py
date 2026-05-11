
from extract.extract import extract
from transform.normalize_users import normalize_users
from transform.normalize_posts import normalize_posts
from transform.normalize_comments import normalize_comments
from transform.validate import validate_data

def print_report(report):
    print("\n===== ETL PIPELINE REPORT =====\n")

    for section, data in report.items():
        print(f"--- {section.upper()} ---")

        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print(data)

        print()

def print_summary(report):
    total_processed = (
        report["users"]["processed"] +
        report["posts"]["processed"] +
        report["comments"]["processed"]
    )

    total_skipped = (
        report["users"]["skipped"] +
        report["posts"]["skipped"] +
        report["comments"]["skipped"]
    )

    print("===== SUMMARY =====")
    print(f"Total processed: {total_processed}")
    print(f"Total skipped: {total_skipped}")


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

validation_report = validate_data(users, posts, comments)


pipeline_report = {
    "users": user_report,
    "posts": post_report,
    "comments": comment_report,
    "validation": validation_report,
    "status": "SUCCESS" if validation_report["valid"] else "FAILED"
}

print_report(pipeline_report)
print_summary(pipeline_report)