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
-- Table structure for table `modifier`
--

DROP TABLE IF EXISTS `modifier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modifier` (
  `modifierid` int NOT NULL AUTO_INCREMENT,
  `value` varchar(200) NOT NULL,
  PRIMARY KEY (`modifierid`)
) ENGINE=InnoDB AUTO_INCREMENT=258 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modifier`
--

LOCK TABLES `modifier` WRITE;
/*!40000 ALTER TABLE `modifier` DISABLE KEYS */;
INSERT INTO `modifier` VALUES (177,'ultra'),(178,'+70'),(179,'+10'),(180,'high'),(181,'medium'),(182,'+5'),(183,'+1'),(184,'-40'),(185,'-25'),(186,'40'),(187,'+40'),(188,'+20'),(189,'+15'),(190,'+0'),(191,'boost'),(192,'15'),(193,'+60'),(194,'+50'),(195,'low'),(196,'+4'),(197,'+3'),(198,'+2'),(199,'Dmg+30% per target\'s M.Resist Reduction Skill'),(200,'fast'),(201,'Dmg+50% per target\'s M.Resist Reduction Skill'),(202,'+35'),(203,'-2 turns'),(204,'+25'),(205,'25'),(206,'-30'),(207,'strength'),(208,'+75'),(209,'-20'),(210,'+100'),(211,'-50'),(212,'-15'),(213,'x2'),(214,'+11'),(215,'30'),(216,''),(217,'20'),(218,'+30'),(219,'+85'),(220,'75'),(221,'-1 turn'),(222,'+7.5'),(223,'50'),(224,'slight'),(225,'+8'),(226,'-35'),(227,'-10'),(228,'x1'),(229,'10'),(230,'x1 with 35% Chance'),(231,'+6'),(232,'+1 turn'),(233,'+65'),(234,'+45'),(235,'-75'),(236,'Hi to Ally w/ least HP'),(237,'-45'),(238,'hp'),(239,'1'),(240,'35'),(241,'+7'),(242,'+9'),(243,'magic'),(244,'-7.5'),(245,'(make targets)'),(246,'5'),(247,'-5'),(248,'+5.5'),(249,'+33'),(250,'7.5'),(251,'super'),(252,'+20%'),(253,'endurance'),(254,'(put targets to)'),(255,'slow'),(256,'Dmg+50% per each [Self] Str. Buff Skill'),(257,'+4.5');
/*!40000 ALTER TABLE `modifier` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-05 23:45:31
