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
  `date` date,
  `start` time,
  'end' time,
  `title` varchar(255),
  `description` varchar(255)
);

ALTER TABLE `todos` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

INSERT into `users`(user_id, token)
VALUES (1,'test_user1'),
       (2,'test_user2'),
       (3,'test_user3')
;
