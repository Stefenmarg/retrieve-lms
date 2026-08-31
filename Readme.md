# Retrive-LMS

Retrieve-LMS is a learning platform for both educators and learners. This platform will be using Narrow (task-specific) Large Language Models (LLMs) and a Retrieval-Augmented (RAG) System . These technologies will be used for generative and non-generative automations for the platform.

## Prerequisites
 * Docker & Docker Compose
 * Python 3.14
 * PostgreSQL (or use Docker Compose stack)

## Database setup; schema and user
This platform will be using a PostgreSQL Database (preferably version 17.0+) and it will connect using the *psycopg* database adapter. Manual setup of the database will not be needed since seeding of the database will be done automatically at first launch.

You will need to create a `user` and a `schema` for the platform, using the following commands:

```postgre
-- Create the database with an owner that you can use for migrations or schema changes
CREATE USER retrieve_admin WITH PASSWORD '<your-secure-password>';
CREATE DATABASE retrieve_app OWNER retrieve_admin;

-- Create the back-end user
CREATE USER retrieve WITH PASSWORD '<backends-secure-password>';

-- Connect to the database
\c retrieve_app;

-- Grant ONLY CRUD permissions
GRANT CONNECT ON DATABASE retrieve_app TO retrieve;
GRANT USAGE ON SCHEMA public TO retrieve;

-- Apply CRUD permissions on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO retrieve;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO retrieve;

-- Apply CRUD permissions on future tables too
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO retrieve;

ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT USAGE ON SEQUENCES TO retrieve;
```

After setup of the admin the the backend user for the retrieve-lms platform you will need to put the values in the `.env` file. Specifically the user, user password, database host, optionally the database name if it is not `retrieve` and optionally the port the postgre database is listening on if not listening on the default `5432` port

Finally, you will **need** to add the user in the `pg_hba.conf` at the end of the file else you will be unable to login and execute anything. Suggested format is as follows but you shouldn't use `0.0.0.0/0` in production due to being the `*` on the connection address which allow connecting to the account from any address:
```bash
host    retrieve_app    retrieve        0.0.0.0/0               scram-sha-256
```