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
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character`
--

LOCK TABLES `character` WRITE;
/*!40000 ALTER TABLE `character` DISABLE KEYS */;
INSERT INTO `character` VALUES (18,'Ais Wallenstein',0),(19,'Amid Teasanara',0),(20,'Amid Teasanare',0),(21,'Anakitty Autumn',0),(22,'Anya Fromel',0),(23,'Artemis',0),(24,'Asfi Al Andromeda',0),(25,'Bell Cranel',0),(26,'Bete Loga',0),(27,'Chloe Lolo',0),(28,'Eren Yaeger',0),(29,'Fels',0),(30,'Filvis Challia',0),(31,'Finn Deimne',0),(32,'Gareth Landrock ',0),(33,'Hermes&Hermes',0),(34,'Hitachi Chigusa',0),(35,'Kashima Ouka',0),(36,'Kino&Hermes',0),(37,'Kino',0),(38,'Kurumi Tokisaki',0),(39,'Lefiya Virdis',0),(40,'Lefiya Viridis',0),(41,'Levi',0),(42,'Liliruca Arde',0),(43,'Line Arshe',0),(44,'Lunor Faust',0),(45,'Mikasa Ackermann',0),(46,'Mord Latro',0),(47,'Naza Ersuisu',0),(48,'Origami Tobiichi',0),(49,'Ottarl',0),(50,'Photo&Sou',0),(51,'Raul Nord',0),(52,'Riveria Ljos Alf',0),(53,'Ryu Lion',0),(54,'Ryu Lion (OG)',0),(55,'Shakti Varma',0),(56,'Shizu&Riku',0),(57,'Tiona Hiryute',0),(58,'Tione Hiryute',0),(59,'Touka Yatogami',0),(60,'Tsubaki Collbrande',0),(61,'Welf Crozzo',0),(62,'Yamato Mikoto',0),(63,'Name',0);
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

-- Dump completed on 2020-02-05 23:45:32
