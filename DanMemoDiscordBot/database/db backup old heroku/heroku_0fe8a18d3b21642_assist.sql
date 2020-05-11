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
-- Table structure for table `assist`
--

DROP TABLE IF EXISTS `assist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assist` (
  `assistid` int(11) NOT NULL AUTO_INCREMENT,
  `characterid` int(11) NOT NULL,
  `alias` varchar(200) DEFAULT NULL,
  `limited` tinyint(4) NOT NULL,
  `stars` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  PRIMARY KEY (`assistid`),
  KEY `charid_idx` (`characterid`),
  CONSTRAINT `characterid4` FOREIGN KEY (`characterid`) REFERENCES `character` (`characterid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1072 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assist`
--

LOCK TABLES `assist` WRITE;
/*!40000 ALTER TABLE `assist` DISABLE KEYS */;
INSERT INTO `assist` VALUES (884,576,'None',0,4,'All Aboard'),(885,514,'None',0,3,'Modern Medicine'),(886,516,'None',0,2,'Cat-Ears'),(887,516,'None',0,4,'Clumsy Detective'),(888,516,'None',0,3,'Lighthearted'),(889,577,'None',0,4,'Artless'),(890,578,'goblinslayer',1,4,'At Home'),(891,576,'None',0,4,'Azure Goddess'),(892,512,'idol',0,4,'Backstage Princess'),(893,579,'None',0,4,'Banquet Attire'),(894,580,'None',0,4,'Banquet Dress'),(895,581,'None',0,4,'Banquet Queen'),(896,545,'ova',0,4,'Bathing Beauty'),(897,581,'None',0,4,'Beautiful Admirer'),(898,521,'free_halloween',1,4,'Living Dead Child'),(899,576,'valentine',1,4,'Beloved Goddess'),(900,582,'dal',1,4,'Berserk'),(901,577,'None',0,4,'Black Rose'),(902,583,'None',0,4,'Brains and Beauty'),(903,576,'casino',0,4,'Bunny Goddess'),(904,542,'new_year',0,4,'Camellia Kimono'),(905,581,'None',0,4,'Captivating Beauty'),(906,576,'None',0,4,'Ceremonial Flame'),(907,584,'anniversary',1,4,'Chained Reign'),(908,576,'dal',1,4,'Chief Goddess'),(909,526,'None',0,2,'Sinister Cat'),(910,526,'detective',0,4,'The Sly Cat'),(911,585,'casino_swimsuit',0,4,'Colonel'),(912,586,'None',0,4,'Countess'),(913,539,'goblinslayer',1,4,'Cowgirl Dress'),(914,557,'casino_swimsuit',0,4,'Cyan'),(915,536,'halloween',1,4,'Dark Divine'),(916,576,'None',1,4,'Day For Exploring'),(917,585,'None',0,2,'Harvest Goddess'),(918,585,'None',0,3,'Mother Seedling'),(919,538,'None',0,4,'Devotion'),(920,587,'None',0,3,'Classy God'),(921,587,'None',0,3,'Tipsy Gaze'),(922,576,'april_fools',1,4,'Director Goddess'),(923,576,'new_year',1,4,'Dreaming Goddess'),(925,554,'None',0,4,'Dungeon Waitress'),(926,524,'dal',1,4,'Efreet'),(927,588,'None',0,3,'Advisor'),(928,588,'None',0,3,'Guild Inspector'),(929,588,'None',0,2,'Receptionist'),(930,588,'None',0,3,'Scholar'),(931,581,'new_year',1,4,'Elegant Queen'),(932,589,'christmas',1,4,'Elegant Vanguard'),(933,588,'None',0,4,'Elf\'s Gift'),(934,590,'loli',1,4,'Elven Childhood'),(935,591,'kino',1,4,'Explosive Girl'),(936,572,'new_year',0,4,'Festive Blade'),(937,576,'kino',1,4,'Filmic Goddess'),(938,584,'anniversary',1,4,'Final Reminiscence'),(939,581,'None',0,3,'Devious Emotion'),(940,581,'None',0,2,'Intrigued Goddess'),(941,581,'None',0,3,'Prowling for Lust'),(942,577,'sword_oratoria',0,4,'Gallant Formal'),(943,592,'None',0,2,'God of the Masses'),(944,592,'None',0,3,'Masked God'),(945,592,'None',0,3,'Mighty Elephant'),(946,535,'halloween',1,4,'Ghost'),(947,576,'christmas_free',1,4,'Gift Goddess'),(948,576,'casino',0,4,'Glitter Goddess'),(949,593,'None',0,4,'God of Light'),(950,594,'None',0,4,'God of Origins'),(951,595,'None',0,4,'God of War'),(952,587,'None',0,4,'God of Wine'),(953,596,'None',0,2,'Elder Smith'),(954,596,'None',0,3,'Godly Swordsmith'),(955,585,'None',0,4,'Golden Wheat'),(956,588,'valentine',1,4,'Handmade Elf'),(957,577,'None',0,3,'Burning Forge'),(958,577,'None',0,3,'Legendary Artisan'),(959,577,'None',0,2,'The One-Eyed'),(960,579,'None',0,3,'Fearless Smile'),(961,579,'None',0,2,'God of Traveler'),(962,597,'goblinslayer',1,4,'Hero of Six'),(963,576,'None',0,4,'Adventurer\'s set'),(964,576,'None',0,1,'Childish Goddess'),(965,576,'april_fools',1,3,'Cunning Goddess'),(966,576,'None',0,3,'Goddess\' Devotion'),(967,576,'None',0,2,'Goddess of Hearth'),(968,576,'None',0,3,'Goddess of Purity'),(969,576,'None',0,3,'Lovebird'),(970,576,'None',1,4,'Truly Sweet'),(971,598,'christmas',1,4,'Holiday Spirit'),(972,588,'christmas',1,4,'Holy Choir'),(973,599,'anniversary',0,4,'In The End'),(974,518,'orion',0,4,'Innocent Goddess'),(975,576,'christmas',1,4,'Jingle Bell'),(976,576,'None',1,4,'Kunoichi Goddess'),(977,520,'None',0,4,'Lawful Judge'),(978,600,'loli',1,4,'Little Dame'),(979,601,'loli',1,4,'Little Goddess'),(980,521,'None',1,4,'Living Dead'),(981,580,'None',0,3,'Cheers!'),(982,580,'None',0,2,'Crafty Goddess'),(983,580,'None',0,3,'Red Quipster'),(984,580,'None',0,3,'Trickster'),(985,554,'None',0,2,'Fertility Helper'),(986,554,'None',0,3,'Prideful Waitress'),(987,592,'None',0,4,'Maharaja Elephant'),(988,602,'None',0,3,'God Neighbor'),(989,602,'None',0,3,'God of Medicine'),(990,602,'None',0,2,'Pharmacist'),(991,603,'None',0,2,'Fertilty\'s Mom'),(992,603,'None',0,3,'Overwhelm'),(993,588,'free_swimsuit',1,4,'Midsummer Maiden'),(994,588,'None',0,4,'Minstrel Elf'),(995,604,'None',0,2,'Guild Worker'),(996,604,'None',0,3,'Workplace Gossip'),(997,576,'orion',0,4,'Moonlight Reunion'),(998,576,'halloween',1,4,'Mummy Goddess'),(999,557,'free',0,3,'Silver Pharmacist'),(1000,598,'new_year',0,4,'New Year Kimono'),(1001,602,'new_year',0,4,'New Year Medic'),(1002,605,'anniversary',1,4,'Nomadic Bard'),(1003,580,'None',0,4,'Oni Demon'),(1004,545,'onsen',0,4,'Onsen Samurai'),(1005,512,'village',0,4,'Outside Orario'),(1006,576,'orion',0,4,'Pajama Goddess'),(1007,576,'onsen',0,4,'Paradise Mood'),(1008,576,'og',0,4,'Part-time Goddess'),(1009,606,'dal',1,4,'Princess'),(1010,579,'free_idol',1,4,'Producer'),(1011,598,'bride',0,4,'Pure Bride'),(1012,598,'None',0,4,'Pure-White Dress'),(1013,581,'None',0,4,'Queen of Beauty'),(1014,576,'christmas',1,4,'Reindeer Goddess'),(1015,549,'None',0,3,'Elven Employee'),(1016,607,'None',0,4,'Sacred Cup'),(1017,576,'None',0,4,'Sacred Fire'),(1018,576,'swimsuit',1,4,'Seaside Goddess'),(1019,608,'aot',1,4,'Sharp Thinker'),(1020,518,'orion',0,4,'Sleeping Innocence'),(1021,526,'None',0,4,'Sly Cat'),(1022,576,'april_fools',1,4,'Space Ribbon'),(1023,604,'swimsuit',1,4,'Summer Break'),(1024,576,'swimsuit',1,4,'Summer Goddess'),(1025,598,'None',1,4,'Summer Mischief'),(1026,576,'ova',0,4,'Swimsuit Contest'),(1027,598,'None',0,3,'A Loving Lunch'),(1028,598,'None',0,3,'Brightened Pub'),(1029,598,'None',1,4,'Candy Shop'),(1030,598,'None',0,2,'Fertility Staff'),(1031,598,'christmas',1,4,'Pure White'),(1032,609,'None',0,2,'Battle God'),(1033,609,'None',0,3,'War Incarnation'),(1034,610,'None',0,4,'The Night Queen'),(1035,580,'None',0,4,'Trickster\'s Truth'),(1036,598,'halloween',1,4,'Tricky Angel'),(1037,611,'aot',1,4,'Uncontrollable'),(1038,581,'None',0,4,'Utmost Beauty'),(1039,588,'None',0,4,'Valorous Elf'),(1040,612,'free',0,2,'Vigorous Medi-God'),(1041,588,'halloween',1,4,'Wannabe Nerd'),(1042,576,'bride',0,4,'Wedding Wish'),(1043,613,'None',0,4,'White Healer'),(1044,580,'None',1,4,'Whoever'),(1045,609,'christmas',1,4,'Winter War God'),(1046,576,'None',0,4,'Yellow Bird'),(1048,519,'ova',0,4,'Your Favorite'),(1052,581,'casino_free_swimsuit',1,4,'Dreamy Swimmer'),(1062,622,'loli',1,4,'Young Blacksmith');
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

-- Dump completed on 2020-04-24 13:01:37
