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
) ENGINE=InnoDB AUTO_INCREMENT=439 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modifier`
--

LOCK TABLES `modifier` WRITE;
/*!40000 ALTER TABLE `modifier` DISABLE KEYS */;
INSERT INTO `modifier` VALUES (339,'ultra'),(340,'+70'),(341,'+10'),(342,'high'),(343,'medium'),(344,'+5'),(345,'+1'),(346,'-40'),(347,'-25'),(348,'40'),(349,'+40'),(350,'+20'),(351,'+15'),(352,'+0'),(353,'boost'),(354,'15'),(355,'+60'),(356,'+50'),(357,'low'),(358,'+4'),(359,'+3'),(360,'+2'),(361,'Dmg+30% per target\'s M.Resist Reduction Skill'),(362,'fast'),(363,'Dmg+50% per target\'s M.Resist Reduction Skill'),(364,'+35'),(365,'-2 turns'),(366,'+25'),(367,'25'),(368,'-30'),(369,'strength'),(370,'+75'),(371,'-20'),(372,'+100'),(373,'-50'),(374,'-15'),(375,'x2'),(376,'+11'),(377,'30'),(378,''),(379,'20'),(380,'+30'),(381,'+85'),(382,'75'),(383,'-1 turn'),(384,'+7.5'),(385,'50'),(386,'slight'),(387,'+8'),(388,'-35'),(389,'-10'),(390,'x1'),(391,'10'),(392,'x1 with 35% Chance'),(393,'+6'),(394,'+1 turn'),(395,'+65'),(396,'+45'),(397,'-75'),(398,'Hi to Ally w/ least HP'),(399,'-45'),(400,'hp'),(401,'1'),(402,'35'),(403,'+7'),(404,'+9'),(405,'magic'),(406,'-7.5'),(407,'(make targets)'),(408,'5'),(409,'-5'),(410,'+5.5'),(411,'+33'),(412,'7.5'),(413,'super'),(414,'+20%'),(415,'endurance'),(416,'(put targets to)'),(417,'slow'),(418,'Dmg+50% per each [Self] Str. Buff Skill'),(419,'+4.5'),(420,'+80'),(421,'+10% (effect does not apply to [Self])'),(422,'+15% (effect does not apply to [Self])'),(423,'-8'),(424,'45'),(425,'8'),(426,'-7'),(427,'-6'),(428,'-4'),(429,'100'),(430,'+12'),(431,'-12'),(432,'+14'),(433,'+18'),(434,'+90'),(435,'7'),(436,'4'),(437,'6'),(438,'+66');
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

-- Dump completed on 2020-03-22  1:25:31