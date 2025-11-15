DROP DATABASE cookchat;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE cookchat;
USE cookchat
GRANT ALL PRIVILEGES ON cookchat.* TO 'testuser';

SET time_zone = '+09:00';
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
    creation_type VARCHAR(20) NOT NULL DEFAULT 'user',
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES users(id),
    FOREIGN KEY (gid) REFERENCES `groups`(id) ON DELETE CASCADE
);

CREATE TABLE eat_reactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message_id INT NOT NULL,
    counts INT NOT NULL,
    FOREIGN KEY(message_id) REFERENCES messages(id) ON DELETE CASCADE
);

CREATE TABLE ai_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gid INT NOT NULL,
    creation_type VARCHAR(20) NOT NULL DEFAULT 'ai',
    message TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gid) REFERENCES `groups`(id) ON DELETE CASCADE
);

CREATE TABLE ai_eat_reactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message_id INT NOT NULL,
    counts INT NOT NULL,
    FOREIGN KEY(message_id) REFERENCES ai_messages(id) ON DELETE CASCADE
);


INSERT INTO users(id, name, email, password) VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テストユーザー1','test@gmail.com','ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');
INSERT INTO users(id, name, email, password) VALUES('1b4d724d-46c5-4ee9-8dfb-5afec5166c6f','テストユーザー2','test2@gmail.com','ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');

INSERT INTO `groups` (id, name, created_by) VALUES(1, 'テストグループ','970af84c-dd40-47ff-af23-282b72b7cca8');

INSERT INTO user_groups(uid,gid) VALUES('970af84c-dd40-47ff-af23-282b72b7cca8',1);
INSERT INTO user_groups(uid,gid) VALUES('1b4d724d-46c5-4ee9-8dfb-5afec5166c6f',1);