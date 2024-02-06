CREATE TABLE IF NOT EXISTS `news` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `media` text COLLATE utf8mb4_unicode_ci,
    `url` text COLLATE utf8mb4_unicode_ci,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `title` text COLLATE utf8mb4_unicode_ci,
    `body` text COLLATE utf8mb4_unicode_ci,
    `vector` VARCHAR(16000),
    INDEX(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `news` (media, url, created_at, title, body)
SELECT
    media
    , url
    , created_at
    , title
    , body
FROM mydata
UNION ALL
SELECT
    media
    , url
    , created_at
    , emotion as title
    , doc as body
FROM knbc
UNION ALL
SELECT
    media
    , url
    , created_at
    , title
    , body
FROM kwdlc
UNION ALL
SELECT
    media
    , url
    , created_at
    , title
    , body
FROM lcc
;
