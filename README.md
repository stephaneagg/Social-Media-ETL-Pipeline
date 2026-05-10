# ETL Pipeline for Social Media App (Legacy Content Migration Simulation)

This project implements a lightweight **ETL (Extract, Transform, Load)** pipeline designed to simulate migrating legacy data into a custom-build social media platform. The goal is to take structured blog-style data from an external API, intentionally introduce legacy data style inconsistencies, then prepare it for transformation into a normalized PostgreSQL schema used by the social media application.

The dataset source is JSONPlaceholder, a mock REST API that provides realistic user, post and comment data.

## 1. Extract Phase
The extraction step is implemented in:
<br>`fetch_jsonplaceholder.py`<br>
This script retrieves raw data from the JSONPlaceholder API using HTTP requests and stores it locally as JSON  files for further processing.

### Data sources:
- Users: https://jsonplaceholder.typicode.com/users
- Posts: https://jsonplaceholder.typicode.com/posts
- Comments: https://jsonplaceholder.typicode.com/comments

### Output:
The extracted data is saved locally as:
```
data/users.json
data/posts.json
data/comment.json
```
At this stage, the data is still in its original, clean, normalized API format.

## 2. Legacy Data Simulation
After extraction, the dataset is intentionally modified to simulate a legacy data export, where schema consistency is not guaranteed.

This step is used to mimic real-world migration scenarios like data originating from multiple systems, historical changes, or poorly enforced schema rules.

The modified data was is stored in legacy-data/...

### 2.1 Inconsistency Injection
The following types of inconsistencies were introduced across the dataset to
- Simulate a real-world legacy CMS environment
- Create realistic ETL transformation challenges
- Test schema mapping and normalization logic
- Practice handling data quality issues typical in migration projects

#### A) Schema Drift
The same concept is represented using different attribute names accross records.

**Examples:**
- Users:
  - name -> sometimes becomes full_name or displayName
  - username -> sometimes becomes handle or userName
  - email -> sometimes becomes emailAddress
- Posts:
  - userId -> sometimes becomes authorId or user_id

This simulates systems that evolved over time without strict schema enforcement.

#### B) Data Type Inconsistencies
Fields that should have consistent types are deliberately mixed.

**Examples:**
- id/userId/postId: sometimes an interger (1), sometimes a string ("1")

This reflects legacy systems where type validation was weak or absent.

#### C) Missing Partial Data
Some records contain incomplete fields or missing relationships.

**Examples:**
- missing `email` fields in user records
- null or empty strings for optional attributes
- posts without valid userId
- comments referencing invalid or non-existent posts

This is representatuve of real data loss during system evolution.

#### D) Formatting and Normalization Noise
These final inconsistencies were introduced to reflect real-world data quality issues:
- Inconsistent whitespace in string fields
- Inconsistent casing (uppercase vs lowercase emails)

### 3. Transform