-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: heroku_0fe8a18d3b21642
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
) ENGINE=InnoDB AUTO_INCREMENT=995 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attribute`
--

LOCK TABLES `attribute` WRITE;
/*!40000 ALTER TABLE `attribute` DISABLE KEYS */;
INSERT INTO `attribute` VALUES (277,'damage'),(278,'foes'),(279,'strength'),(280,'physical_resist'),(281,'endurance'),(282,'agility'),(283,'ailment_resist'),(284,'mp_regen'),(285,'hp'),(286,'mp'),(287,'physical_attack'),(288,'magic_attack'),(289,'defense'),(290,'dexterity'),(291,'magic'),(292,'wind_resist'),(293,'magic_resist'),(294,'heal_modifier'),(295,'sleep'),(296,'earth_resist'),(297,'self'),(298,'skill'),(299,'hp_regen'),(300,''),(301,'penetration_rate'),(302,'penetration_damage'),(303,'status_buff'),(304,'dark_attack'),(305,'poison'),(306,'critical_damage'),(307,'light_resist'),(308,'guard_rate'),(309,'all_status'),(310,'indexed_to'),(311,'insect_killer'),(312,'foe'),(313,'poison_resist'),(314,'wind_attack'),(315,'all_damage_resist'),(316,'null_physical_attack_no_special'),(317,'beast_killer'),(318,'fire_resist'),(319,'stun'),(320,'ailment_cure'),(321,'spirit_killer'),(322,'seal'),(323,'dark_resist'),(324,'str_buff_removal_no_assist'),(325,'magic_buff_removal_no_assist'),(326,'light_attack'),(327,'wdark_resist'),(328,'material_killer'),(329,'heal'),(330,'allies'),(331,'mp_heal'),(332,'seal_resist'),(333,'curse_cure'),(334,'water_resist'),(335,'water_attack'),(336,'critical_rate'),(337,'hp_regen_removal_no_assist'),(338,'thunder_resist'),(339,'boost'),(340,'prevent_ko'),(341,'counter_rate'),(342,'unguard_rate'),(343,'speed'),(344,'null_magic_attack_no_special'),(345,'Dmg. +60% per each Target\'s Heal Reduction Skill'),(346,'fire_attack'),(347,'uncounter_rate'),(348,'fast_growth'),(349,'null_charm'),(350,'ox_slayer'),(351,'life_steal'),(352,'counter_damage'),(353,'single_damage_resist'),(354,'earth_attack'),(355,'stregth'),(356,'debuff_removal_no_assist'),(357,'mag_debuff_removal_no_assist'),(358,'taunt'),(359,'stun_resist'),(360,'charm'),(361,'cover'),(362,'ice_resist'),(363,'dexteriry'),(364,'slow'),(365,'giant_killer'),(366,'thunder_attack'),(367,'worm_killer'),(368,'status_debuff'),(369,'guard_rate_buff_removal_no_assist'),(370,'hp_buff_removal_no_assist'),(371,'plant_killer'),(372,'mp_drain'),(373,'When countering, instead of regular attack, Lo Heals an Ally with least % HP'),(374,'sa_gauge_charge'),(375,'all_damage_resist_removal_no_assist'),(376,'When countering, regular attack [Foe] with Ultra Unguard Rate'),(377,'Dmg. +50% per 1 [Self] Regen/All Attack Dmg. Reduction Skill'),(378,'Dmg. +60% per 1 [Self] Regen/All Attack Dmg. Reduction Skill'),(379,'dragon_killer'),(380,'penetration'),(381,'str_debuff_removal_no_assist'),(382,'When countering, instead of regular attack, [Foe] Str. & Mag. -45% for 2 turns'),(383,'physical_resist_buff_removal_no_assist'),(384,'taunt_resist'),(385,'desterity'),(386,'When countering, instead of regular attack, extends Status Buffs for Allies for 1 turn'),(387,'magical_resist'),(388,'Dmg. +15% per 1 [Self] Regen/Str. Buff Skill'),(389,'Dmg. +25% per 1 [Self] Regen/Str. Buff Skill'),(392,'None'),(402,' Fast Growth. Null Charm\n'),(412,' When countering and attacking, regular M. Attack a Foe with Thunder Element\n'),(422,' Water Resist \n'),(432,' All Status \n'),(442,' Ability Pt. toward Giants'),(452,' Fast Growth. Null Charm.\n'),(462,' When countering and attacking, regular M. Attack a Foe with Thunder Element \n'),(472,' Fast Growth. Null Charm. \n'),(482,' When countering and attacking, regular M. Attack a Foe with Dark Element \n'),(492,' Light Resist \n'),(502,' Ability Pt. toward Ghosts'),(512,' Fast Growth \n'),(522,' Will of Thunder: I \n'),(532,' Water Resistance: I \n'),(542,' Luck: I \n'),(552,' Giant Killer \n'),(562,'per_each_targets_physical_resist_reduction_skill'),(572,' When countering and attacking, regular P. Attack a Foe with Wind Element \n'),(582,' Earth Resist \n'),(592,' Counter Damage'),(602,' When countering and attacking, regular P. Attack a Foe with Water Element \n'),(612,' Fire Resist \n'),(622,' Ability Pt. toward Worms'),(632,'physical_resist_debuff_removal_no_assist'),(642,' When countering, instead of attacking regularly, Taunt a Foe \n'),(652,' Guard Rate \n'),(662,' Mag. , Agi. \n'),(672,' Ability Pt. toward Aqua'),(682,'per_each_self_str_buff_skill'),(692,' HP Regen , MP Regen \n'),(702,' Str. , Agi. , Dex. \n'),(712,'per_each_self_str_buff'),(722,' When countering and attacking, regular P. Attack a Foe with Fire Element \n'),(732,' Penetration Damage \n'),(742,' Wind Resist \n'),(752,' Ability Pt. toward Insects'),(762,' When countering and attacking, regular M. Attack a Foe with Earth Element'),(763,' Penetration Damage'),(764,' Thunder Resist'),(765,' Mag. Agi. Dex.'),(766,' When countering, regular attack a Foe & Remove Agi. Buffs exc. Assist Skills.'),(767,' Guard Rate'),(768,' Fire Resist'),(769,' Str. Agi. Dex.'),(770,' When countering, regular attack a Foe & HP Heal of Dmg.'),(771,' Dark Resist'),(772,' Ability Pt. toward Beasts'),(773,'null_ailments'),(774,' Dex.'),(775,' Agi.'),(776,' Str.'),(777,' End.'),(778,' M.Resist'),(779,' Ailment Resist'),(780,' HP Regen'),(781,' [Foe] Regular attack when countering w/ 60% Taunt'),(782,' P.Resist M.Resist'),(783,' Light Resist'),(784,' Ability Pt. toward Ogres'),(785,' Ability Pt. toward Material'),(786,' Mag.'),(787,' Mag. End.'),(788,' P.Resist'),(789,' Agi. Dex.'),(790,' When countering and attacking, regular P. Attack a Foe & HP Heal of Dmg'),(791,' All Status'),(792,' MP Regen'),(793,' Ability Pt. toward Spirits'),(794,' Critical Damage'),(795,' When countering and attacking, regular M. Attack a Foe with Fire Element'),(796,' Wind Resist'),(797,' When countering and attacking, regular P. Attack a Foe with Thunder Element'),(798,' Water Resist'),(799,' HP Regen MP Regen'),(800,' When countering, instead of attacking regularly, it (Lo) Heals an Ally. Prioritizes an Ally with lower percentage HP.'),(801,' When countering, regular attack a Foe. Damage +80% only when a target is Slow.'),(802,' Mag. Agi.'),(803,' When countering and attacking, regular attack a Foe with Earth Element'),(804,' Str. when equipped with L.Sword'),(805,' When countering and attacking, regular P. Attack a Foe with Water Element'),(806,' Dark Resist When countering and attacking, regular P. Attack a Foe with Light Element'),(807,' When countering, instead of regular attack, Lo Heals an Ally with least HP'),(808,' Earth Resist'),(809,' When countering, it extends Status Buff for Allies for turn'),(810,' When countering and attacking, regular P. Attack a Foe with Wind Element'),(811,' Str. End. Agi. Dex.'),(812,' When countering and attacking, regular P. Attack a Foe with Light Element'),(813,' Str. Agi.'),(814,' When countering and attacking, regular M. Attack a Foe with Water Element'),(815,' When countering and attacking, regular P. Attack a Foe with Fire Element'),(816,' Ability Pt. toward Ox'),(817,' When countering and attacking, regular P. Attack a Foe with Dark Element'),(818,' When countering and attacking, regular P. Attack a Foe with Earth Element'),(819,' When countering, regular P. Attack a Foe and reduces Status Buff for turn'),(820,' Str. End.'),(821,' Ability Pt. toward Dragons'),(822,' Str. Dex.'),(823,' Mag. End. Agi. Dex.'),(824,' When countering, regular attack a Foe & Heal-25% for 4 turns.'),(825,' End. Agi. Dex.'),(826,' Wind Resist When countering and attacking, regular P. Attack a Foe with Fire Element'),(827,' Light Resist When countering and attacking, regular P. Attack a Foe with Dark Element'),(828,' [Foe] Regular attack when countering w/90% Stun'),(829,'sleep_resist'),(830,'slow_resist'),(831,'charm_resist'),(832,'water_damage'),(833,'light_resistance'),(834,'fire_resistance'),(835,'null_ailment'),(836,'null_magic'),(837,'null_physical'),(838,' strength'),(839,' endurance'),(840,' agility'),(841,' ailment_resist'),(842,' mp_regen'),(843,' magic'),(844,' endurance dexterity'),(845,' earth_resist'),(846,' physical_resist'),(847,' dexterity'),(848,' hp_regen'),(849,' penetration_damage'),(850,' wind_resist'),(851,' endurance dexterity agility'),(852,' critical_damage'),(853,' light_resist'),(854,' agility dexterity'),(855,' all_status'),(856,' magic_resist'),(857,' insect_killer'),(858,' strength agility'),(859,' endurance agility dexterity'),(860,' poison_resist'),(861,' endurance agility'),(862,' beast_killer'),(863,' fire_resist'),(864,'physical_resist_buff'),(865,' spirit_killer'),(866,' physical_resist magic_resist'),(867,' when_countering_and_attacking_regular_physical_attack_with_water_element'),(868,' wdark_resist'),(869,' material_killer'),(870,' when_counter_regular_attack_foe_sealed'),(871,' endurance agility dexterity strength'),(872,' guard_rate'),(873,' thunder_resist'),(874,'per_each_self_mag_buff'),(875,'dex'),(876,'Agi'),(877,'per_each_self_mag_buff_skill'),(878,'water_attack_removal_no_assist'),(879,'  Fire Resist'),(880,'  Critical Damage'),(881,'  Penetration Damage'),(882,'  Mag. Agi. Dex.'),(883,'  Ability Pt. toward Plants'),(884,' dark_resist'),(885,' strength dexterity'),(886,' water_resist'),(887,' fast_growth null_charm'),(888,' strength magic'),(889,' ox_slayer'),(890,' counter_attack_regular_physical_attack_fire'),(891,' counter_damage'),(892,'  Dark Resist'),(893,' stregth'),(894,'  Str. Agi.'),(895,'  Wind Resist'),(896,'  Agi. Dex.'),(897,'  Ability Pt. toward Beasts'),(898,'per_each_self_dex_buff_skill'),(899,' guard'),(900,' magic_resist physical_resist'),(901,' magic endurance agility dexterity'),(902,'status_debuff_removal_no_assist'),(903,'agility_buff_skill'),(904,' strength endurance agility dexterity'),(905,'  Dex.'),(906,'  Agi.'),(907,'  End.'),(908,'  Str.'),(909,'  Ailment Resist'),(910,'per_each_target_physical_resist_debuff'),(911,'Scapegoat during turn'),(912,'cover_single_attack'),(913,' counter_attack_regular_physical_attack_earth'),(914,' strength endurance'),(915,' magic endurance'),(916,' endurance dexteriry'),(917,'magic_resist_buff'),(918,' counter_attack_slow'),(919,' endurance dexterity agility magic'),(920,' counter_attack_magic_attack_water'),(921,' endurance agility dexterity magic'),(922,' counter_attack_magic_attack_dark'),(923,' strength agility dexterity'),(924,' giant_killer'),(925,' counter_attack_physical_attack_thunder'),(926,' agility dexterity strength'),(927,' worm_killer'),(928,'heal_buff_removal_no_assist'),(929,' magic agility'),(930,' plant_killer'),(931,' counter_attack_magical_attack_water'),(932,' When countering, instead of regular attack, Lo Heals an Ally with least % HP'),(933,' endurance agility dexteriry'),(934,'index_to'),(935,' When countering, regular attack [Foe] with Ultra Unguard Rate'),(936,' heal_counter_lowest_hp'),(937,'against_slow_target'),(938,' dragon_killer'),(939,' counter_attack_physical_attack_wind'),(940,' When countering, instead of regular attack, [Foe] Str. & Mag. -45% for 2 turns'),(941,'per_each_target_magic_resist'),(942,'  Guard Rate'),(943,'  Light Resist'),(944,'  Mag. End. Agi. Dex.'),(945,'  Ability Pt. toward Ghosts'),(946,'per_each_self_str_critical_rate_buff'),(947,' Thunder Resist counter_attack_physical_attack_earth'),(948,' endurance strength agility dexterity'),(949,'status_buff_removal_no_assist'),(950,'target_stun'),(951,'  When countering, instead of regular attack, Lo Heals an Ally with least HP'),(952,' endurance agility desterity'),(953,' When countering, instead of regular attack, extends Status Buffs for Allies for 1 turn'),(954,' physical_resist magical_resist'),(955,'per_each_target_single_damage_resist'),(956,'per_each_self_critical_rate'),(957,'fire_attack_removal_no_assist'),(958,'earth_attack_removal_no_assist'),(959,'wind_attack_removal_no_assist'),(960,'reflect_magic_attack_no_special'),(961,' dexterity endurance'),(962,' When countering, instead of attacking regularly, Taunt a Foe'),(963,'  When countering and attacking, regular P. Attack a Foe with Fire Element'),(964,'  Str. Agi. Dex.'),(965,'  Ability Pt. toward Insects'),(966,' Fast Growth Null Charm'),(967,' When countering and attacking, regular M. Attack a Foe with Thunder Element'),(968,'  Counter Damage'),(969,' When countering and attacking, regular M. Attack a Foe with Dark Element'),(970,'agility_buff_removal_no_assist'),(971,' Ability Pt. toward Ghost'),(972,' Thunder Resist+25%. When countering and attacking, regular P.Attack a Foe with Earth Element.'),(973,' Ability Pt. toward Plants'),(974,' When countering and attacking, regular P.Attack a Foe with Light Element.'),(975,'per_each_fire_attack_buff_skill'),(976,' Wind Resist+25%. When countering and attacking, regular M.Attack a Foe with Fire Element.'),(977,' magic_attack'),(978,' When countering and attacking, regular M. Attack a Foe with Fire Element.'),(979,'penetration_game'),(980,' When countering, instead of attacking regularly, it Nulls a Magic Attack one time for Self. (exc. Special Arts)'),(981,'removal_str_agi_dark_attack_no_assist'),(982,'per_each_self_light_attack_buff_skill'),(983,' Dark Resist +25%. When countering and attacking, regularP. Attack a Foe with Light Element.'),(984,' When countering and attacking, regular M. Attack a Foe with Water Element.'),(985,'per_each_self_critical_rate_buff_skill'),(986,'guard_resist'),(987,'removal_presist_no_assist'),(988,' When countering and attacking, regular P. Attack a Foe with Fire Element.'),(989,'removal_agi_dex_no_assist'),(990,' Regular attack a Foe when countering, Removes P. Resist Buffs exc. Assist Skills'),(991,'per_each_self_single_target_damage_resist'),(992,' Mag. when equipped with L.Sword'),(993,' Light Resist +25% & When countering and attacking, regular P. Attack a Foe with Dark Element'),(994,' Dark Resist +25% & When countering and attacking, regular P. Attack a Foe with Light Element');
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

-- Dump completed on 2020-05-11 11:19:20
