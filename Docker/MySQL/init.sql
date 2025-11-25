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


-- デモ用users
-- パスワード: hoge
INSERT INTO users(id, name, email, password) VALUES('6d05f6e4-2f33-49ca-9962-b65908ee319a', 'かおり', 'kaori@example.com', 'ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');
INSERT INTO users(id, name, email, password) VALUES('995f03c4-a2b3-4b77-b2ca-5dd1dd567924', 'パパ', 'takuya@example.com', 'ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');
INSERT INTO users(id, name, email, password) VALUES('587ed39a-d692-45db-b8c5-df50db94c082', '美咲', 'misaki@example.com', 'ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');
INSERT INTO users(id, name, email, password) VALUES('52d479fd-7e53-4aac-9e5f-a0069c5c8cfb', '翔太', 'shota@example.com', 'ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');
INSERT INTO users(id, name, email, password) VALUES('283524a9-2c86-4ef4-be19-f4ffd83312d6', '桜井恵子', 'keiko@example.com', 'ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');
INSERT INTO users(id, name, email, password) VALUES('4b965fa4-b482-43ef-b00e-b838d503826a', 'じいじ', 'kenichi@example.com', 'ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');
INSERT INTO users(id, name, email, password) VALUES('0bb6c997-0555-49a2-acd1-f24d5c617d0c', 'トシオ', 'toshio@example.com', 'ecb666d778725ec97307044d642bf4d160aabb76f56c0069c71ea25b1e926825');

-- デモ用groups
INSERT INTO `groups` (id, name, created_by) VALUES(1, '桜井家', '6d05f6e4-2f33-49ca-9962-b65908ee319a');
INSERT INTO `groups` (id, name, created_by) VALUES(2, '桜井家+じいじ＆ばあば', '6d05f6e4-2f33-49ca-9962-b65908ee319a');

-- デモ用user_groups
-- "桜井家"
INSERT INTO user_groups(uid, gid) VALUES('6d05f6e4-2f33-49ca-9962-b65908ee319a', 1);
INSERT INTO user_groups(uid, gid) VALUES('995f03c4-a2b3-4b77-b2ca-5dd1dd567924', 1);
INSERT INTO user_groups(uid, gid) VALUES('587ed39a-d692-45db-b8c5-df50db94c082', 1);
INSERT INTO user_groups(uid, gid) VALUES('52d479fd-7e53-4aac-9e5f-a0069c5c8cfb', 1);

-- "桜井家+じいじ＆ばあば"
INSERT INTO user_groups(uid, gid) VALUES('6d05f6e4-2f33-49ca-9962-b65908ee319a', 2);
INSERT INTO user_groups(uid, gid) VALUES('995f03c4-a2b3-4b77-b2ca-5dd1dd567924', 2);
INSERT INTO user_groups(uid, gid) VALUES('587ed39a-d692-45db-b8c5-df50db94c082', 2);
INSERT INTO user_groups(uid, gid) VALUES('52d479fd-7e53-4aac-9e5f-a0069c5c8cfb', 2);
INSERT INTO user_groups(uid, gid) VALUES('283524a9-2c86-4ef4-be19-f4ffd83312d6', 2);
INSERT INTO user_groups(uid, gid) VALUES('4b965fa4-b482-43ef-b00e-b838d503826a', 2);

-- デモ用messagesとeat_reactions
-- "桜井家"
INSERT INTO messages (id, uid, gid, message, created_at) VALUES(1, '6d05f6e4-2f33-49ca-9962-b65908ee319a', 1, 'みんな、今日の夕飯なんだけど、何か食べたいものある？', '2025-11-23 18:00:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(1, 0);

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(2, '587ed39a-d692-45db-b8c5-df50db94c082', 1, 'ハンバーグがいい！', '2025-11-23 18:01:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(2, 0);

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(3, '52d479fd-7e53-4aac-9e5f-a0069c5c8cfb', 1, 'えー、昨日も肉じゃん。中華がいいなー', '2025-11-23 18:02:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(3, 0);

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(4, '995f03c4-a2b3-4b77-b2ca-5dd1dd567924', 1, '俺はなんでもいいよ。でも、美咲の言う通り、ハンバーグもいいな。', '2025-11-23 18:03:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(4, 0);

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(5, '6d05f6e4-2f33-49ca-9962-b65908ee319a', 1, 'うーん、意見が割れちゃったな…。挽肉と豆腐はあるから…。よし、AIに相談してみよう！', '2025-11-23 18:04:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(5, 0);

-- "桜井家+じいじ＆ばあば"

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(6, '283524a9-2c86-4ef4-be19-f4ffd83312d6', 2, '香織さんへ　週末は魚が食べたいわ。あ、焼き魚がいいかしら。　恵子より', '2025-11-23 19:00:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(6, 0);

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(7, '6d05f6e4-2f33-49ca-9962-b65908ee319a', 2, 'お義母さん、ごめんなさい、魚焼きグリルが故障しちゃったみたいなの。', '2025-11-23 19:01:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(7, 0);

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(8, '4b965fa4-b482-43ef-b00e-b838d503826a', 2, 'わしはさっぱりしたものがいいな。鍋とか。', '2025-11-23 19:02:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(8, 0);

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(9, '995f03c4-a2b3-4b77-b2ca-5dd1dd567924', 2, '父さん、鍋は今日暑くない？', '2025-11-23 19:03:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(9, 0);

INSERT INTO messages (id, uid, gid, message, created_at) VALUES(10, '6d05f6e4-2f33-49ca-9962-b65908ee319a', 2, 'サッパリしてるけど、暑くるしくない魚料理がいいのかな。今日、ちょうどスーパーへ行くから、AIに相談してみよう！', '2025-11-23 19:04:00');
INSERT INTO eat_reactions (message_id, counts) VALUES(10, 0);