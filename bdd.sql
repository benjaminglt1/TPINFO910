
CREATE DATABASE flask;
USE flask;
CREATE TABLE `users` (`id` bigint(20) NOT NULL AUTO_INCREMENT,`login` varchar(50) DEFAULT NULL,`password` varchar(50) DEFAULT NULL,PRIMARY KEY (`id`));
INSERT INTO users (id,login,password) VALUES (NULL,"Ben","BenPass");
INSERT INTO users (id,login,password) VALUES (NULL,"Test","TestPass");

/*SELECT * FROM users;*/
