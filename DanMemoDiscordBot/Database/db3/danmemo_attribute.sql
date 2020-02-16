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
-- Table structure for table `attribute`
--

DROP TABLE IF EXISTS `attribute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attribute` (
  `attributeid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`attributeid`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute`
--

LOCK TABLES `attribute` WRITE;
/*!40000 ALTER TABLE `attribute` DISABLE KEYS */;
INSERT INTO `attribute` VALUES (164,'damage'),(165,'foes'),(166,'strength'),(167,'physical_resist'),(168,'endurance'),(169,'agility'),(170,'ailment_resist'),(171,'mp_regen'),(172,'hp'),(173,'mp'),(174,'physical_attack'),(175,'magic_attack'),(176,'defense'),(177,'dexterity'),(178,'magic'),(179,'wind_resist'),(180,'magic_resist'),(181,'heal_modifier'),(182,'sleep'),(183,'earth_resist'),(184,'self'),(185,'skill'),(186,'hp_regen'),(187,''),(188,'penetration_rate'),(189,'penetration_damage'),(190,'status_buff'),(191,'dark_attack'),(192,'poison'),(193,'critical_damage'),(194,'light_resist'),(195,'guard_rate'),(196,'all_status'),(197,'indexed_to'),(198,'insect_killer'),(199,'foe'),(200,'poison_resist'),(201,'wind_attack'),(202,'all_damage_resist'),(203,'null_physical_attack_no_special'),(204,'beast_killer'),(205,'fire_resist'),(206,'stun'),(207,'ailment_cure'),(208,'spirit_killer'),(209,'seal'),(210,'dark_resist'),(211,'str_buff_removal_no_assist'),(212,'magic_buff_removal_no_assist'),(213,'light_attack'),(214,'wdark_resist'),(215,'material_killer'),(216,'heal'),(217,'allies'),(218,'mp_heal'),(219,'seal_resist'),(220,'curse_cure'),(221,'water_resist'),(222,'water_attack'),(223,'critical_rate'),(224,'hp_regen_removal_no_assist'),(225,'thunder_resist'),(226,'boost'),(227,'prevent_ko'),(228,'counter_rate'),(229,'unguard_rate'),(230,'speed'),(231,'null_magic_attack_no_special'),(232,'Dmg. +60% per each Target\'s Heal Reduction Skill'),(233,'fire_attack'),(234,'uncounter_rate'),(235,'fast_growth'),(236,'null_charm'),(237,'ox_slayer'),(238,'life_steal'),(239,'counter_damage'),(240,'single_damage_resist'),(241,'earth_attack'),(242,'stregth'),(243,'debuff_removal_no_assist'),(244,'mag_debuff_removal_no_assist'),(245,'taunt'),(246,'stun_resist'),(247,'charm'),(248,'cover'),(249,'ice_resist'),(250,'dexteriry'),(251,'slow'),(252,'giant_killer'),(253,'thunder_attack'),(254,'worm_killer'),(255,'status_debuff'),(256,'guard_rate_buff_removal_no_assist'),(257,'hp_buff_removal_no_assist'),(258,'plant_killer'),(259,'mp_drain'),(260,'When countering, instead of regular attack, Lo Heals an Ally with least % HP'),(261,'sa_gauge_charge'),(262,'all_damage_resist_removal_no_assist'),(263,'When countering, regular attack [Foe] with Ultra Unguard Rate'),(264,'Dmg. +50% per 1 [Self] Regen/All Attack Dmg. Reduction Skill'),(265,'Dmg. +60% per 1 [Self] Regen/All Attack Dmg. Reduction Skill'),(266,'dragon_killer'),(267,'penetration'),(268,'str_debuff_removal_no_assist'),(269,'When countering, instead of regular attack, [Foe] Str. & Mag. -45% for 2 turns'),(270,'physical_resist_buff_removal_no_assist'),(271,'taunt_resist'),(272,'desterity'),(273,'When countering, instead of regular attack, extends Status Buffs for Allies for 1 turn'),(274,'magical_resist'),(275,'Dmg. +15% per 1 [Self] Regen/Str. Buff Skill'),(276,'Dmg. +25% per 1 [Self] Regen/Str. Buff Skill');
/*!40000 ALTER TABLE `attribute` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-05 23:45:29
