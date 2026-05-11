# Legacy Data Inconsistencies to Resolve

## Schema Drift Resolution
Field names vary across records. Transform logic must resolve multiple aliases.

### User Field Resolution
| Canonical Field | Legacy Variants |
| :--- | :--- |
| username | username, handle, userName |
| display_name | name, full_name, displayName |
| email | email, emailAddress |

### Post Field Resolution
| Canonical Field | Legacy Variants |
| :--- | :--- |
| user_id | userId, authorId, user_id |

## Data Type Normalization
Legacy IDs may be ` 1 or "1"`. Transform logic must resolve all IDs (user IDs, post IDs, comment IDs and foreign keys) to integers

## Missing / Partial Data Handling
All data fields in the legacy data are not promised. Transormation logic should handle missing or invalid data.

**If a required field is missing:**
- Skip record or generate default
- Log error

**If an optional field is missing:**
- Set value of None or generate default
- In the case of image_url, profile_image_url and bio, they do not exist in the legacy data. Omit them in the transformation and a null value will be assigned at insertion.

**Generated defaults**
- created_at
  - Generate synthetic timestamp of current time at runtime
- password_hash
  - Generate placeholder hash: `"LEGACY_MIGRATION_PLACEHOLDER"`
- role
  - Generate default value: `"USER"`
- user_id
  - In the comments data, since a user_id is not specified a default user_id 0 will be used

### User Rules
**Required:**
- id
- username
- email

**Optional:**
- display_name
- profile_image_url
- bio

### Post Rules
**Required:**
- id
- user_id

**Optional:**
- created_at
- image_url

### Comment Rules
**Required:**
- id
- post_id
- user_id
- created_at

**Optional:**
- content

## Formatting Normalization
Legacy data does not guarantee formatting consistency. Transformation logic should resolve textual inconsistencies

**Email Normalization:**
The email field in user data should be normalized to resolve inconsistent capitalization

**Text Normalization:**
Text fields (display_name, post content, comments) should be normalized to remove whitespace

## Comment Author Attribution Handling
The legacy comment data does not contain a user_id field, while the target database schema requires every comment to reference an existing user through a foeign key constraint.

To preserve all comment records during migration while maintaining referential integrity, the transformation pipeline creates a defailt system user during the user normalization stage.

**Default User Record:**
```
{
  "id": 0,
  "created_at": <generated>,
  "username": "legacy_user",
  "display_name": "Mysterious User",
  "email": "legacy@system.local",
  "password_hash": "LEGACY_SYSTEM_ACCOUNT",
  "role": "USER"
}
```

**Transformation Rule:**
<br>All normalized comment records are assigned:
```
"user_id": 0
```

**Rationale:**

This approach was selected because it:
- preserves all legacy comment data
- satisfies foreign key constraints in the target schema
- avoids generating artificial user-to-comment relationships
- clearly identifies comments with unknown original authorship

## Relationship Validation
Since the target database schema enforces foreign keys, entity relationships must be valid

### Posts
Validate:
```
post.user_id must exist
comment.post_id must exist
comment.user_id must exist
```
If invalid, skip the entry

## Transform Execution Order
Because of dependencies, the transformation pipeline must execute in the following order

1) Transform Users
2) Transform Posts
3) Transform Comments


## Validation
Perform global integrity checks on all tranformed data before moving on to insertion
- Ensure all foreign keys are valid
- Detect duplicates

## Transformation Summary Report
The following is generated at completion:
```
===== ETL PIPELINE REPORT =====

--- USERS ---
processed: X
skipped: X
skip_reasons: [X]

--- POSTS ---
processed: X
skipped: X
skip_reasons: [X]

--- COMMENTS ---
processed: X
skipped: X
skip_reasons: [X]

--- VALIDATION ---
valid: X
errors: [X]
```