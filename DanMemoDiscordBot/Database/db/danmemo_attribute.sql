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
) ENGINE=InnoDB AUTO_INCREMENT=394 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute`
--

LOCK TABLES `attribute` WRITE;
/*!40000 ALTER TABLE `attribute` DISABLE KEYS */;
INSERT INTO `attribute` VALUES (277,'damage'),(278,'foes'),(279,'strength'),(280,'physical_resist'),(281,'endurance'),(282,'agility'),(283,'ailment_resist'),(284,'mp_regen'),(285,'hp'),(286,'mp'),(287,'physical_attack'),(288,'magic_attack'),(289,'defense'),(290,'dexterity'),(291,'magic'),(292,'wind_resist'),(293,'magic_resist'),(294,'heal_modifier'),(295,'sleep'),(296,'earth_resist'),(297,'self'),(298,'skill'),(299,'hp_regen'),(300,''),(301,'penetration_rate'),(302,'penetration_damage'),(303,'status_buff'),(304,'dark_attack'),(305,'poison'),(306,'critical_damage'),(307,'light_resist'),(308,'guard_rate'),(309,'all_status'),(310,'indexed_to'),(311,'insect_killer'),(312,'foe'),(313,'poison_resist'),(314,'wind_attack'),(315,'all_damage_resist'),(316,'null_physical_attack_no_special'),(317,'beast_killer'),(318,'fire_resist'),(319,'stun'),(320,'ailment_cure'),(321,'spirit_killer'),(322,'seal'),(323,'dark_resist'),(324,'str_buff_removal_no_assist'),(325,'magic_buff_removal_no_assist'),(326,'light_attack'),(327,'wdark_resist'),(328,'material_killer'),(329,'heal'),(330,'allies'),(331,'mp_heal'),(332,'seal_resist'),(333,'curse_cure'),(334,'water_resist'),(335,'water_attack'),(336,'critical_rate'),(337,'hp_regen_removal_no_assist'),(338,'thunder_resist'),(339,'boost'),(340,'prevent_ko'),(341,'counter_rate'),(342,'unguard_rate'),(343,'speed'),(344,'null_magic_attack_no_special'),(345,'Dmg. +60% per each Target\'s Heal Reduction Skill'),(346,'fire_attack'),(347,'uncounter_rate'),(348,'fast_growth'),(349,'null_charm'),(350,'ox_slayer'),(351,'life_steal'),(352,'counter_damage'),(353,'single_damage_resist'),(354,'earth_attack'),(355,'stregth'),(356,'debuff_removal_no_assist'),(357,'mag_debuff_removal_no_assist'),(358,'taunt'),(359,'stun_resist'),(360,'charm'),(361,'cover'),(362,'ice_resist'),(363,'dexteriry'),(364,'slow'),(365,'giant_killer'),(366,'thunder_attack'),(367,'worm_killer'),(368,'status_debuff'),(369,'guard_rate_buff_removal_no_assist'),(370,'hp_buff_removal_no_assist'),(371,'plant_killer'),(372,'mp_drain'),(373,'When countering, instead of regular attack, Lo Heals an Ally with least % HP'),(374,'sa_gauge_charge'),(375,'all_damage_resist_removal_no_assist'),(376,'When countering, regular attack [Foe] with Ultra Unguard Rate'),(377,'Dmg. +50% per 1 [Self] Regen/All Attack Dmg. Reduction Skill'),(378,'Dmg. +60% per 1 [Self] Regen/All Attack Dmg. Reduction Skill'),(379,'dragon_killer'),(380,'penetration'),(381,'str_debuff_removal_no_assist'),(382,'When countering, instead of regular attack, [Foe] Str. & Mag. -45% for 2 turns'),(383,'physical_resist_buff_removal_no_assist'),(384,'taunt_resist'),(385,'desterity'),(386,'When countering, instead of regular attack, extends Status Buffs for Allies for 1 turn'),(387,'magical_resist'),(388,'Dmg. +15% per 1 [Self] Regen/Str. Buff Skill'),(389,'Dmg. +25% per 1 [Self] Regen/Str. Buff Skill'),(390,'sleep_resist'),(391,'charm_resist'),(392,'null_ailment'),(393,'slow_resist');
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

-- Dump completed on 2020-03-22  1:25:29
