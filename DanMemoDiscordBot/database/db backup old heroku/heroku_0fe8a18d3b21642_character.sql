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
-- Table structure for table `character`
--

DROP TABLE IF EXISTS `character`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `character` (
  `characterid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `iscollab` tinyint(4) NOT NULL,
  PRIMARY KEY (`characterid`)
) ENGINE=InnoDB AUTO_INCREMENT=662 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character`
--

LOCK TABLES `character` WRITE;
/*!40000 ALTER TABLE `character` DISABLE KEYS */;
INSERT INTO `character` VALUES (511,'Priestess',0),(512,'Ais Wallenstein',0),(513,'Ais (Girl)',0),(514,'Amid Teasanare',0),(515,'Anakitty Autumn',0),(516,'Anya Fromel',0),(517,'Lefiya Viridis',0),(518,'Artemis',0),(519,'Liliruca Arde',0),(520,'Asfi Al Andromeda',0),(521,'Bell Cranel',0),(522,'Bete (Boy)',0),(523,'Bete Loga',0),(524,'Kotori Itsuka',0),(525,'Aisha Belka',0),(526,'Chloe Lolo',0),(527,'Argonaut',0),(528,'Samira',0),(529,'Cassandra Ilion',0),(530,'Filvis Challia',0),(531,'Elmina',0),(532,'Kashima Ouka',0),(533,'Fina',0),(534,'Eren Jaeger',0),(535,'Fels',0),(536,'Riveria Ljos Alf',0),(537,'Finn Deimne',0),(538,'Sanjouno Haruhime',0),(539,'Hitachi Chigusa',0),(540,'Gareth Landrock ',0),(541,'Hermes&Hermes',0),(542,'Tsubaki Collbrande',0),(543,'Kino & Hermes',0),(544,'Kino',0),(545,'Yamato Mikoto',0),(546,'Kurumi Tokisaki',0),(547,'Daphne Lauros',0),(548,'Levi',0),(549,'Ryu Lion',0),(550,'Noble Fencer',0),(551,'Line Arshe',0),(552,'Bell (Boy)',0),(553,'Liliruca (Girl)',0),(554,'Lunor Faust',0),(555,'Mikasa Ackermann',0),(556,'Mord Latro',0),(557,'Naza Ersuisu',0),(558,'Origami Tobiichi',0),(559,'Ottarl',0),(560,'Photo & Sou',0),(561,'Raul Nord',0),(562,'Tione Hiryute',0),(563,'Shakti Varma',0),(564,'Shizu & Riku',0),(565,'Goblin Slayer',0),(566,'Shido Itsuka',0),(567,'High Elf Archer',0),(568,'Crozzo',0),(569,'Tiona Hiryute',0),(570,'Touka Yatogami',0),(571,'Galmus',0),(572,'Welf Crozzo',0),(573,'Welf (Boy)',0),(574,'Lena Tally',0),(575,'Yuri',0),(576,'Hestia',0),(577,'Hephaistios',0),(578,'Cow Girl',0),(579,'Hermes',0),(580,'Loki',0),(581,'Freya',0),(582,'Kaguya & Liliruca',0),(583,'Eina',0),(584,'Ariadne',0),(585,'Demeter',0),(586,'Syr',0),(587,'Dionysus',0),(588,'Eina Tulle',0),(589,'Ryu',0),(590,'Lefiya (Girl)',0),(591,'Ti',0),(592,'Ganesha',0),(593,'Apollo',0),(594,'Ouranos',0),(595,'Ares',0),(596,'Goibniu',0),(597,'Sword Maiden',0),(598,'Syr Flover',0),(599,'Orna',0),(600,'Riveria (Girl)',0),(601,'Hestia (Girl)',0),(602,'Miach',0),(603,'Mia Grand',0),(604,'Misha Flot',0),(605,'Ryulu',0),(606,'Crunchyroll-Hime',0),(607,'Soma',0),(608,'Armin Arlert',0),(609,'Takemikazuchi',0),(610,'Ishtar',0),(611,'Titan Eren',0),(612,'Dianceht',0),(613,'Amid',0),(622,'Hephaistios (Girl)',0),(632,'Anya (Girl)',0),(642,'Chloe (Girl)',0),(652,'Lunor (Girl)',0);
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

-- Dump completed on 2020-04-24 13:01:44
