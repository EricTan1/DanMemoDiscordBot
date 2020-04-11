DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `discordid` varchar(255) NOT NULL,
  `data` text NOT NULL,
  PRIMARY KEY (`userid`)
);