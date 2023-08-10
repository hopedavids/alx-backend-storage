-- Create the ComputeAverageWeightedScoreForUser stored procedure
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight INT;
    DECLARE avg_weighted_score FLOAT;

    SELECT SUM(score * weight), SUM(weight)
    INTO total_score, total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    IF total_weight IS NULL THEN
        SET avg_weighted_score = 0;
    ELSE
        SET avg_weighted_score = total_score / total_weight;
    END IF;

    UPDATE users
    SET average_score = avg_weighted_score
    WHERE id = user_id;

END;
//
DELIMITER ;
