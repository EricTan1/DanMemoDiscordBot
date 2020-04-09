-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: danmemo
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `character`
--

DROP TABLE IF EXISTS `character`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character` (
  `characterid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `iscollab` tinyint NOT NULL,
  PRIMARY KEY (`characterid`)
) ENGINE=InnoDB AUTO_INCREMENT=207 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character`
--

LOCK TABLES `character` WRITE;
/*!40000 ALTER TABLE `character` DISABLE KEYS */;
INSERT INTO `character` VALUES (111,'Ais Wallenstein',0),(112,'Amid Teasanara',0),(113,'Amid Teasanare',0),(114,'Anakitty Autumn',0),(115,'Anya Fromel',0),(116,'Artemis',0),(117,'Asfi Al Andromeda',0),(118,'Bell Cranel',0),(119,'Bete Loga',0),(120,'Chloe Lolo',0),(121,'Eren Yaeger',0),(122,'Fels',0),(123,'Filvis Challia',0),(124,'Finn Deimne',0),(125,'Gareth Landrock ',0),(126,'Hermes&Hermes',0),(127,'Hitachi Chigusa',0),(128,'Kashima Ouka',0),(129,'Kino&Hermes',0),(130,'Kino',0),(131,'Kurumi Tokisaki',0),(132,'Lefiya Virdis',0),(133,'Lefiya Viridis',0),(134,'Levi',0),(135,'Liliruca Arde',0),(136,'Line Arshe',0),(137,'Lunor Faust',0),(138,'Mikasa Ackermann',0),(139,'Mord Latro',0),(140,'Naza Ersuisu',0),(141,'Origami Tobiichi',0),(142,'Ottarl',0),(143,'Photo&Sou',0),(144,'Raul Nord',0),(145,'Riveria Ljos Alf',0),(146,'Ryu Lion',0),(147,'Ryu Lion (OG)',0),(148,'Shakti Varma',0),(149,'Shizu&Riku',0),(150,'Tiona Hiryute',0),(151,'Tione Hiryute',0),(152,'Touka Yatogami',0),(153,'Tsubaki Collbrande',0),(154,'Welf Crozzo',0),(155,'Yamato Mikoto',0),(156,'Name',0),(157,'Armin Arlert',0),(158,'Crunchyroll-Hime',0),(159,'Demeter',0),(160,'Dianceht',0),(161,'Dionysus',0),(162,'Eina Tulle',0),(163,'Freya',0),(164,'Ganesha',0),(165,'Goibniu',0),(166,'Hephaistios',0),(167,'Hermes',0),(168,'Hestia',0),(169,'Kaguya & Liliruca',0),(170,'Kotori Itsuka',0),(171,'Loki',0),(172,'Miach',0),(173,'Mia Grand',0),(174,'Misha Flot',0),(175,'Ouranos',0),(176,'Syr Flover',0),(177,'Syr Flover (Christmas)',0),(178,'Takemikazuchi',0),(179,'Titan Eren',0),(180,'Ti',0),(181,'Ariadne',0),(182,'Orna',0),(183,'Ryulu',0),(184,'Apollo',0),(185,'Soma',0),(186,'Ishtar',0),(187,'Ares',0),(188,'Cow Girl',0),(189,'Sanjouno Haruhime',0),(190,'Aisha Belka',0),(191,'Argonaut',0),(192,'Elmina',0),(193,'Crozzo',0),(194,'Yuri',0),(195,'Galmus',0),(196,'Fina',0),(197,'Daphne Lauros',0),(198,'Cassandra Ilion',0),(199,'Lena Tally',0),(200,'Samira',0),(201,'Shido Itsuka',0),(202,'Goblin Slayer',0),(203,'Priestess',0),(204,'High Elf Archer',0),(205,'Noble Fencer',0),(206,'Tione Hirute',0);
/*!40000 ALTER TABLE `character` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-02 17:46:51
