-- This file creates a new table called users in any database
-- Create a user from any database
CREATE TABLE IF NOT EXISTS users(
	id INTEGER NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) UNIQUE NOT NULL,
	name VARCHAR(255),
	PRIMARY KEY(id)
);
