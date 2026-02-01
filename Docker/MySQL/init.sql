DROP DATABASE IF EXISTS snsapp_f_team;

DROP USER IF EXISTS 'testuser'@'%';


CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';

CREATE DATABASE IF NOT EXISTS snsapp_f_team
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;


GRANT ALL PRIVILEGES ON snsapp_f_team.* TO 'testuser'@'%';

FLUSH PRIVILEGES;

USE snsapp_f_team;

CREATE TABLE
    users (
        user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        profile TEXT DEFAULT NULL,
        learning TEXT DEFAULT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (user_id),
        UNIQUE KEY uq_users_email (email)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    follow (
        user_id BIGINT UNSIGNED NOT NULL,
        followed_user_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (user_id, followed_user_id),
        KEY idx_follow_user_id (user_id),
        KEY idx_follow_followed_user_id (followed_user_id),
        CONSTRAINT fk_follow_user FOREIGN KEY (user_id) REFERENCES users (user_id),
        CONSTRAINT fk_followed_user FOREIGN KEY (followed_user_id) REFERENCES users (user_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    posts (
        post_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        deleted_at DATETIME (6) DEFAULT NULL,
        PRIMARY KEY (post_id),
        KEY idx_posts_user_id (user_id),
        CONSTRAINT fk_posts_user FOREIGN KEY (user_id) REFERENCES users (user_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    comments (
        comment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        deleted_at DATETIME (6) DEFAULT NULL,
        PRIMARY KEY (comment_id),
        KEY idx_comments_user_id (user_id),
        KEY idx_comments_post_id (post_id),
        CONSTRAINT fk_comments_user FOREIGN KEY (user_id) REFERENCES users (user_id),
        CONSTRAINT fk_comments_post FOREIGN KEY (post_id) REFERENCES posts (post_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    bookmark (
        bookmark_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED DEFAULT NULL,
        comment_id BIGINT UNSIGNED DEFAULT NULL,
        PRIMARY KEY (bookmark_id),
        KEY idx_bookmark_user_id (user_id),
        KEY idx_bookmark_post_id (post_id),
        KEY idx_bookmark_comment_id (comment_id),
        CONSTRAINT fk_bookmark_user FOREIGN KEY (user_id) REFERENCES users (user_id),
        CONSTRAINT fk_bookmark_post FOREIGN KEY (post_id) REFERENCES posts (post_id),
        CONSTRAINT fk_bookmark_comment FOREIGN KEY (comment_id) REFERENCES comments (comment_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;



CREATE TABLE
    good_actions (
        good_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED DEFAULT NULL,
        comment_id BIGINT UNSIGNED DEFAULT NULL,
        PRIMARY KEY (good_id),
        KEY idx_good_user_id (user_id),
        KEY idx_good_post_id (post_id),
        KEY idx_good_comment_id (comment_id),
        CONSTRAINT fk_good_user FOREIGN KEY (user_id) REFERENCES users (user_id),
        CONSTRAINT fk_good_post FOREIGN KEY (post_id) REFERENCES posts (post_id),
        CONSTRAINT fk_good_comment FOREIGN KEY (comment_id) REFERENCES comments (comment_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    tags (
        tag_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        tag VARCHAR(255) NOT NULL UNIQUE,
        PRIMARY KEY (tag_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


CREATE TABLE
    post_tags (
        post_id BIGINT UNSIGNED NOT NULL,
        tag_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (post_id, tag_id),
        KEY idx_tags_post_id (post_id),
        KEY idx_tags_tag_id (tag_id),
        CONSTRAINT fk_tags_post FOREIGN KEY (post_id) REFERENCES posts (post_id),
        CONSTRAINT fk_tags_tag FOREIGN KEY (tag_id) REFERENCES tags (tag_id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;



INSERT INTO users (user_name, email, password, profile, learning)
VALUES 
  ('山田太郎', 'taro@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244','温泉行きたい。','MySQLを少々。'),
  ('鈴木二郎', 'jiro@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244','ヒートテック良き。','Pythonのさわりを。'),
  ('田中花子', 'hanako@example.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244','濡れた髪のまま眠りたい。','');

INSERT INTO posts (user_id, content)
VALUES
  (1, 'こんにちは！初めての投稿です。'),
  (1, '今日はとても良い天気ですね。'),
  (1, '今日も勉強頑張ります！');


INSERT INTO comments (user_id, post_id, content)
VALUES
    (2, 1, '応援しています！頑張ってください。'),
    (1, 1, 'おっふ、サンキューです。');

INSERT INTO tags (tag)
VALUES
    ('html'),
    ('Ruby');

INSERT INTO follow (user_id, followed_user_id)
VALUES
    (3, 1),
    (1, 2);

INSERT INTO bookmark (user_id, post_id)
VALUES
    (2, 3);

INSERT INTO bookmark (user_id, comment_id)
VALUES
    (1, 1);

INSERT INTO good_actions (user_id, post_id)
VALUES
    (3, 2);

INSERT INTO good_actions (user_id, comment_id)
VALUES
    (2, 1);

INSERT INTO post_tags (post_id, tag_id)
VALUES
    (1, 1);
