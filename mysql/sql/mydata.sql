CREATE TABLE IF NOT EXISTS `mydata` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `title` text COLLATE utf8mb4_unicode_ci,
    `body` text COLLATE utf8mb4_unicode_ci,
    `media` text COLLATE utf8mb4_unicode_ci,
    `url` text COLLATE utf8mb4_unicode_ci,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX(`id`),
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

LOAD DATA LOCAL INFILE '/data/mydata/mydata.tsv'
INTO TABLE mydata
FIELDS TERMINATED BY '\t'
(title, body);
