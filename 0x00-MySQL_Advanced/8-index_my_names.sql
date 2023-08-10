--  An SQL script that creates an index idx_name_first on the table names 
-- And the first letter of name.

-- Create index on the first letter of the name column
CREATE INDEX idx_name_first ON names (LEFT(name, 1));
