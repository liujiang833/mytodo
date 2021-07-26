DROP DATABASE IF EXISTS mytodo;
CREATE DATABASE mytodo;
use mytodo;
CREATE TABLE `users` (
  `user_id` int PRIMARY KEY AUTO_INCREMENT,
  `token` varchar(32)
);

CREATE TABLE `todos` (
  `todo_number` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `time` datetime,
  `title` varchar(255),
  `description` varchar(255)
);

ALTER TABLE `todos` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);