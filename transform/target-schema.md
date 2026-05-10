# Target Schema Definition
The following defines the target database as well as exactly how the transformed records should look like

## Users Table
### Database Schema
| Column | Required | Description |
| :--- | :--- | :--- |
| Id | Yes | Primary Key |
| created_at | Yes (created at insertion) | Account creation timestamp |
| username | Yes | Unique user handle |
| display_name | No | User-visible handle |
| profile_image_url | No | Profile Picture |
| bio | No | User profile description |
| email | Yes | User email |
| password_hash | Yes | Authentication credential |
| role | No | User authorization role |

### User Transform Output
```
{
  "id": 1,
  "username": "bret",
  "display_name": "Leanne Graham",
  "profile_image_url": null,
  "bio": null,
  "email": "sincere@april.biz",
  "password_hash": "<generated>",
  "role": "USER"
}
```

## Posts Table

### Database Schema
| Column | Required | Description |
| :--- | :--- | :--- |
| Id | Yes | Primary Key |
| user_id | Yes | FK -> users.id |
| created_at | Yes (created at insertion) | Post timestamp |
| image_url | No | Optional media |
| content_text | No | Post Content |

### Transformation Output
```
{
  "id": 1,
  "user_id": 1,
  "content_text": "Post body..."
}
```


## Comments Table

### Datanase Schema
| Column | Required | Description |
| :--- | :--- | :--- |
| Id | Yes | Primary Key |
| user_id | Yes | FK -> users.id |
| post_id | Yes | FK -> posts.id |
| created_at | Yes (created at insertion) | Comment timestamp |
| content | No | Comment body |

### Transformation Output
```
{
  "id": 1,
  "post_id": 1,
  "user_id": 1,
  "content": "Comment body"
}
```