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
-- Table structure for table `assist`
--

DROP TABLE IF EXISTS `assist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assist` (
  `assistid` int NOT NULL AUTO_INCREMENT,
  `characterid` int NOT NULL,
  `splashuri` varchar(2048) DEFAULT NULL,
  `iconuri` varchar(2048) DEFAULT NULL,
  `limited` tinyint NOT NULL,
  `stars` int NOT NULL,
  `title` varchar(200) NOT NULL,
  PRIMARY KEY (`assistid`),
  KEY `charid_idx` (`characterid`),
  CONSTRAINT `characterid4` FOREIGN KEY (`characterid`) REFERENCES `character` (`characterid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=412 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assist`
--

LOCK TABLES `assist` WRITE;
/*!40000 ALTER TABLE `assist` DISABLE KEYS */;
INSERT INTO `assist` VALUES (258,113,'None','None',0,3,'Modern Medicine'),(259,113,'None','None',0,4,'White Healer'),(260,115,'None','None',0,2,'Cat-Ears'),(261,115,'None','None',0,4,'Clumsy Detective'),(262,115,'None','None',0,3,'Lighthearted'),(263,157,'None','None',1,4,'Sharp Thinker'),(264,116,'None','None',0,4,'Innocent Goddess'),(265,116,'None','None',0,4,'Sleeping Innocence'),(266,118,'None','None',1,4,'Living Dead Child'),(267,120,'None','None',0,2,'Sinister Cat'),(268,120,'None','None',0,4,'The Sly Cat'),(269,158,'None','None',1,4,'Princess'),(270,159,'None','None',0,4,'Golden Wheat'),(271,159,'None','None',0,2,'Harvest Goddess'),(272,159,'None','None',0,3,'Mother Seedling'),(273,160,'None','None',0,3,'Vigorous Medi-God'),(274,161,'None','None',0,3,'Classy God'),(275,161,'None','None',0,4,'God of Wine'),(276,161,'None','None',0,3,'Tipsy Gaze'),(277,162,'None','None',0,3,'Advisor'),(278,162,'None','None',0,4,'Brains and Beauty'),(279,162,'None','None',0,4,'Elf\'s Gift'),(280,162,'None','None',0,3,'Guild Inspector'),(281,162,'None','None',1,4,'Handmade Elf'),(282,162,'None','None',1,4,'Holy Choir'),(283,162,'None','None',1,4,'Midsummer Maiden'),(284,162,'None','None',0,4,'Minstrel Elf'),(285,162,'None','None',0,2,'Receptionist'),(286,162,'None','None',0,3,'Scholar'),(287,162,'None','None',0,4,'Valorous Elf'),(288,163,'None','None',0,4,'Banquet Queen'),(289,163,'None','None',0,4,'Beautiful Admirer'),(290,163,'None','None',0,3,'Devious Emotion'),(291,163,'None','None',1,4,'Elegant Queen'),(292,163,'None','None',0,2,'Intrigued Goddess'),(293,163,'None','None',0,3,'Prowling for Lust'),(294,163,'None','None',0,4,'Queen of Beauty'),(295,163,'None','None',0,4,'Utmost Beauty'),(296,164,'None','None',0,2,'God of the Masses'),(297,164,'None','None',0,4,'Maharaja Elephant'),(298,164,'None','None',0,3,'Masked God'),(299,164,'None','None',0,3,'Mighty Elephant'),(300,165,'None','None',0,2,'Elder Smith'),(301,165,'None','None',0,3,'Godly Swordsmith'),(302,166,'None','None',0,4,'Artless'),(303,166,'None','None',0,4,'Black Rose'),(304,166,'None','None',0,3,'Burning Forge'),(305,166,'None','None',0,3,'Legendary Artisan'),(306,166,'None','None',0,2,'The One-Eyed'),(307,166,'None','None',1,4,'Young Blacksmith'),(308,167,'None','None',0,4,'Banquet Attire'),(309,167,'None','None',0,3,'Fearless Smile'),(310,167,'None','None',0,2,'God of Traveler'),(311,168,'None','None',0,4,'All Abroad'),(312,168,'None','None',1,4,'Beloved Goddess'),(313,168,'None','None',0,4,'Bunny Goddess'),(314,168,'None','None',0,4,'Ceremonial Flame'),(315,168,'None','None',1,4,'Chief Goddess'),(316,168,'None','None',0,1,'Childish Goddess'),(317,168,'None','None',1,3,'Cunning Goddess'),(318,168,'None','None',1,4,'Day For Exploring'),(319,168,'None','None',1,4,'Director Goddess'),(320,168,'None','None',1,4,'Dreaming Goddess'),(321,168,'None','None',1,4,'Filmic Goddess'),(322,168,'None','None',0,4,'Glitter Goddess'),(323,168,'None','None',0,3,'Goddess\' Devotion'),(324,168,'None','None',0,2,'Goddess of Hearth'),(325,168,'None','None',0,3,'Goddess of Purity'),(326,168,'None','None',1,4,'Jingle Bell'),(327,168,'None','None',1,4,'Kunoichi Goddess'),(328,168,'None','None',1,4,'Little Goddess'),(329,168,'None','None',0,3,'Lovebird'),(330,168,'None','None',0,4,'Moonlight Reunion'),(331,168,'None','None',1,4,'Mummy Goddess'),(332,168,'None','None',0,4,'Pajama Goddess'),(333,168,'None','None',0,4,'Paradise Mood'),(334,168,'None','None',0,4,'Part-time Goddess'),(335,168,'None','None',1,4,'Reindeer Goddess'),(336,168,'None','None',0,4,'Sacred Fire'),(337,168,'None','None',1,4,'Seaside Goddess'),(338,168,'None','None',1,4,'Summer Goddess'),(339,168,'None','None',1,4,'Truly Sweet'),(340,168,'None','None',0,4,'Wedding Wish'),(341,169,'None','None',1,4,'Berserk'),(342,170,'None','None',1,4,'Efreet'),(343,133,'None','None',1,4,'Elven Childhood'),(344,171,'None','None',0,4,'Banquet Dress'),(345,171,'None','None',0,3,'Cheers!'),(346,171,'None','None',0,2,'Crafty Goddess'),(347,171,'None','None',0,4,'Oni Demon'),(348,171,'None','None',0,3,'Red Quipster'),(349,171,'None','None',0,3,'Trickster'),(350,171,'None','None',0,4,'Trickster\'s Truth'),(351,171,'None','None',1,4,'Whoever'),(352,137,'None','None',0,2,'Fertility Helper'),(353,137,'None','None',0,3,'Prideful Waitress'),(354,172,'None','None',0,3,'God Neighbor'),(355,172,'None','None',0,3,'God of Medicine'),(356,172,'None','None',0,2,'Pharmicist'),(357,173,'None','None',0,2,'Fertilty\'s Mom'),(358,173,'None','None',0,3,'Overwhelm'),(359,174,'None','None',0,2,'Guild Worker'),(360,174,'None','None',1,4,'Summer Break'),(361,174,'None','None',0,3,'Workplace Gossip'),(362,140,'None','None',0,3,'Silver Pharmacist'),(363,175,'None','None',0,4,'God of Origins'),(364,145,'None','None',1,4,'Dark Divine'),(365,145,'None','None',1,4,'Little Dame'),(366,146,'None','None',0,3,'Elven Employee'),(367,176,'None','None',0,3,'A Loving Lunch'),(368,176,'None','None',0,3,'Brightened Pub'),(369,176,'None','None',1,4,'Candy Shop'),(370,176,'None','None',0,4,'Countess'),(371,176,'None','None',0,2,'Fertility Staff'),(372,176,'None','None',1,4,'Holiday Spirit'),(373,176,'None','None',0,4,'Pure-White Dress'),(374,176,'None','None',0,4,'Pure Bride'),(375,177,'None','None',1,4,'Pure White'),(376,176,'None','None',1,4,'Summer Mischief'),(377,176,'None','None',1,4,'Tricky Angel'),(378,178,'None','None',0,2,'Battle God'),(379,178,'None','None',0,3,'War Incarnation'),(380,179,'None','None',1,4,'Uncontrollable'),(381,180,'None','None',1,4,'Explosive Girl'),(382,153,'None','None',0,4,'Camellia Kimono'),(383,154,'None','None',0,4,'Festive Blade'),(384,155,'None','None',0,4,'Onsen Samurai'),(385,181,'None','None',1,4,'Chained Reign'),(386,181,'None','None',1,4,'Final Reminiscence'),(387,182,'None','None',0,4,'In The End'),(388,183,'None','None',1,4,'Nomadic Bard'),(389,184,'None','None',0,4,'God of Light'),(390,185,'None','None',0,4,'Sacred Cup'),(391,186,'None','None',0,4,'The Night Queen'),(392,187,'None','None',0,4,'God of War'),(393,188,'None','None',1,4,'At Home'),(394,111,'None','None',0,4,'Outside Orario'),(395,111,'None','None',0,4,'Backstage Princess'),(396,117,'None','None',0,4,'Lawful Judge'),(397,127,'None','None',1,4,'Cowgirl Dress'),(398,146,'None','None',1,4,'Elegant Vanguard'),(399,140,'None','None',0,4,'Cyan'),(400,122,'None','None',1,4,'Ghost'),(401,168,'None','None',0,4,'Azure Goddess'),(402,168,'None','None',1,4,'Gift Goddess'),(403,168,'None','None',0,4,'Yellow Bird'),(404,168,'None','None',0,4,'Swimsuit Contest'),(405,176,'None','None',0,4,'New Year Kimono'),(406,162,'None','None',1,4,'Wannabe Nerd'),(407,163,'None','None',1,4,'Dreamy Swimmer'),(408,159,'None','None',0,4,'Colonel'),(409,172,'None','None',0,4,'New Year Medic'),(410,178,'None','None',1,4,'Winter War God'),(411,137,'None','None',0,4,'Dungeon Waitress');
/*!40000 ALTER TABLE `assist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-02 17:46:50
