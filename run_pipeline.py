# run_pipeline.py

from extract.extract import extract
from transform.normalize_users import normalize_users
from transform.normalize_posts import normalize_posts
from transform.normalize_comments import normalize_comments
from transform.validate import validate_data
from load.load import load_all

def print_transform_report(report):
    print("\n===== ETL PIPELINE REPORT =====\n")

    for section, data in report.items():
        print(f"--- {section.upper()} ---")

        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print(data)

        print()

def print_transform_summary(report):
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


def print_load_report(report):
    print("\n===== LOAD REPORT =====")

    if report["status"] == "FAILED":
        print(f"FAILED: {report['error']}")
        return

    for entity in ["users", "posts", "comments"]:
        r = report[entity]

        print(f"\n{entity.upper()}")
        print(f"Attempted: {r['attempted']}")
        print(f"Inserted:  {r['inserted']}")
        print(f"Skipped:   {r['skipped']}")
        print(f"Failed:    {r['failed']}")


# extract raw data
raw_users = extract("legacy-data/users.json")
raw_posts = extract("legacy-data/posts.json")
raw_comments = extract("legacy-data/comments.json")

# normalize users and prepare list of valid user IDs
users, user_report = normalize_users(raw_users)
valid_user_ids = {u["id"] for u in users}

# normalize posts and prepare list of valid post IDs
posts, post_report = normalize_posts(raw_posts, valid_user_ids)
post_ids = {p["id"] for p in posts}

# normalize comments
comments, comment_report = normalize_comments(
    raw_comments,
    valid_user_ids,
    post_ids
)

# Validate the transformed data
validation_report = validate_data(users, posts, comments)

# log transformation results
pipeline_report = {
    "users": user_report,
    "posts": post_report,
    "comments": comment_report,
    "validation": validation_report,
    "status": "SUCCESS" if validation_report["valid"] else "FAILED"
}
print_transform_report(pipeline_report)
print_transform_summary(pipeline_report)



load_report = load_all(users, posts, comments)

print_load_report(load_report)