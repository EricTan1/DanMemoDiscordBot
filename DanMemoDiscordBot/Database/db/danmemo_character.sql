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
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `character`
--

LOCK TABLES `character` WRITE;
/*!40000 ALTER TABLE `character` DISABLE KEYS */;
INSERT INTO `character` VALUES (111,'Ais Wallenstein',0),(112,'Amid Teasanara',0),(113,'Amid Teasanare',0),(114,'Anakitty Autumn',0),(115,'Anya Fromel',0),(116,'Artemis',0),(117,'Asfi Al Andromeda',0),(118,'Bell Cranel',0),(119,'Bete Loga',0),(120,'Chloe Lolo',0),(121,'Eren Yaeger',0),(122,'Fels',0),(123,'Filvis Challia',0),(124,'Finn Deimne',0),(125,'Gareth Landrock ',0),(126,'Hermes&Hermes',0),(127,'Hitachi Chigusa',0),(128,'Kashima Ouka',0),(129,'Kino&Hermes',0),(130,'Kino',0),(131,'Kurumi Tokisaki',0),(132,'Lefiya Virdis',0),(133,'Lefiya Viridis',0),(134,'Levi',0),(135,'Liliruca Arde',0),(136,'Line Arshe',0),(137,'Lunor Faust',0),(138,'Mikasa Ackermann',0),(139,'Mord Latro',0),(140,'Naza Ersuisu',0),(141,'Origami Tobiichi',0),(142,'Ottarl',0),(143,'Photo&Sou',0),(144,'Raul Nord',0),(145,'Riveria Ljos Alf',0),(146,'Ryu Lion',0),(147,'Ryu Lion (OG)',0),(148,'Shakti Varma',0),(149,'Shizu&Riku',0),(150,'Tiona Hiryute',0),(151,'Tione Hiryute',0),(152,'Touka Yatogami',0),(153,'Tsubaki Collbrande',0),(154,'Welf Crozzo',0),(155,'Yamato Mikoto',0),(156,'Name',0);
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

-- Dump completed on 2020-02-23 18:45:15
