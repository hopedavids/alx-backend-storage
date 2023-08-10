-- An SQL script that creates a table users following these requirements:
-- Make an attribute unique directly in the table schema will enforced your business rules and avoid bugs in your application

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
