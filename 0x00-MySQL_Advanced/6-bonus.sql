-- Create a procedure to change the correction/grade of a student
-- on a particular project
DELIMITER //
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name CHAR(255), IN score INT)
BEGIN
	DECLARE proj_id INTEGER;
	SET proj_id = (SELECT id FROM projects WHERE name = project_name);
	IF proj_id IS NULL THEN
		INSERT INTO projects(name) VALUES(project_name);
		SET proj_id = LAST_INSERT_ID();
	END IF;
	INSERT INTO corrections(score, user_id, project_id) VALUES(score, user_id, proj_id);
END;//
DELIMITER ;
