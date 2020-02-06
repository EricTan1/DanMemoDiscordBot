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
-- Table structure for table `adventurer`
--

DROP TABLE IF EXISTS `adventurer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adventurer` (
  `adventurerid` int NOT NULL AUTO_INCREMENT,
  `characterid` int NOT NULL,
  `typeid` int NOT NULL,
  `limited` tinyint NOT NULL,
  `ascended` tinyint NOT NULL,
  `stars` int NOT NULL,
  `splashuri` varchar(2048) DEFAULT NULL,
  `iconuri` varchar(2048) DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  PRIMARY KEY (`adventurerid`),
  KEY `characterid_idx` (`characterid`),
  KEY `typeid_idx` (`typeid`),
  CONSTRAINT `characterid` FOREIGN KEY (`characterid`) REFERENCES `character` (`characterid`) ON DELETE CASCADE,
  CONSTRAINT `typeid` FOREIGN KEY (`typeid`) REFERENCES `type` (`typeid`)
) ENGINE=InnoDB AUTO_INCREMENT=261 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adventurer`
--

LOCK TABLES `adventurer` WRITE;
/*!40000 ALTER TABLE `adventurer` DISABLE KEYS */;
INSERT INTO `adventurer` VALUES (83,18,37,1,0,4,NULL,NULL,'Angelic Leader'),(84,18,40,0,0,4,NULL,NULL,'Bathroom Princess'),(85,18,37,0,0,2,NULL,NULL,'Battle Princess'),(86,18,37,0,0,4,NULL,NULL,'Bunny Princess'),(87,18,37,1,0,3,NULL,NULL,'Cold Princess'),(88,18,43,0,0,4,NULL,NULL,'Crimson Tempest'),(89,18,37,1,0,4,NULL,NULL,'Devil Princess'),(90,18,37,0,0,4,NULL,NULL,'Glitter Princess'),(91,18,40,0,0,4,NULL,NULL,'Gorgeous Princess'),(92,18,37,0,0,4,NULL,NULL,'Heroic Liaris'),(93,18,37,0,0,4,NULL,NULL,'Honor Princess'),(94,18,37,1,0,4,NULL,NULL,'Little Princess'),(95,18,37,1,0,4,NULL,NULL,'Regiment Princess'),(96,18,43,1,0,4,NULL,NULL,'Santa Princess'),(97,18,37,0,0,4,NULL,NULL,'Sparkle Princess'),(98,18,40,1,0,4,NULL,NULL,'Splash Princess'),(99,18,37,1,0,4,NULL,NULL,'Starving Mind'),(100,18,37,1,0,4,NULL,NULL,'Summer Princess'),(101,18,43,1,0,4,NULL,NULL,'Sweet Princess'),(102,18,37,0,0,3,NULL,NULL,'Sword Princess'),(103,19,45,0,0,4,NULL,NULL,'Dea Saint'),(104,20,40,1,0,4,NULL,NULL,'Beach Saint'),(105,21,40,0,0,4,NULL,NULL,'White Flash'),(106,22,40,0,0,4,NULL,NULL,'Brave Fighter'),(107,22,37,0,0,4,NULL,NULL,'Feline Lancer'),(108,22,43,1,0,4,NULL,NULL,'Holiday Cat'),(109,22,37,1,0,4,NULL,NULL,'Hyper Energetic'),(110,23,40,0,0,4,NULL,NULL,'Virgin Goddess'),(111,24,40,0,0,2,NULL,NULL,'Alchemist'),(112,24,40,0,0,4,NULL,NULL,'Almighty Fighter'),(113,24,40,0,0,3,NULL,NULL,'Combat Commander'),(114,24,37,0,0,4,NULL,NULL,'Onsen Princess'),(115,24,40,0,0,4,NULL,NULL,'Sailor Princess'),(116,24,40,0,0,4,NULL,NULL,'Thunderous Perseus'),(117,25,37,0,0,1,NULL,NULL,'Adventurer'),(118,25,37,0,0,4,NULL,NULL,'Argonaut'),(119,25,43,1,0,4,NULL,NULL,'Aspiring Elegance'),(120,25,37,1,0,4,NULL,NULL,'A Fresh Start'),(121,25,43,1,0,4,NULL,NULL,'Breezy Freese'),(122,25,37,0,0,4,NULL,NULL,'Honor Succession'),(123,25,37,0,0,2,NULL,NULL,'Liaris Freese'),(124,25,43,0,0,4,NULL,NULL,'Little Freese'),(125,25,37,0,0,4,NULL,NULL,'Moonlight Oath'),(126,25,43,1,0,4,NULL,NULL,'ODM Fighter'),(127,25,37,0,0,3,NULL,NULL,'Ox Slayer'),(128,25,43,1,0,4,NULL,NULL,'The White Rabbit'),(129,25,37,1,0,3,NULL,NULL,'Dungeon Addict'),(130,25,40,1,0,4,NULL,NULL,'The Edgiest Teen'),(131,26,37,1,0,4,NULL,NULL,'Little Wolf'),(132,26,37,1,0,4,NULL,NULL,'Moonlit Wolf'),(133,26,37,0,0,4,NULL,NULL,'Silver Moonshadow'),(134,26,37,0,0,3,NULL,NULL,'Ulfheoinn'),(135,26,37,0,0,2,NULL,NULL,'Werewolf'),(136,27,40,0,0,4,NULL,NULL,'Absolute Discover'),(137,27,40,0,0,4,NULL,NULL,'Black Cat'),(138,27,43,0,0,4,NULL,NULL,'Gallant Fighter'),(139,27,40,1,0,4,NULL,NULL,'Holly Wreath'),(140,28,37,1,0,4,NULL,NULL,'Wings of Freedom'),(141,29,45,0,0,4,NULL,NULL,'The Shadow'),(142,30,40,0,0,4,NULL,NULL,'Blessed Elf'),(143,30,43,0,0,4,NULL,NULL,'Cute Elf'),(144,30,43,0,0,3,NULL,NULL,'Maenads'),(145,30,43,0,0,4,NULL,NULL,'Maenad\'s Maiden'),(146,31,40,0,0,3,NULL,NULL,'Braver'),(147,31,37,0,0,4,NULL,NULL,'Brave Swordsman'),(148,31,40,0,0,2,NULL,NULL,'Captain'),(149,31,37,0,0,4,NULL,NULL,'Classy Gentleman'),(150,31,40,0,0,4,NULL,NULL,'Masked Braver'),(151,31,40,1,0,4,NULL,NULL,'Oriental Attire'),(152,32,46,0,0,2,NULL,NULL,'Elgarm'),(153,32,46,1,0,4,NULL,NULL,'Sunrise Axe'),(154,32,46,0,0,3,NULL,NULL,'Torrential'),(155,33,37,1,0,4,NULL,NULL,'Two-Wheel Racer'),(156,34,45,1,0,3,NULL,NULL,'Evanescent'),(157,34,40,0,0,4,NULL,NULL,'Fushi-Kaden'),(158,34,40,0,0,4,NULL,NULL,'Secret Onsen'),(159,34,45,1,0,4,NULL,NULL,'Sparkling Crystal'),(160,34,45,0,0,2,NULL,NULL,'Thousand Blades'),(161,35,46,0,0,3,NULL,NULL,'Solid Resolutions'),(162,35,46,0,0,2,NULL,NULL,'War God\'s Child'),(163,35,46,0,0,4,NULL,NULL,'Will of Iron'),(164,36,37,1,0,4,NULL,NULL,'Foreign Traveler'),(165,37,37,0,0,3,NULL,NULL,'Traveler'),(166,38,40,1,0,4,NULL,NULL,'Nightmare'),(167,39,43,0,0,4,NULL,NULL,'Bashful Elf'),(168,39,43,0,0,4,NULL,NULL,'Elven Awakening'),(169,39,43,0,0,4,NULL,NULL,'Incantation'),(170,39,43,0,0,3,NULL,NULL,'Lots of Love'),(171,39,43,0,0,3,NULL,NULL,'Thousand Elf'),(172,39,40,1,0,4,NULL,NULL,'Winter Elf'),(173,40,43,1,0,3,NULL,NULL,'Dark Class Act'),(174,40,40,1,0,4,NULL,NULL,'Elegant Elf'),(175,40,43,0,0,4,NULL,NULL,'Elf\'s Honor'),(176,40,43,0,0,4,NULL,NULL,'Geisha Elf'),(177,40,43,1,0,4,NULL,NULL,'Love Magic'),(178,40,43,1,0,4,NULL,NULL,'Offshore Elf'),(179,40,43,1,0,4,NULL,NULL,'Wicked Elf'),(180,41,37,1,0,4,NULL,NULL,'Strongest Soldier'),(181,42,45,0,0,3,NULL,NULL,'Artel Assist'),(182,42,43,1,0,3,NULL,NULL,'Artel Tart'),(183,42,45,0,0,4,NULL,NULL,'Disguised Pallum'),(184,42,37,0,0,4,NULL,NULL,'Echoing Arrow'),(185,42,43,0,0,4,NULL,NULL,'Enjoy Onsen'),(186,42,45,1,0,3,NULL,NULL,'Honestly Wicked'),(187,42,43,0,0,4,NULL,NULL,'Little Girl'),(188,42,43,0,0,4,NULL,NULL,'Longing Bride'),(189,42,43,0,0,4,NULL,NULL,'Lovely Travel'),(190,42,40,1,0,4,NULL,NULL,'Metal Robot'),(191,42,45,1,0,4,NULL,NULL,'Pallum Passion'),(192,42,43,1,0,4,NULL,NULL,'Summer Fun'),(193,42,45,0,0,2,NULL,NULL,'Supporter'),(194,42,43,1,0,4,NULL,NULL,'Sweet Devil'),(195,42,45,1,0,4,NULL,NULL,'Temptations'),(196,42,40,1,0,4,NULL,NULL,'Winter Cream'),(197,43,40,0,0,4,NULL,NULL,'Faithful Mage'),(198,44,37,0,0,4,NULL,NULL,'Black Fist'),(199,44,37,0,0,3,NULL,NULL,'Little Detective'),(200,45,37,1,0,4,NULL,NULL,'First in Class'),(201,46,37,0,0,3,NULL,NULL,'Dogfight'),(202,47,40,0,0,4,NULL,NULL,'Medicinal Archer'),(203,48,43,1,0,4,NULL,NULL,'Angel'),(204,49,37,0,0,4,NULL,NULL,'King'),(205,49,37,0,0,4,NULL,NULL,'Mighty King'),(206,49,37,0,0,4,NULL,NULL,'Superior Reign'),(207,50,45,1,0,4,NULL,NULL,'Photographer'),(208,51,40,0,0,3,NULL,NULL,'High Novice'),(209,51,40,1,0,4,NULL,NULL,'Night Buster'),(210,52,43,0,0,4,NULL,NULL,'Crimson Dazzle'),(211,52,43,0,0,4,NULL,NULL,'Dressed Royal'),(212,52,45,0,0,2,NULL,NULL,'Great Mage'),(213,52,43,0,0,4,NULL,NULL,'Holy White Royal'),(214,52,45,0,0,3,NULL,NULL,'Nine Hell'),(215,52,45,0,0,4,NULL,NULL,'Royal Elf'),(216,53,37,1,0,3,NULL,NULL,'Beach Winds'),(217,54,40,0,0,4,NULL,NULL,'Gale'),(218,53,40,0,0,4,NULL,NULL,'Gale Disguised'),(219,53,43,0,0,3,NULL,NULL,'Gale in Yukata'),(220,53,43,1,0,4,NULL,NULL,'Glistening Elf'),(221,53,43,1,0,4,NULL,NULL,'Holy Gale'),(222,53,37,0,0,4,NULL,NULL,'Knight Elf'),(223,53,37,1,0,4,NULL,NULL,'Pretty Lady'),(224,53,40,0,0,4,NULL,NULL,'Roaring Gale'),(225,53,46,1,0,4,NULL,NULL,'Vampiric Fairy'),(226,55,37,0,0,3,NULL,NULL,'Fist Fighter'),(227,55,37,1,0,4,NULL,NULL,'Blue Lotus'),(228,55,40,0,0,4,NULL,NULL,'Casino Lady'),(229,56,37,1,0,4,NULL,NULL,'Wondering Man'),(230,57,40,0,0,4,NULL,NULL,'Amber Sunflower'),(231,57,37,0,0,3,NULL,NULL,'Berserker'),(232,57,40,0,0,4,NULL,NULL,'Blustering Beauty'),(233,57,40,0,0,4,NULL,NULL,'Dancing Blessing'),(234,57,37,0,0,2,NULL,NULL,'Full Throttle'),(235,57,37,1,0,4,NULL,NULL,'Summer Swim'),(236,57,37,1,0,4,NULL,NULL,'Sweet Heart'),(237,58,40,0,0,3,NULL,NULL,'Backdraft'),(238,58,43,0,0,4,NULL,NULL,'Blushing Peony'),(239,58,37,0,0,4,NULL,NULL,'Crimson Dahlia'),(240,58,40,0,0,4,NULL,NULL,'Love Recipe'),(241,58,37,0,0,4,NULL,NULL,'Passionately Postal'),(242,58,37,0,0,2,NULL,NULL,'Pine Heart'),(243,58,37,1,0,4,NULL,NULL,'Suntan Girl'),(244,58,40,0,0,4,NULL,NULL,'Twinkle Stream'),(245,59,37,1,0,4,NULL,NULL,'Princess'),(246,60,37,1,0,3,NULL,NULL,'Cyclop\'s New Year'),(247,60,37,0,0,4,NULL,NULL,'Iron Warrior'),(248,61,46,0,0,2,NULL,NULL,'Blacksmith'),(249,61,46,0,0,4,NULL,NULL,'Howling Blade'),(250,61,46,0,0,3,NULL,NULL,'Ignis'),(251,61,40,0,0,4,NULL,NULL,'Smithy Expert'),(252,61,46,0,0,4,NULL,NULL,'Zeal Blast'),(253,62,43,1,0,4,NULL,NULL,'Love Lesson'),(254,62,40,0,0,2,NULL,NULL,'Samurai Girl'),(255,62,40,0,0,4,NULL,NULL,'Samurai Kunoichi'),(256,62,40,1,0,3,NULL,NULL,'Snow White'),(257,62,40,1,0,4,NULL,NULL,'The Traditional'),(258,62,40,1,0,4,NULL,NULL,'Yukata Beauty'),(259,62,40,0,0,3,NULL,NULL,'Zetsu Ei'),(260,63,37,0,0,0,NULL,NULL,'Title');
/*!40000 ALTER TABLE `adventurer` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-05 23:45:30
