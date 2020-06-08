-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: us-cdbr-iron-east-04.cleardb.net    Database: heroku_0fe8a18d3b21642
-- ------------------------------------------------------
-- Server version	5.5.56-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dispatch`
--

DROP TABLE IF EXISTS `dispatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatch` (
  `dispatchid` int(11) NOT NULL AUTO_INCREMENT,
  `typename` varchar(200) NOT NULL,
  `stage` varchar(200) DEFAULT NULL,
  `name` varchar(200) NOT NULL,
  `char1id` varchar(200) NOT NULL,
  `char2id` varchar(200) NOT NULL,
  `char3id` varchar(200) NOT NULL,
  `char4id` varchar(200) NOT NULL,
  PRIMARY KEY (`dispatchid`)
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispatch`
--

LOCK TABLES `dispatch` WRITE;
/*!40000 ALTER TABLE `dispatch` DISABLE KEYS */;
INSERT INTO `dispatch` VALUES (73,'R_1 ','(1/7)','Collect Information','Anya','Mama Mia','Syr','Lunor'),(74,'R_1 ','(2/7)','Interfere','Bete','Bell','Chloe','Ryu'),(75,'R_1 ','(3/7)','Trailing a Man','Asfi','Chloe','Chigusa','Mikoto'),(76,'R_1 ','(4/7)','Base Investigation','Naza','Amid','Miach','Dian'),(77,'R_1 ','(5/7)','Partying Undercover','Loki','Demeter','Hermes','Dionysis'),(78,'R_1 ','(6/7)','Unmasked','Tione','Tiona','Filvis','Bete'),(79,'R_1 ','(7/7)','Operation Desctruction','Aiz','Finn','Shakti','Ottarl'),(80,'R_2 ','(1/4)','Sword Princess\'s Test','Bell','Finn','Mikoto','Takemikazuchi'),(81,'R_2 ','(2/4)','Blacksmith\'s Backup','Amid','Misha','Loki','Eina'),(82,'R_2 ','(3/4)','Find Quality Materials','Finn','Riveria','Gareth','Shakti'),(83,'R_2 ','(4/4)','Sword to Keep Fighting','Aiz','Tsubaki','Hephaistios','Goibniu'),(84,'R_3 ','(1/4)','Mad Wolf\'s Test','Bell','Aiz','Ryu','Tiona'),(85,'R_3 ','(2/4)','Seeking Hard Ore','Raul','Lili','Lefiya','Chigusa'),(86,'R_3 ','(3/4)','Special Magic Ore','Riveria','Lefiya','Filvis','Ryu'),(87,'R_3 ','(4/4)','A Starving Wolf','Bete','Aiz','Chloe','Ryu'),(88,'R_4 ','(1/4)','Thousand Elf\'s Request','Bell','Gareth','Ouka','Mord'),(89,'R_4 ','(2/4)','Materials for a Wand','Lili','Tiona','Amid','Anakitty'),(90,'R_4 ','(3/4)','To the Sacred Forest','Ryu','Asfi','Filvis','Chloe'),(91,'R_4 ','(4/4)','I Want to Catch Up','Tiona','Aiz','Riveria','Lefiya'),(92,'R_5 ','(1/4)','Helping a Supporter','Raul','Lili','Chigusa','Lefiya'),(93,'R_5 ','(2/4)','Shopping War','Chigusa','Mama Mia','Demeter','Syr'),(94,'R_5 ','(3/4)','Seoro Exploration','Mord','Mikoto','Ouka','Naza'),(95,'R_5 ','(4/4)','Find Rare Materials','Bell','Asfi','Ryu','Chloe'),(96,'R_6 ','(1/4)','Masked Adventurer','Bell','Mikoto','Asfi','Mord'),(97,'R_6 ','(2/4)','Poetic Justice','Mikoto','Shakti','Asfi','Bete'),(98,'R_6 ','(3/4)','Attack Middle Floors','Chloe','Lunor','Anya','Mama Mia'),(99,'R_6 ','(4/4)','The Holy Tree','Riveria','Eina','Filvis','Lefiya'),(100,'R_7 ','(1/4)','Cat\'s Spear','Ryu','Asfi','Lefiya','Raul'),(101,'R_7 ','(2/4)','Let\'s go to Melen!','Tione','Tiona','Mikoto','Chloe'),(102,'R_7 ','(3/4)','Search for Gold Mine','Bell','Syr','Hephaistios','Goibniu'),(103,'R_7 ','(4/4)','Lost Cat\'s Rampage','Finn','Anya','Shakti','Ouka'),(104,'R_8 ','(1/4)','Overworking Blacksmith','Ottar','Tione','Tiona','Ouka'),(105,'R_8 ','(2/4)','Loki\'s Impossible Wish','Ais','Finn','Riveria','Bete'),(106,'R_8 ','(3/4)','Craft! Grand Axe!','Welf','Hephaistios','Tsubaki','Goibniu'),(107,'R_8 ','(4/4)','Prepare for Expedition','Lili','Lefiya','Chigusa','Raul'),(108,'CP_1',NULL,'Sneaking Mission, Meow','Welf','Mikoto','Tione','Chigusa'),(109,'CP_2',NULL,'How Do I Teach?','Riveria','Filvis','Shakti','Takemikazuchi'),(110,'CP_3',NULL,'Carrier Wanted','Raul','Lili','AnaKitty','Fels'),(111,'CP_4',NULL,'A Demon Arrives','Shakti','Finn','Tsubaki','Ottarl'),(112,'CP_5',NULL,'Expose Casino\'s Crime!','Bell','Ryu','Syr','Mord'),(113,'CP_6',NULL,'A gift to Freya','Ottarl','Mama Mia','Hermes','Anya'),(114,'CP_7',NULL,'Combat Training','Tiona','Bete','Lunor','Takemikazuchi'),(115,'CP_8',NULL,'Mysterious Conditions?','Ais','Asfi','Chloe','Amid'),(116,'E_1',NULL,'Anonymous Millionaire','Riveria','Dionysis','Raul','Amid'),(117,'E_2',NULL,'Anonymous Millionaire','Mord','Tsubaki','Ottarl','Raul'),(118,'E_3',NULL,'Anonymous Millionaire','Hestia','Gareth','Syr','Ryu'),(119,'E_4',NULL,'Anonymous Millionaire','Mikoto','Tione','Anya','Mama Mia');
/*!40000 ALTER TABLE `dispatch` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-08 15:40:11
