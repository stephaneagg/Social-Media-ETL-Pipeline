import psycopg2

DBNAME="pgdev"
USER="stephg"
PASSWORD="password"
HOST="localhost"
PORT=5332

def get_connection():
    return psycopg2.connect(
        dbname=DBNAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )


def load_users(conn, users):

  report = {
    "attempted": 0,
    "inserted": 0,
    "failed": 0,
    "skipped": 0
  }

  with conn.cursor() as cur:
    for user in users:
      report["attempted"] += 1

      try:
        cur.execute("""
          INSERT INTO users (id, created_at, username, display_name, email, password_hash, role)
          VALUES (%s, %s, %s, %s, %s, %s, %s)
          ON CONFLICT (id) DO NOTHING
        """, (
          user["id"],
          user["created_at"],
          user["username"],
          user["display_name"],
          user["email"],
          user["password_hash"],
          user["role"]
          )
        )

        if cur.rowcount == 1:
          report["inserted"] += 1
        else:
          report["skipped"] += 1

      except Exception:
        report["failed"] += 1
        raise

  return report


def load_posts(conn, posts):

  report = {
    "attempted": 0,
    "inserted": 0,
    "failed": 0,
    "skipped": 0
  }

  with conn.cursor() as cur:
    for post in posts:
      report["attempted"] += 1

      try:
        cur.execute("""
          INSERT INTO posts (id, user_id, created_at, content_text)
          VALUES (%s, %s, %s, %s)
          ON CONFLICT (id) DO NOTHING
        """, (
          post["id"],
          post["user_id"],
          post["created_at"],
          post["content_text"],
          )
        )

        if cur.rowcount == 1:
          report["inserted"] += 1
        else:
          report["skipped"] += 1

      except Exception:
        report["failed"] += 1
        raise

  return report


def load_comments(conn, comments):

  report = {
    "attempted": 0,
    "inserted": 0,
    "failed": 0,
    "skipped": 0
  }

  with conn.cursor() as cur:
    for comment in comments:
      report["attempted"] += 1

      try:
        cur.execute("""
          INSERT INTO comments (id, post_id, user_id, created_at, content)
          VALUES (%s, %s, %s, %s, %s)
          ON CONFLICT (id) DO NOTHING
        """, (
          comment["id"],
          comment["post_id"],
          comment["user_id"],
          comment["created_at"],
          comment["content"]
          )
        )

        if cur.rowcount == 1:
          report["inserted"] += 1
        else:
          report["skipped"] += 1

      except Exception:
        report["failed"] += 1
        raise

  return report

def load_all(users, posts, comments):
    conn = get_connection()

    try:
        user_report = load_users(conn, users)
        post_report = load_posts(conn, posts)
        comment_report = load_comments(conn, comments)

        conn.commit()

        return {
          "users": user_report,
          "posts": post_report,
          "comments": comment_report,
          "status": "SUCCESS"
        }

    except Exception as e:
        conn.rollback()

        return {
          "status": "FAILED",
          "error": str(e)
        }

    finally:
        conn.close()