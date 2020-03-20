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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adventurer`
--

LOCK TABLES `adventurer` WRITE;
/*!40000 ALTER TABLE `adventurer` DISABLE KEYS */;
INSERT INTO `adventurer` VALUES (440,111,59,1,0,4,'None','None','Angelic Leader'),(441,111,62,0,0,4,'None','None','Bathroom Princess'),(442,111,59,0,0,2,'None','None','Battle Princess'),(443,111,59,0,0,4,'None','None','Bunny Princess'),(444,111,59,1,0,3,'None','None','Cold Princess'),(445,111,65,0,0,4,'None','None','Crimson Tempest'),(446,111,59,1,0,4,'None','None','Devil Princess'),(447,111,59,0,0,4,'None','None','Glitter Princess'),(448,111,62,0,0,4,'None','None','Gorgeous Princess'),(449,111,59,0,0,4,'None','None','Heroic Liaris'),(450,111,59,0,0,4,'None','None','Honor Princess'),(451,111,59,1,0,4,'None','None','Little Princess'),(452,111,59,1,0,4,'None','None','Regiment Princess'),(453,111,65,1,0,4,'None','None','Santa Princess'),(454,111,59,0,0,4,'None','None','Sparkle Princess'),(455,111,62,1,0,4,'None','None','Splash Princess'),(456,111,59,1,0,4,'None','None','Starving Mind'),(457,111,59,1,0,4,'None','None','Summer Princess'),(458,111,65,1,0,4,'None','None','Sweet Princess'),(459,111,59,0,0,3,'None','None','Sword Princess'),(460,112,67,0,0,4,'None','None','Dea Saint'),(461,113,62,1,0,4,'None','None','Beach Saint'),(462,114,62,0,0,4,'None','None','White Flash'),(463,115,62,0,0,4,'None','None','Brave Fighter'),(464,115,59,0,0,4,'None','None','Feline Lancer'),(465,115,65,1,0,4,'None','None','Holiday Cat'),(466,115,59,1,0,4,'None','None','Hyper Energetic'),(467,116,62,0,0,4,'None','None','Virgin Goddess'),(468,117,62,0,0,2,'None','None','Alchemist'),(469,117,62,0,0,4,'None','None','Almighty Fighter'),(470,117,62,0,0,3,'None','None','Combat Commander'),(471,117,59,0,0,4,'None','None','Onsen Princess'),(472,117,62,0,0,4,'None','None','Sailor Princess'),(473,117,62,0,0,4,'None','None','Thunderous Perseus'),(474,118,59,0,0,1,'None','None','Adventurer'),(475,118,59,0,0,4,'None','None','Argonaut'),(476,118,65,1,0,4,'None','None','Aspiring Elegance'),(477,118,59,1,0,4,'None','None','A Fresh Start'),(478,118,65,1,0,4,'None','None','Breezy Freese'),(479,118,59,0,0,4,'None','None','Honor Succession'),(480,118,59,0,0,2,'None','None','Liaris Freese'),(481,118,65,0,0,4,'None','None','Little Freese'),(482,118,59,0,0,4,'None','None','Moonlight Oath'),(483,118,65,1,0,4,'None','None','ODM Fighter'),(484,118,59,0,0,3,'None','None','Ox Slayer'),(485,118,65,1,0,4,'None','None','The White Rabbit'),(486,118,59,1,0,3,'None','None','Dungeon Addict'),(487,118,62,1,0,4,'None','None','The Edgiest Teen'),(488,119,59,1,0,4,'None','None','Little Wolf'),(489,119,59,1,0,4,'None','None','Moonlit Wolf'),(490,119,59,0,0,4,'None','None','Silver Moonshadow'),(491,119,59,0,0,3,'None','None','Ulfheoinn'),(492,119,59,0,0,2,'None','None','Werewolf'),(493,120,62,0,0,4,'None','None','Absolute Discover'),(494,120,62,0,0,4,'None','None','Black Cat'),(495,120,65,0,0,4,'None','None','Gallant Fighter'),(496,120,62,1,0,4,'None','None','Holly Wreath'),(497,121,59,1,0,4,'None','None','Wings of Freedom'),(498,122,67,0,0,4,'None','None','The Shadow'),(499,123,62,0,0,4,'None','None','Blessed Elf'),(500,123,65,0,0,4,'None','None','Cute Elf'),(501,123,65,0,0,3,'None','None','Maenads'),(502,123,65,0,0,4,'None','None','Maenad\'s Maiden'),(503,124,62,0,0,3,'None','None','Braver'),(504,124,59,0,0,4,'None','None','Brave Swordsman'),(505,124,62,0,0,2,'None','None','Captain'),(506,124,59,0,0,4,'None','None','Classy Gentleman'),(507,124,62,0,0,4,'None','None','Masked Braver'),(508,124,62,1,0,4,'None','None','Oriental Attire'),(509,125,68,0,0,2,'None','None','Elgarm'),(510,125,68,1,0,4,'None','None','Sunrise Axe'),(511,125,68,0,0,3,'None','None','Torrential'),(512,126,59,1,0,4,'None','None','Two-Wheel Racer'),(513,127,67,1,0,3,'None','None','Evanescent'),(514,127,62,0,0,4,'None','None','Fushi-Kaden'),(515,127,62,0,0,4,'None','None','Secret Onsen'),(516,127,67,1,0,4,'None','None','Sparkling Crystal'),(517,127,67,0,0,2,'None','None','Thousand Blades'),(518,128,68,0,0,3,'None','None','Solid Resolutions'),(519,128,68,0,0,2,'None','None','War God\'s Child'),(520,128,68,0,0,4,'None','None','Will of Iron'),(521,129,59,1,0,4,'None','None','Foreign Traveler'),(522,130,59,0,0,3,'None','None','Traveler'),(523,131,62,1,0,4,'None','None','Nightmare'),(524,132,65,0,0,4,'None','None','Bashful Elf'),(525,132,65,0,0,4,'None','None','Elven Awakening'),(526,132,65,0,0,4,'None','None','Incantation'),(527,132,65,0,0,3,'None','None','Lots of Love'),(528,132,65,0,0,3,'None','None','Thousand Elf'),(529,132,62,1,0,4,'None','None','Winter Elf'),(530,133,65,1,0,3,'None','None','Dark Class Act'),(531,133,62,1,0,4,'None','None','Elegant Elf'),(532,133,65,0,0,4,'None','None','Elf\'s Honor'),(533,133,65,0,0,4,'None','None','Geisha Elf'),(534,133,65,1,0,4,'None','None','Love Magic'),(535,133,65,1,0,4,'None','None','Offshore Elf'),(536,133,65,1,0,4,'None','None','Wicked Elf'),(537,134,59,1,0,4,'None','None','Strongest Soldier'),(538,135,67,0,0,3,'None','None','Artel Assist'),(539,135,65,1,0,3,'None','None','Artel Tart'),(540,135,67,0,0,4,'None','None','Disguised Pallum'),(541,135,59,0,0,4,'None','None','Echoing Arrow'),(542,135,65,0,0,4,'None','None','Enjoy Onsen'),(543,135,67,1,0,3,'None','None','Honestly Wicked'),(544,135,65,0,0,4,'None','None','Little Girl'),(545,135,65,0,0,4,'None','None','Longing Bride'),(546,135,65,0,0,4,'None','None','Lovely Travel'),(547,135,62,1,0,4,'None','None','Metal Robot'),(548,135,67,1,0,4,'None','None','Pallum Passion'),(549,135,65,1,0,4,'None','None','Summer Fun'),(550,135,67,0,0,2,'None','None','Supporter'),(551,135,65,1,0,4,'None','None','Sweet Devil'),(552,135,67,1,0,4,'None','None','Temptations'),(553,135,62,1,0,4,'None','None','Winter Cream'),(554,136,62,0,0,4,'None','None','Faithful Mage'),(555,137,59,0,0,4,'None','None','Black Fist'),(556,137,59,0,0,3,'None','None','Little Detective'),(557,138,59,1,0,4,'None','None','First in Class'),(558,139,59,0,0,3,'None','None','Dogfight'),(559,140,62,0,0,4,'None','None','Medicinal Archer'),(560,141,65,1,0,4,'None','None','Angel'),(561,142,59,0,0,4,'None','None','King'),(562,142,59,0,0,4,'None','None','Mighty King'),(563,142,59,0,0,4,'None','None','Superior Reign'),(564,143,67,1,0,4,'None','None','Photographer'),(565,144,62,0,0,3,'None','None','High Novice'),(566,144,62,1,0,4,'None','None','Night Buster'),(567,145,65,0,0,4,'None','None','Crimson Dazzle'),(568,145,65,0,0,4,'None','None','Dressed Royal'),(569,145,67,0,0,2,'None','None','Great Mage'),(570,145,65,0,0,4,'None','None','Holy White Royal'),(571,145,67,0,0,3,'None','None','Nine Hell'),(572,145,67,0,0,4,'None','None','Royal Elf'),(573,146,59,1,0,3,'None','None','Beach Winds'),(574,147,62,0,0,4,'None','None','Gale'),(575,146,62,0,0,4,'None','None','Gale Disguised'),(576,146,65,0,0,3,'None','None','Gale in Yukata'),(577,146,65,1,0,4,'None','None','Glistening Elf'),(578,146,65,1,0,4,'None','None','Holy Gale'),(579,146,59,0,0,4,'None','None','Knight Elf'),(580,146,59,1,0,4,'None','None','Pretty Lady'),(581,146,62,0,0,4,'None','None','Roaring Gale'),(582,146,68,1,0,4,'None','None','Vampiric Fairy'),(583,148,59,0,0,3,'None','None','Fist Fighter'),(584,148,59,1,0,4,'None','None','Blue Lotus'),(585,148,62,0,0,4,'None','None','Casino Lady'),(586,149,59,1,0,4,'None','None','Wondering Man'),(587,150,62,0,0,4,'None','None','Amber Sunflower'),(588,150,59,0,0,3,'None','None','Berserker'),(589,150,62,0,0,4,'None','None','Blustering Beauty'),(590,150,62,0,0,4,'None','None','Dancing Blessing'),(591,150,59,0,0,2,'None','None','Full Throttle'),(592,150,59,1,0,4,'None','None','Summer Swim'),(593,150,59,1,0,4,'None','None','Sweet Heart'),(594,151,62,0,0,3,'None','None','Backdraft'),(595,151,65,0,0,4,'None','None','Blushing Peony'),(596,151,59,0,0,4,'None','None','Crimson Dahlia'),(597,151,62,0,0,4,'None','None','Love Recipe'),(598,151,59,0,0,4,'None','None','Passionately Postal'),(599,151,59,0,0,2,'None','None','Pine Heart'),(600,151,59,1,0,4,'None','None','Suntan Girl'),(601,151,62,0,0,4,'None','None','Twinkle Stream'),(602,152,59,1,0,4,'None','None','Princess'),(603,153,59,1,0,3,'None','None','Cyclop\'s New Year'),(604,153,59,0,0,4,'None','None','Iron Warrior'),(605,154,68,0,0,2,'None','None','Blacksmith'),(606,154,68,0,0,4,'None','None','Howling Blade'),(607,154,68,0,0,3,'None','None','Ignis'),(608,154,62,0,0,4,'None','None','Smithy Expert'),(609,154,68,0,0,4,'None','None','Zeal Blast'),(610,155,65,1,0,4,'None','None','Love Lesson'),(611,155,62,0,0,2,'None','None','Samurai Girl'),(612,155,62,0,0,4,'None','None','Samurai Kunoichi'),(613,155,62,1,0,3,'None','None','Snow White'),(614,155,62,1,0,4,'None','None','The Traditional'),(615,155,62,1,0,4,'None','None','Yukata Beauty'),(616,155,62,0,0,3,'None','None','Zetsu Ei'),(617,156,59,0,0,0,'None','None','Title');
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

-- Dump completed on 2020-02-23 18:45:15
