-- a SQL script that creates a stored procedure ComputeAverageScoreForUser 
-- That computes and store the average score for a student. Note: An average score can be a decimal

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE num_corrections INT;
    
    -- Compute total score and number of corrections for the user
    SELECT SUM(score), COUNT(*) INTO total_score, num_corrections
    FROM corrections
    WHERE user_id = user_id;
    
    -- Update average score for the user
    UPDATE users
    SET average_score = IF(num_corrections > 0, total_score / num_corrections, 0)
    WHERE id = user_id;
    
END;
//

DELIMITER ;

