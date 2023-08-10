-- SQL script that creates an index idx_name_first_score on the table names 
-- And the first letter of name and the score

-- Create index on the first letter of name and score columns
USE holberton;

CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);
