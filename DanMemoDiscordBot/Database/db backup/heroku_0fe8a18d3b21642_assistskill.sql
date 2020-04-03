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
-- Table structure for table `assistskill`
--

DROP TABLE IF EXISTS `assistskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assistskill` (
  `assistskillid` int(11) NOT NULL AUTO_INCREMENT,
  `assistid` int(11) NOT NULL,
  `skillname` varchar(200) NOT NULL,
  PRIMARY KEY (`assistskillid`),
  KEY `assistid1_idx` (`assistid`),
  CONSTRAINT `assistid1` FOREIGN KEY (`assistid`) REFERENCES `assist` (`assistid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=766 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assistskill`
--

LOCK TABLES `assistskill` WRITE;
/*!40000 ALTER TABLE `assistskill` DISABLE KEYS */;
INSERT INTO `assistskill` VALUES (512,258,'Scholar Mind Trick+'),(513,258,'Scholar Mind Trick++'),(514,259,'Nurse\'s Healing+'),(515,259,'Nurse\'s Healing++'),(516,260,'Cat\'s Aid+'),(517,260,'Cat\'s Aid++'),(518,261,'By Instinct+'),(519,261,'By Instinct++'),(520,262,'Cheerful Support+'),(521,262,'Cheerful Support++'),(522,263,'Great Vision+'),(523,263,'Great Vision++'),(524,264,'Holy Bowstring+'),(525,264,'Holy Bowstring++'),(526,265,'Until the Sunrise+'),(527,265,'Until the Sunrise++'),(528,266,'Outbreak+'),(529,266,'Outbreak++'),(530,267,'Killer\'s Trickery+'),(531,267,'Killer\'s Trickery++'),(532,268,'Black Cat Inspection+'),(533,268,'Black Cat Inspection++'),(534,269,'Elemental Aura+'),(535,269,'Elemental Aura++'),(536,270,'Gentle Gaze+'),(537,270,'Gentle Gaze++'),(538,271,'Harvest\'s Grace+'),(539,271,'Harvest\'s Grace++'),(540,272,'Mother Bounty+'),(541,272,'Mother Bounty++'),(542,273,'Thank Me, Peasants!+'),(543,273,'Thank Me, Peasants!++'),(544,274,'Grace of Cups+'),(545,274,'Grace of Cups++'),(546,275,'Winding Intoxication+'),(547,275,'Winding Intoxication++'),(548,276,'Sweet Smile+'),(549,276,'Sweet Smile++'),(550,277,'Guild\'s Advice+'),(551,277,'Guild\'s Advice++'),(552,278,'Welcome!+'),(553,278,'Welcome!++'),(554,279,'Small Devotion+'),(555,279,'Small Devotion++'),(556,280,'Elven Investigation+'),(557,280,'Elven Investigation++'),(558,281,'Chocolate Advice+'),(559,281,'Chocolate Advice++'),(560,282,'Blessing Carols+'),(561,282,'Blessing Carols++'),(562,283,'Summer Fling+'),(563,283,'Summer Fling++'),(564,284,'Song of Honor+'),(565,284,'Song of Honor++'),(566,285,'Advice+'),(567,285,'Advice++'),(568,286,'Theory Library+'),(569,286,'Theory Library++'),(570,287,'Sanctuary Prayer+'),(571,287,'Sanctuary Prayer++'),(572,288,'Wicked Temptation+'),(573,288,'Wicked Temptation++'),(574,289,'Queen\'s Nightgown+'),(575,289,'Queen\'s Nightgown++'),(576,290,'Mad Love+'),(577,290,'Mad Love++'),(578,291,'Ceremonial Sensation+'),(579,291,'Ceremonial Sensation++'),(580,292,'In the Shadows+'),(581,292,'In the Shadows++'),(582,293,'Rampant Compassion+'),(583,293,'Rampant Compassion++'),(584,294,'Beauty Worship+'),(585,294,'Beauty Worship++'),(586,295,'Regina Coeli+'),(587,295,'Regina Coeli++'),(588,296,'I am Ganesha!+'),(589,296,'I am Ganesha!++'),(590,297,'Maharaja\'s Rule+'),(591,297,'Maharaja\'s Rule++'),(592,298,'Cry of a God+'),(593,298,'Cry of a God++'),(594,299,'Grand Order+'),(595,299,'Grand Order++'),(596,300,'Cunning Advice+'),(597,300,'Cunning Advice++'),(598,301,'Smith God\'s Eye+'),(599,301,'Smith God\'s Eye++'),(600,302,'Wrought Iron+'),(601,302,'Wrought Iron++'),(602,303,'Thunder Steel+'),(603,303,'Thunder Steel++'),(604,304,'Melody of Steel+'),(605,304,'Melody of Steel++'),(606,305,'Forge God\'s Refine+'),(607,305,'Forge God\'s Refine++'),(608,306,'Steel Guard+'),(609,306,'Steel Guard++'),(610,307,'Child Blacksmith\'s Crafting+'),(611,307,'Child Blacksmith\'s Crafting++'),(612,308,'Smooth Talk+'),(613,308,'Smooth Talk++'),(614,309,'Secret Intuition+'),(615,309,'Secret Intuition++'),(616,310,'Travel God\'s Grace+'),(617,310,'Travel God\'s Grace++'),(618,311,'Lucky Tour+'),(619,311,'Lucky Tour++'),(620,312,'Chocolate is War+'),(621,312,'Chocolate is War++'),(622,313,'Happiness Fever+'),(623,313,'Happiness Fever++'),(624,314,'Goddess\'s Prayer+'),(625,314,'Goddess\'s Prayer++'),(626,315,'Date with Bell+'),(627,315,'Date with Bell++'),(628,316,'Flame of Hope+'),(629,316,'Flame of Hope++'),(630,317,'Uncontrollable God+'),(631,317,'Uncontrollable God++'),(632,318,'With A Secret Map+'),(633,318,'With A Secret Map++'),(634,319,'Yearly Revival+'),(635,319,'Yearly Revival++'),(636,320,'Rise and Shine+'),(637,320,'Rise and Shine++'),(638,321,'Sparkling Smile+'),(639,321,'Sparkling Smile++'),(640,322,'Gold Fever+'),(641,322,'Gold Fever++'),(642,323,'Dazzling Wish+'),(643,323,'Dazzling Wish++'),(644,324,'Aid of Divine Fire+'),(645,324,'Aid of Divine Fire++'),(646,325,'Maiden\'s Protection+'),(647,325,'Maiden\'s Protection++'),(648,326,'God\'s Present+'),(649,326,'God\'s Present++'),(650,327,'Goddess Aura+'),(651,327,'Goddess Aura++'),(652,328,'Help of Child God+'),(653,328,'Help of Child God++'),(654,329,'My Heart to You+'),(655,329,'My Heart to You++'),(656,330,'Eternal Agape+'),(657,330,'Eternal Agape++'),(658,331,'Mummy Guidance+'),(659,331,'Mummy Guidance++'),(660,332,'Old Times+'),(661,332,'Old Times++'),(662,333,'Onsen Effect+'),(663,333,'Onsen Effect++'),(664,334,'Hilarious Service+'),(665,334,'Hilarious Service++'),(666,335,'Phantom Beast?+'),(667,335,'Phantom Beast?++'),(668,336,'Mysterious Bonfire+'),(669,336,'Mysterious Bonfire++'),(670,337,'Bouncing Blessing+'),(671,337,'Bouncing Blessing++'),(672,338,'Summer Holiday!+'),(673,338,'Summer Holiday!++'),(674,339,'Candy-Coated+'),(675,339,'Candy-Coated++'),(676,340,'Day of the Dream+'),(677,340,'Day of the Dream+'),(678,341,'Drilling Wind+'),(679,341,'Drilling Wind++'),(680,342,'Crimson Coat+'),(681,342,'Crimson Coat++'),(682,343,'Cutie Canon+'),(683,343,'Cutie Canon++'),(684,344,'Trickster\'s Skills+'),(685,344,'Trickster\'s Skills++'),(686,345,'Tonight, we feast!+'),(687,345,'Tonight, we feast!++'),(688,346,'Jester\'s Policy+'),(689,346,'Jester\'s Policy++'),(690,347,'Just for Fun+'),(691,347,'Just for Fun++'),(692,348,'Say What?!+'),(693,348,'Say What?!++'),(694,349,'The Masked Grin+'),(695,349,'The Masked Grin++'),(696,350,'Amusing Agitation+'),(697,350,'Amusing Agitation++'),(698,351,'My time, finally+'),(699,351,'My time, finally++'),(700,352,'Cleaning Skills+'),(701,352,'Cleaning Skills++'),(702,353,'Service Skills+'),(703,353,'Service Skills++'),(704,354,'God\'s Medicine+'),(705,354,'God\'s Medicine++'),(706,355,'Medi-God\'s Grace+'),(707,355,'Medi-God\'s Grace++'),(708,356,'Secret Potion+'),(709,356,'Secret Potion++'),(710,357,'Fertility\'s Cheer+'),(711,357,'Fertility\'s Cheer++'),(712,358,'Straighten Up!+'),(713,358,'Straighten Up!++'),(714,359,'Critical Hint+'),(715,359,'Critical Hint++'),(716,360,'Happy Vacation+'),(717,360,'Happy Vacation++'),(718,361,'Rumor Hunter+'),(719,361,'Rumor Hunter++'),(720,362,'Child of the MediGod+'),(721,362,'Child of the MediGod++'),(722,363,'Giant\'s Prayer+'),(723,363,'Giant\'s Prayer++'),(724,364,'Mastery Lightning+'),(725,364,'Mastery Lightning++'),(726,365,'My name is Alf!+'),(727,365,'My name is Alf!++'),(728,366,'Chivalry\'s Lesson+'),(729,366,'Chivalry\'s Lesson++'),(730,367,'Hearty Lunch Box+'),(731,367,'Hearty Lunch Box++'),(732,368,'Heartful Smile+'),(733,368,'Heartful Smile++'),(734,369,'Chocomint Fertility+'),(735,369,'Chocomint Fertility++'),(736,370,'Sleight of Hands+'),(737,370,'Sleight of Hands++'),(738,371,'Fertility\'s Gift+'),(739,371,'Fertility\'s Gift++'),(740,372,'Promised Road Home+'),(741,372,'Phantom Beast?++'),(742,373,'Innocent Blessing+'),(743,373,'Innocent Blessing++'),(744,374,'Heavy Promise+'),(745,374,'Heavy Promise++'),(746,375,'Snow Gift+'),(747,375,'Snow Gift++'),(748,376,'Devilish Spur+'),(749,376,'Devilish Spur++'),(750,377,'Angelic Fertility+'),(751,377,'Angelic Fertility++'),(752,378,'War God\'s Grace+'),(753,378,'War God\'s Grace++'),(754,379,'War Rampage+'),(755,379,'War Rampage++'),(756,380,'Titan\'s Roar+'),(757,380,'Titan\'s Roar++'),(758,381,'It\'s Alright Now+'),(759,381,'It\'s Alright Now++'),(760,382,'Head-Turner+'),(761,382,'Head-Turner++'),(762,383,'Pose of Diligence+'),(763,383,'Pose of Diligence++'),(764,384,'Onsen Prayer+'),(765,384,'Onsen Prayer++');
/*!40000 ALTER TABLE `assistskill` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-02 15:51:12