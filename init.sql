
DROP DATABASE cookchat;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE cookchat;
USE cookchat
GRANT ALL PRIVILEGES ON cookchat.* TO 'testuser';

CREATE TABLE users (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(64) NOT NULL
);

CREATE TABLE `groups` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    created_by VARCHAR(255),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE user_groups (
    PRIMARY KEY(uid, gid),
    uid VARCHAR(255) NOT NULL,
    gid INT NOT NULL,
    FOREIGN KEY (uid) REFERENCES users(id),
    FOREIGN KEY (gid) REFERENCES `groups`(id) ON DELETE CASCADE
);

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid VARCHAR(255) NOT NULL,
    gid INT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES users(id),
    FOREIGN KEY (gid) REFERENCES `groups`(id) ON DELETE CASCADE
);