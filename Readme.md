Retrieve-LMS
============

Retrieve-LMS is a learning platform for both educators and learners. This platform will be using Narrow (task-specific) Large Language Models (LLMs) and a Retrieval-Augmented (RAG) System . These technologies will be used for generative and non-generative automations for the platform.

1\. Prerequisites
-----------------

*   Docker & Docker Compose
    
*   Python 3.14
    
*   PostgreSQL (or use Docker Compose stack)
    

2\. Database Setup; Schema and User
-----------------------------------

This platform will be using a PostgreSQL Database (preferably version 17.0+) and it will connect using the _psycopg_ database adapter. Manual setup of the database will not be needed since seeding of the database will be done automatically at first launch.

You will need to create a `user` and a `schema` for the platform, using the following commands:

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

After setup of the admin the backend user for the retrieve-lms platform you will need to put the values in the `.env` file. Specifically the user, user password, database host, optionally the database name if it is not `retrieve` and optionally the port the postgre database is listening on if not listening on the default `5432` port

Finally, you will **need** to add the user in the `pg_hba.conf` at the end of the file else you will be unable to login and execute anything. Suggested format is as follows but you shouldn't use `0.0.0.0/0` in production due to being the `*` on the connection address which allow connecting to the account from any address:

    host    retrieve_app    retrieve        0.0.0.0/0               scram-sha-256

**3\. Environment Variables; What Do They Do and Mean**
-------------------------------------------------------

This platform uses one variable file for both the frontend and the backend but due to the settings inside the configuration file of each part only those defined entries are assigned in the settings variable. The following code snippet is part of both configuration files.

    model_config = {
        "env_file": Path(__file__).resolve().parents[2] / ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }

It provides the path to the environment file that is in the root of the repo, it ignores case sensitivity and ignores extra entries in the file that aren't inside Settings class.

### **3.1 Frontend Variables**

The variables for the frontend are:

1.  **app\_name**: The name of the application, in this case the name of the platform "Retrieve"
    
2.  **app\_debug**: If the app is in debug mode. Debug mode allows printing responses and their statuses as well as reloading files on content change.
    
3.  **app\_demo**: If the app is in demo mode. Demo mode allows creating an account with higher permissions, which as of this time is an admin account.
    
4.  **app\_address**: The host or hostname the app is hosted under. In our case for local development we have localhost:8001 and for production [retrieve-lms.stefenmarg.com](http://retrieve-lms.stefenmarg.com).
    
5.  **storage\_secret**: The password or secret used to sign the data in the secure storage that NiceGUI uses. It does have a field validator that does not allow launch of the app without one and throws a warning if the length of the secret is not greater or equal than 32 characters.
    
6.  **timeout\_time\_httpx\_seconds: The time in seconds that httpx will wait for a response from the resource requested.**
    

### **3.2 Backend Variables**

The variables used in the backend are:

1.  **app\_debug**: If the app is in debug mode. Debug mode allows printing of message, properties at generation time, detailed error messages, status information as well as setting the secure flag of the secure tokens.
    
2.  **jwt\_secret:** The password or secret used to sign the data in the JWT token that the backend generates. It does have a field validator that does not allow launch of the app without one and throws a warning if the length of the secret is not greater or equal than 32 characters.
    
3.  **jwt\_access\_token\_expiration\_minutes:** The time it takes for the JWT Access token to expire
    
4.  **jwt\_refresh\_token\_expiration\_minutes:** The time it takes for the JWT Refresh token
    
5.  **db\_user**: The username of the backend user that has only the CRUD permissions in the dataase
    
6.  **db\_password**: The secure password that the database user needs to login to Postgre
    
7.  **db\_host:** The host address of the system that is running the PostgreSQL database
    
8.  **db\_port**: The port that the database is listening to
    
9.  **db\_name**: The name of the database that the user has access to.