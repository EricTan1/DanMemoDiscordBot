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
-- Table structure for table `adventurerskill`
--

DROP TABLE IF EXISTS `adventurerskill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adventurerskill` (
  `adventurerskillid` int NOT NULL AUTO_INCREMENT,
  `adventurerid` int NOT NULL,
  `skillname` varchar(100) NOT NULL,
  `skilltype` varchar(100) NOT NULL,
  PRIMARY KEY (`adventurerskillid`),
  KEY `adventurerid_idx` (`adventurerid`),
  CONSTRAINT `adventurerid1` FOREIGN KEY (`adventurerid`) REFERENCES `adventurer` (`adventurerid`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2523 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adventurerskill`
--

LOCK TABLES `adventurerskill` WRITE;
/*!40000 ALTER TABLE `adventurerskill` DISABLE KEYS */;
INSERT INTO `adventurerskill` VALUES (1807,440,'Salvaging Aeriel','special'),(1808,440,'Complete Angelic Power','combat'),(1809,440,'Piko Hammer Slash','combat'),(1810,440,'Angelic Cut','combat'),(1811,441,'Timidus Lil Rafaga','special'),(1812,441,'Illusion Mech','combat'),(1813,441,'Illusion Piercer','combat'),(1814,441,'Veter Schrimm','combat'),(1815,442,'Special Placeholder','special'),(1816,442,'Skill 1 Placeholder','combat'),(1817,442,'Skill 2 Placeholder','combat'),(1818,442,'Skill 3 Placeholder','combat'),(1819,443,'Jackpot Lil Rafaga','special'),(1820,443,'Lucky Strike','combat'),(1821,443,'Lucky Chain','combat'),(1822,443,'Good Luck','combat'),(1823,444,'Pikopiko Aerial','special'),(1824,444,'Ariel?','combat'),(1825,444,'Tres Piercer?','combat'),(1826,444,'Veter Mech?','combat'),(1827,445,'Fleur Lil Rafaga','special'),(1828,445,'Carmine Blaze','combat'),(1829,445,'Cardinal Blade','combat'),(1830,445,'Blast of Pain','combat'),(1831,446,'Heaven\'s Catastrophe','special'),(1832,446,'Devilish Malevolence','combat'),(1833,446,'Disintegrate','combat'),(1834,446,'Ruthless Sword','combat'),(1835,447,'Gorgeous Lil Rafaga','special'),(1836,447,'Fortune Strike','combat'),(1837,447,'Fortune Chain','combat'),(1838,447,'Streak','combat'),(1839,448,'Amazon Lil Rafaga','special'),(1840,448,'Calma Lovushka','combat'),(1841,448,'Force Wind','combat'),(1842,448,'Veter Escudo','combat'),(1843,449,'Tempest Lil Rafaga','special'),(1844,449,'Ariel','combat'),(1845,449,'Tres Piercer','combat'),(1846,449,'Veter Mech','combat'),(1847,450,'Radiant Lil Rafaga','special'),(1848,450,'Blade Dance','combat'),(1849,450,'Phase Slicer','combat'),(1850,450,'Stiletto','combat'),(1851,451,'Innocent Lil Rafaga','special'),(1852,451,'Miliy Piercer','combat'),(1853,451,'Sheet Volya','combat'),(1854,451,'Miliy Mech','combat'),(1855,452,'Solid Lil Rafaga','special'),(1856,452,'Air Combination','combat'),(1857,452,'Tornado Break','combat'),(1858,452,'Revelation Cyclone','combat'),(1859,453,'Present Lil Rafaga','special'),(1860,453,'Kamita Mech','combat'),(1861,453,'Varder Mech','combat'),(1862,453,'Veter Grato','combat'),(1863,454,'Eternal Lil Rafaga','special'),(1864,454,'Syvet Mech','combat'),(1865,454,'Syvet Shpaga','combat'),(1866,454,'Lasvete Nyeba','combat'),(1867,455,'Illumines Lil Rafaga','special'),(1868,455,'Ã‰chthra Piercer','combat'),(1869,455,'Contempt Mech','combat'),(1870,455,'Prevent Wind','combat'),(1871,456,'Mortal Encounter','special'),(1872,456,'Devour Magic','combat'),(1873,456,'Bone Splitter','combat'),(1874,456,'Hunger','combat'),(1875,457,'Tidal Lil Rafaga','special'),(1876,457,'Aqua Blade','combat'),(1877,457,'Cobalt Edge','combat'),(1878,457,'Aqua Bite','combat'),(1879,458,'Mal Amour','special'),(1880,458,'Heart Breaker','combat'),(1881,458,'Pure Glittering Edge','combat'),(1882,458,'Passion Coordination','combat'),(1883,459,'Lil Rafaga','special'),(1884,459,'Ariel','combat'),(1885,459,'Tres Piercer','combat'),(1886,459,'Veter Mech','combat'),(1887,460,'Tera Sagrado','special'),(1888,460,'Dea Animus','combat'),(1889,460,'Dea Templum','combat'),(1890,460,'Gehenna Croce','combat'),(1891,461,'Shining Halation','special'),(1892,461,'Flooding Water','combat'),(1893,461,'Clear Water Potion','combat'),(1894,461,'Cure Stream Potion','combat'),(1895,462,'Splashing Barrage','special'),(1896,462,'Breezy Blade','combat'),(1897,462,'Sword Stream','combat'),(1898,462,'Water Spike','combat'),(1899,463,'Ruling Rift','special'),(1900,463,'Lancer Inspiration','combat'),(1901,463,'Riddle','combat'),(1902,463,'Dismantle','combat'),(1903,464,'Geiravor Dens','special'),(1904,464,'Cat Spike','combat'),(1905,464,'Quick Revenge','combat'),(1906,464,'Charge Growl','combat'),(1907,465,'Speed Party!','special'),(1908,465,'Fraction','combat'),(1909,465,'Breach','combat'),(1910,465,'Ferocious Piece','combat'),(1911,466,'Scratch Frantically','special'),(1912,466,'Charge Stake','combat'),(1913,466,'Rapid Scure','combat'),(1914,466,'Cat Inspire','combat'),(1915,467,'Cascading Glint Arrow','special'),(1916,467,'Lightning Fletcher','combat'),(1917,467,'Stoicism','combat'),(1918,467,'Pristine Presence','combat'),(1919,468,'Special Placeholder','special'),(1920,468,'Skill 1 Placeholder','combat'),(1921,468,'Skill 2 Placeholder','combat'),(1922,468,'Skill 3 Placeholder','combat'),(1923,469,'Throwing Mastery','special'),(1924,469,'Noxious Sting','combat'),(1925,469,'Vanishing Shroud','combat'),(1926,469,'Maker\'s Insight','combat'),(1927,470,'Special Placeholder','special'),(1928,470,'Skill 1 Placeholder','combat'),(1929,470,'Skill 2 Placeholder','combat'),(1930,470,'Skill 3 Placeholder','combat'),(1931,471,'Crack Burst','special'),(1932,471,'Spread Knife','combat'),(1933,471,'Diffusion Knife','combat'),(1934,471,'Flash Knowledge','combat'),(1935,472,'Chemistal Burst','special'),(1936,472,'Hypno Mist','combat'),(1937,472,'Plague Sting','combat'),(1938,472,'Illness Miasma','combat'),(1939,473,'Ascending Knives','special'),(1940,473,'Magnetic Maze','combat'),(1941,473,'Phase Shift','combat'),(1942,473,'Thunder Crash','combat'),(1943,474,'Special Placeholder','special'),(1944,474,'Skill 1 Placeholder','combat'),(1945,474,'Skill 2 Placeholder','combat'),(1946,474,'Skill 3 Placeholder','combat'),(1947,475,'Special Placeholder','special'),(1948,475,'Skill 1 Placeholder','combat'),(1949,475,'Skill 2 Placeholder','combat'),(1950,475,'Skill 3 Placeholder','combat'),(1951,476,'Firebolt Igniter','special'),(1952,476,'Seething','combat'),(1953,476,'Fiery Courage','combat'),(1954,476,'Noble Firebolt','combat'),(1955,477,'New Year\'s Strike','special'),(1956,477,'Blast Gleam','combat'),(1957,477,'Rapid Flash','combat'),(1958,477,'Double Defense','combat'),(1959,478,'Firebolt Fireworks','special'),(1960,478,'Firebolt','combat'),(1961,478,'Rapid Firebolt','combat'),(1962,478,'Preparation','combat'),(1963,479,'Argonaut Incarnation','special'),(1964,479,'Sharpness','combat'),(1965,479,'Molten Spike','combat'),(1966,479,'Sweeping Strike','combat'),(1967,480,'Special Placeholder','special'),(1968,480,'Skill 1 Placeholder','combat'),(1969,480,'Skill 2 Placeholder','combat'),(1970,480,'Skill 3 Placeholder','combat'),(1971,481,'Special Placeholder','special'),(1972,481,'Skill 1 Placeholder','combat'),(1973,481,'Skill 2 Placeholder','combat'),(1974,481,'Skill 3 Placeholder','combat'),(1975,482,'Sworn Strike','special'),(1976,482,'True Strike','combat'),(1977,482,'Glorius Aim','combat'),(1978,482,'Bright Fatality','combat'),(1979,483,'Argonaut Sky Chain','special'),(1980,483,'Blast Edge','combat'),(1981,483,'Wind Storm','combat'),(1982,483,'Gale Force','combat'),(1983,484,'Argonaut Firebolt','special'),(1984,484,'Firebolt','combat'),(1985,484,'Tri-Slicer','combat'),(1986,484,'Argonaut','combat'),(1987,485,'Luna Traviesa','special'),(1988,485,'Reverie Reps','combat'),(1989,485,'Fortis Spes','combat'),(1990,485,'Pierce Firebolt','combat'),(1991,486,'Dungeon Dance','special'),(1992,486,'Firebolt?','combat'),(1993,486,'Tri Slicer','combat'),(1994,486,'Argonaut?','combat'),(1995,487,'Darkest Doom\'s Edge','special'),(1996,487,'Slashing Atonement','combat'),(1997,487,'Blackest Aura','combat'),(1998,487,'Forbidden Left Arm','combat'),(1999,488,'Rumble Growl','special'),(2000,488,'Rufen Mut','combat'),(2001,488,'Grand Barrage','combat'),(2002,488,'Erde Angriff','combat'),(2003,489,'Vertilgen Wolf','special'),(2004,489,'Lethality','combat'),(2005,489,'Bloodboil','combat'),(2006,489,'Eternal Thirst','combat'),(2007,490,'Ulfheoinn','special'),(2008,490,'Wolfskehl','combat'),(2009,490,'Ulfr rogi','combat'),(2010,490,'Fenris Wolf','combat'),(2011,491,'Special Placeholder','special'),(2012,491,'Skill 1 Placeholder','combat'),(2013,491,'Skill 2 Placeholder','combat'),(2014,491,'Skill 3 Placeholder','combat'),(2015,492,'Special Placeholder','special'),(2016,492,'Skill 1 Placeholder','combat'),(2017,492,'Skill 2 Placeholder','combat'),(2018,492,'Skill 3 Placeholder','combat'),(2019,493,'Special Placeholder','special'),(2020,493,'Skill 1 Placeholder','combat'),(2021,493,'Skill 2 Placeholder','combat'),(2022,493,'Skill 3 Placeholder','combat'),(2023,494,'Felesculus','special'),(2024,494,'Fierce Dagger','combat'),(2025,494,'Siecle Thief','combat'),(2026,494,'Nox Haze','combat'),(2027,495,'Resonating Rift','special'),(2028,495,'Wanted Mark','combat'),(2029,495,'Land Spike','combat'),(2030,495,'Dagger Mastery','combat'),(2031,496,'Sharp Gift','special'),(2032,496,'Parrying Dagger','combat'),(2033,496,'Fend','combat'),(2034,496,'Laceration','combat'),(2035,497,'High Altitude Trajectory','special'),(2036,497,'Dive Attack','combat'),(2037,497,'Focused Attack','combat'),(2038,497,'Head-on Attack','combat'),(2039,498,'Verite Amour','special'),(2040,498,'Hekma Irada','combat'),(2041,498,'Nadam Reruabado','combat'),(2042,498,'God\'s Theorem','combat'),(2043,499,'Blinkedge Tornado','special'),(2044,499,'Windforce','combat'),(2045,499,'Sonic Wind','combat'),(2046,499,'Vitalize','combat'),(2047,500,'Electrocute','special'),(2048,500,'Trueno Natura','combat'),(2049,500,'Ardor Fulmen','combat'),(2050,500,'Cor Exaltatio','combat'),(2051,501,'Special Placeholder','special'),(2052,501,'Skill 1 Placeholder','combat'),(2053,501,'Skill 2 Placeholder','combat'),(2054,501,'Skill 3 Placeholder','combat'),(2055,502,'Special Placeholder','special'),(2056,502,'Skill 1 Placeholder','combat'),(2057,502,'Skill 2 Placeholder','combat'),(2058,502,'Skill 3 Placeholder','combat'),(2059,503,'Special Placeholder','special'),(2060,503,'Skill 1 Placeholder','combat'),(2061,503,'Skill 2 Placeholder','combat'),(2062,503,'Skill 3 Placeholder','combat'),(2063,504,'Furious Brave','special'),(2064,504,'Heightened Strike','combat'),(2065,504,'Slash Cleave','combat'),(2066,504,'Enrage','combat'),(2067,505,'Special Placeholder','special'),(2068,505,'Skill 1 Placeholder','combat'),(2069,505,'Skill 2 Placeholder','combat'),(2070,505,'Skill 3 Placeholder','combat'),(2071,506,'Tactical Tuxedo','special'),(2072,506,'Rush Spear','combat'),(2073,506,'Buster Edge','combat'),(2074,506,'Destructor','combat'),(2075,507,'Hell Finegas','special'),(2076,507,'Trample Lance','combat'),(2077,507,'Braver Order','combat'),(2078,507,'Destructor','combat'),(2079,508,'Secourer Tenebres','special'),(2080,508,'Void Circle','combat'),(2081,508,'Riptide Roller','combat'),(2082,508,'Crescent Abrasion','combat'),(2083,509,'Special Placeholder','special'),(2084,509,'Skill 1 Placeholder','combat'),(2085,509,'Skill 2 Placeholder','combat'),(2086,509,'Skill 3 Placeholder','combat'),(2087,510,'Mighty Sunrise','special'),(2088,510,'Strong Defense','combat'),(2089,510,'Attack Fortress','combat'),(2090,510,'Scintillate Ax','combat'),(2091,511,'Special Placeholder','special'),(2092,511,'Skill 1 Placeholder','combat'),(2093,511,'Skill 2 Placeholder','combat'),(2094,511,'Skill 3 Placeholder','combat'),(2095,512,'Biker Bash','special'),(2096,512,'Rev Up','combat'),(2097,512,'Burn Out','combat'),(2098,512,'Traction Burst','combat'),(2099,513,'Chigusa Senbu','special'),(2100,513,'Breath of Spring','combat'),(2101,513,'Purifying Water','combat'),(2102,513,'Anti-Spell Circle','combat'),(2103,514,'Narukami Sakura','special'),(2104,514,'Shunrai Shigure','combat'),(2105,514,'Shinobigoi Yukidoke','combat'),(2106,514,'Kushimitama Kagura','combat'),(2107,515,'The Invite to Onsen','special'),(2108,515,'Astonishing Slash','combat'),(2109,515,'Earth Calling Kodachi','combat'),(2110,515,'Chigo No Jin','combat'),(2111,516,'Chigusa Snowfall','special'),(2112,516,'Healing Waters','combat'),(2113,516,'Emerald Shine','combat'),(2114,516,'Divine Waters','combat'),(2115,517,'Special Placeholder','special'),(2116,517,'Skill 1 Placeholder','combat'),(2117,517,'Skill 2 Placeholder','combat'),(2118,517,'Skill 3 Placeholder','combat'),(2119,518,'Special Placeholder','special'),(2120,518,'Skill 1 Placeholder','combat'),(2121,518,'Skill 2 Placeholder','combat'),(2122,518,'Skill 3 Placeholder','combat'),(2123,519,'Special Placeholder','special'),(2124,519,'Skill 1 Placeholder','combat'),(2125,519,'Skill 2 Placeholder','combat'),(2126,519,'Skill 3 Placeholder','combat'),(2127,520,'Ouka-Nisouren','special'),(2128,520,'Spear of Absolute Bravery','combat'),(2129,520,'Fair and Square','combat'),(2130,520,'Do or Die Resistance','combat'),(2131,521,'Flute Shot','special'),(2132,521,'Projected Trajectory Shot','combat'),(2133,521,'Bolting Assault Shot','combat'),(2134,521,'Target Focused Shot','combat'),(2135,522,'Cannon Shot','special'),(2136,522,'Persuader','combat'),(2137,522,'First Chance','combat'),(2138,522,'Stance Square','combat'),(2139,523,'Eighth Bullet','special'),(2140,523,'Second Bullet','combat'),(2141,523,'Fourth Bullet','combat'),(2142,523,'Seventh Bullet','combat'),(2143,524,'Elf Ring','special'),(2144,524,'Karpos Dallos','combat'),(2145,524,'Karpos Pyr','combat'),(2146,524,'Anemos Fotia','combat'),(2147,525,'Eternal Burst','special'),(2148,525,'Lumen Keorn','combat'),(2149,525,'Lumen Solum','combat'),(2150,525,'Alvis Kairos','combat'),(2151,526,'Elf Ring','special'),(2152,526,'Arcs Ray','combat'),(2153,526,'Lux Maleficium','combat'),(2154,526,'Anemos Fotia','combat'),(2155,527,'Special Placeholder','special'),(2156,527,'Skill 1 Placeholder','combat'),(2157,527,'Skill 2 Placeholder','combat'),(2158,527,'Skill 3 Placeholder','combat'),(2159,528,'Special Placeholder','special'),(2160,528,'Skill 1 Placeholder','combat'),(2161,528,'Skill 2 Placeholder','combat'),(2162,528,'Skill 3 Placeholder','combat'),(2163,529,'Crystal Deluge','special'),(2164,529,'Blanc Glace','combat'),(2165,529,'Avalanche Neige','combat'),(2166,529,'Elle Grace','combat'),(2167,530,'Aspara Illusion','special'),(2168,530,'Arcs Ray?','combat'),(2169,530,'Ether Charge?','combat'),(2170,530,'Magias Decremento?','combat'),(2171,531,'Icechunk Impact','special'),(2172,531,'Sleet Fall','combat'),(2173,531,'Crushing Deluge','combat'),(2174,531,'Soothing Mist','combat'),(2175,532,'Har Rea Laevateinn','special'),(2176,532,'Kindling','combat'),(2177,532,'Laid Waste','combat'),(2178,532,'Immolation','combat'),(2179,533,'Radiant Lily','special'),(2180,533,'Clear Simmer','combat'),(2181,533,'Dispel Aureole','combat'),(2182,533,'Horoscope Ray','combat'),(2183,534,'Galactica Magica','special'),(2184,534,'Shining Wizard','combat'),(2185,534,'Keep it a secret!','combat'),(2186,534,'Magic Attack','combat'),(2187,535,'Aquatic Tornado','special'),(2188,535,'Aquatic Nova','combat'),(2189,535,'Aquatic Lure','combat'),(2190,535,'Aquatic Ray','combat'),(2191,536,'Spikey Avalanche','special'),(2192,536,'Black Brand','combat'),(2193,536,'Amplify Agony','combat'),(2194,536,'Shadow Feeder','combat'),(2195,537,'Fast Dimensional Attack','special'),(2196,537,'Horizontal Attack','combat'),(2197,537,'Slash','combat'),(2198,537,'Rotating Attack','combat'),(2199,538,'Special Placeholder','special'),(2200,538,'Skill 1 Placeholder','combat'),(2201,538,'Skill 2 Placeholder','combat'),(2202,538,'Skill 3 Placeholder','combat'),(2203,539,'Blizzard Rain','special'),(2204,539,'Icicle Arrow','combat'),(2205,539,'Mana Stock ','combat'),(2206,539,'Reforce Cancel','combat'),(2207,540,'Powering Arrow','special'),(2208,540,'Heal Medicine','combat'),(2209,540,'Chaos Pale','combat'),(2210,540,'Flaming Blade','combat'),(2211,541,'Lightning Arcbolt','special'),(2212,541,'Conductivity','combat'),(2213,541,'Enhanced Lightning','combat'),(2214,541,'Loaded Lightning','combat'),(2215,542,'Nature Blessing','special'),(2216,542,'Raising Arrow','combat'),(2217,542,'Through Pain','combat'),(2218,542,'Assault Potion','combat'),(2219,543,'Tumbling!','special'),(2220,543,'Cure Potion?','combat'),(2221,543,'Detoxification?','combat'),(2222,543,'Poison Arrow?','combat'),(2223,544,'Special Placeholder','special'),(2224,544,'Skill 1 Placeholder','combat'),(2225,544,'Skill 2 Placeholder','combat'),(2226,544,'Skill 3 Placeholder','combat'),(2227,545,'Bubble Bloom','special'),(2228,545,'Bubble Rush','combat'),(2229,545,'Wipe Away','combat'),(2230,545,'Hydro Blast','combat'),(2231,546,'Shining Explosion','special'),(2232,546,'Sparkle Circle','combat'),(2233,546,'Light Magic-Sword','combat'),(2234,546,'Shining Howling','combat'),(2235,547,'Pallum Satelite Cannon','special'),(2236,547,'Emergency Maintenance','combat'),(2237,547,'Caustic Smog','combat'),(2238,547,'Robot Punch','combat'),(2239,548,'Bursting Affection','special'),(2240,548,'Lively Heart','combat'),(2241,548,'Warm Heart','combat'),(2242,548,'Shy Burn','combat'),(2243,549,'Dolphin Army','special'),(2244,549,'Calamity Water','combat'),(2245,549,'Water Magic Sword','combat'),(2246,549,'Frozen Water','combat'),(2247,550,'Special Placeholder','special'),(2248,550,'Skill 1 Placeholder','combat'),(2249,550,'Skill 2 Placeholder','combat'),(2250,550,'Skill 3 Placeholder','combat'),(2251,551,'Trick or Sweet','special'),(2252,551,'Sweet Prank','combat'),(2253,551,'Magical Wand','combat'),(2254,551,'Bad Trick','combat'),(2255,552,'Sunshine Ray','special'),(2256,552,'Heal Medicine','combat'),(2257,552,'Hypnotic Arrow','combat'),(2258,552,'Ether Assist','combat'),(2259,553,'Flame Illusion','special'),(2260,553,'Bright Hearth','combat'),(2261,553,'Petit Feu','combat'),(2262,553,'Eggnog Potion','combat'),(2263,554,'Blinding Chant','special'),(2264,554,'Face Cutter','combat'),(2265,554,'Focused Will','combat'),(2266,554,'Enlightenment','combat'),(2267,555,'Assault Strike','special'),(2268,555,'Danger Detection','combat'),(2269,555,'Thorough Destruction','combat'),(2270,555,'Black Fist Crush','combat'),(2271,556,'Special Placeholder','special'),(2272,556,'Skill 1 Placeholder','combat'),(2273,556,'Skill 2 Placeholder','combat'),(2274,556,'Skill 3 Placeholder','combat'),(2275,557,'ODM Attacks','special'),(2276,557,'Cartwheel Attack','combat'),(2277,557,'Ascending Attack','combat'),(2278,557,'Non-Stop','combat'),(2279,558,'Invisible Slayer','special'),(2280,558,'Short Ripper','combat'),(2281,558,'Massive Force','combat'),(2282,558,'Wide Slash','combat'),(2283,559,'Gatling Arrow','special'),(2284,559,'Trick Arrow','combat'),(2285,559,'Buster Arrow','combat'),(2286,559,'Hiding Position','combat'),(2287,560,'Metatron','special'),(2288,560,'Heavenly Wings','combat'),(2289,560,'Sword of Light','combat'),(2290,560,'The Sun','combat'),(2291,561,'King\'s War Cry','special'),(2292,561,'Providence Eye','combat'),(2293,561,'Raging Impact','combat'),(2294,561,'Conquerer\'s Strike','combat'),(2295,562,'Lightning Strike','special'),(2296,562,'Slash of Light','combat'),(2297,562,'Tumultuous Zoom','combat'),(2298,562,'Bolt of Destruction','combat'),(2299,563,'Fangs of Apocalypse','special'),(2300,563,'Edge of Moment','combat'),(2301,563,'Rupture of Annihilation','combat'),(2302,563,'Mighty Power Slash','combat'),(2303,564,'Strobe Light','special'),(2304,564,'Full Throttle','combat'),(2305,564,'Pharmacy','combat'),(2306,564,'Voice of Poplar Street','combat'),(2307,565,'Special Placeholder','special'),(2308,565,'Skill 1 Placeholder','combat'),(2309,565,'Skill 2 Placeholder','combat'),(2310,565,'Skill 3 Placeholder','combat'),(2311,566,'Voltage Emission','special'),(2312,566,'Negative Electrode','combat'),(2313,566,'Positive Electrode','combat'),(2314,566,'Polarity Repulsion','combat'),(2315,567,'Special Placeholder','special'),(2316,567,'Skill 1 Placeholder','combat'),(2317,567,'Skill 2 Placeholder','combat'),(2318,567,'Skill 3 Placeholder','combat'),(2319,568,'Diamond Trail','special'),(2320,568,'Frost Nova','combat'),(2321,568,'Chilling Blast','combat'),(2322,568,'Winter\'s Grasp','combat'),(2323,569,'Special Placeholder','special'),(2324,569,'Skill 1 Placeholder','combat'),(2325,569,'Skill 2 Placeholder','combat'),(2326,569,'Skill 3 Placeholder','combat'),(2327,570,'Pillar of Heavens','special'),(2328,570,'Brightnening Weapon','combat'),(2329,570,'Lucent Force','combat'),(2330,570,'Zenith Sanction','combat'),(2331,571,'Special Placeholder','special'),(2332,571,'Skill 1 Placeholder','combat'),(2333,571,'Skill 2 Placeholder','combat'),(2334,571,'Skill 3 Placeholder','combat'),(2335,572,'Rea Laevateinn','special'),(2336,572,'Luna Aldis','combat'),(2337,572,'Veil Breath','combat'),(2338,572,'Wynn Fimbulvetr','combat'),(2339,573,'Milenas Wind','special'),(2340,573,'Shockwave Tempest','combat'),(2341,573,'Tempest Reverberato','combat'),(2342,573,'Elven Protection','combat'),(2343,574,'Luminous Wind','special'),(2344,574,'Noah Heal','combat'),(2345,574,'Vindblitz','combat'),(2346,574,'Teal Wind','combat'),(2347,575,'Luminous Vortex','special'),(2348,575,'Stormbolt','combat'),(2349,575,'Stellaris','combat'),(2350,575,'Downburst','combat'),(2351,576,'Special Placeholder','special'),(2352,576,'Skill 1 Placeholder','combat'),(2353,576,'Skill 2 Placeholder','combat'),(2354,576,'Skill 3 Placeholder','combat'),(2355,577,'Luminous Star Gale','special'),(2356,577,'Arctic','combat'),(2357,577,'Wind Shear','combat'),(2358,577,'Revelation Cyclone','combat'),(2359,578,'Faye Congelation','special'),(2360,578,'Glacies Nivis','combat'),(2361,578,'Valanga Neve','combat'),(2362,578,'Nous Oblio','combat'),(2363,579,'Furore Impaler','special'),(2364,579,'Velocity','combat'),(2365,579,'Cyclocity','combat'),(2366,579,'Windfury','combat'),(2367,580,'Confession D\'amour','special'),(2368,580,'Orange Veil','combat'),(2369,580,'Chagrin Chanter','combat'),(2370,580,'Gloire Tyffon','combat'),(2371,581,'Zephyrus Dawnbringer','special'),(2372,581,'Flashing','combat'),(2373,581,'Oppression','combat'),(2374,581,'Against Bane','combat'),(2375,582,'Vampiric Drain','special'),(2376,582,'Insite Wind','combat'),(2377,582,'Fairy Vamp','combat'),(2378,582,'Vind Chaos','combat'),(2379,583,'Muthee Sagrama','special'),(2380,583,'Visana','combat'),(2381,583,'Udayati','combat'),(2382,583,'Dharana','combat'),(2383,584,'Ambra Ugrata','special'),(2384,584,'Vidyut','combat'),(2385,584,'Ek Garjana','combat'),(2386,584,'Vajrapaat','combat'),(2387,585,'Patatrin Naga','special'),(2388,585,'Suzila','combat'),(2389,585,'Durbalata','combat'),(2390,585,'Askanda','combat'),(2391,586,'One-Bladed Bisection','special'),(2392,586,'Headwind','combat'),(2393,586,'Artisan Sword','combat'),(2394,586,'Concentration','combat'),(2395,587,'Shattering Onslaught','special'),(2396,587,'Static State','combat'),(2397,587,'Breaking Point','combat'),(2398,587,'Lightning Slash','combat'),(2399,588,'Special Placeholder','special'),(2400,588,'Skill 1 Placeholder','combat'),(2401,588,'Skill 2 Placeholder','combat'),(2402,588,'Skill 3 Placeholder','combat'),(2403,589,'Gamine Prune','special'),(2404,589,'Gardien Tonnerre','combat'),(2405,589,'Temerite Innocence','combat'),(2406,589,'Foudre Neige','combat'),(2407,590,'Vila Lassa','special'),(2408,590,'Pololokka Rodirro','combat'),(2409,590,'Stela Defesa','combat'),(2410,590,'Luna Pregare','combat'),(2411,591,'Special Placeholder','special'),(2412,591,'Skill 1 Placeholder','combat'),(2413,591,'Skill 2 Placeholder','combat'),(2414,591,'Skill 3 Placeholder','combat'),(2415,592,'Intense Heat','special'),(2416,592,'Tres Rodirro','combat'),(2417,592,'Audaz Gusto','combat'),(2418,592,'Pudo Rodirro','combat'),(2419,593,'Chocolata Soltar','special'),(2420,593,'Pecado Merienda','combat'),(2421,593,'Bonito Ruptura','combat'),(2422,593,'Bravo Gusto','combat'),(2423,594,'Special Placeholder','special'),(2424,594,'Skill 1 Placeholder','combat'),(2425,594,'Skill 2 Placeholder','combat'),(2426,594,'Skill 3 Placeholder','combat'),(2427,588,'Special Placeholder','special'),(2428,588,'Skill 1 Placeholder','combat'),(2429,588,'Skill 2 Placeholder','combat'),(2430,588,'Skill 3 Placeholder','combat'),(2431,595,'Sacred Peony','special'),(2432,595,'Flash Perfume','combat'),(2433,595,'Rampage Beat','combat'),(2434,595,'Heavenly Blow','combat'),(2435,596,'Galvanic Ravager','special'),(2436,596,'Roll of Thunder','combat'),(2437,596,'Volt Charge','combat'),(2438,596,'Unstable Thunder','combat'),(2439,597,'Special Placeholder','special'),(2440,597,'Skill 1 Placeholder','combat'),(2441,597,'Skill 2 Placeholder','combat'),(2442,597,'Skill 3 Placeholder','combat'),(2443,598,'Unrequited Rhapsody','special'),(2444,598,'Rumble Dance','combat'),(2445,598,'Bridal Path Dash','combat'),(2446,598,'Single-Minded Lover','combat'),(2447,599,'Special Placeholder','special'),(2448,599,'Skill 1 Placeholder','combat'),(2449,599,'Skill 2 Placeholder','combat'),(2450,599,'Skill 3 Placeholder','combat'),(2451,600,'Backdraft','special'),(2452,600,'Gritar Amor','combat'),(2453,600,'Amor Rampage','combat'),(2454,600,'Lindo Pastel','combat'),(2455,601,'Karna Lassa','special'),(2456,601,'Forte Grans','combat'),(2457,601,'Stela Scudo','combat'),(2458,601,'Luna Pleghierra','combat'),(2459,602,'Sword of the End','special'),(2460,602,'Spirit Extinction Blow','combat'),(2461,602,'Aerial Glint','combat'),(2462,602,'Sword Force','combat'),(2463,603,'Lepida Cyclops','special'),(2464,603,'Kakitsubata','combat'),(2465,603,'Rindo','combat'),(2466,603,'Housenka','combat'),(2467,604,'Iron Galive','special'),(2468,604,'Oniyuri','combat'),(2469,604,'Suzuran','combat'),(2470,604,'Hitujigusa','combat'),(2471,605,'Special Placeholder','special'),(2472,605,'Skill 1 Placeholder','combat'),(2473,605,'Skill 2 Placeholder','combat'),(2474,605,'Skill 3 Placeholder','combat'),(2475,606,'Special Placeholder','special'),(2476,606,'Skill 1 Placeholder','combat'),(2477,606,'Skill 2 Placeholder','combat'),(2478,606,'Skill 3 Placeholder','combat'),(2479,607,'Special Placeholder','special'),(2480,607,'Skill 1 Placeholder','combat'),(2481,607,'Skill 2 Placeholder','combat'),(2482,607,'Skill 3 Placeholder','combat'),(2483,608,'Thousand Flames','special'),(2484,608,'Name of the Flame','combat'),(2485,608,'The Art of Forging','combat'),(2486,608,'Spark Hammer','combat'),(2487,609,'Special Placeholder','special'),(2488,609,'Skill 1 Placeholder','combat'),(2489,609,'Skill 2 Placeholder','combat'),(2490,609,'Skill 3 Placeholder','combat'),(2491,610,'Tiger Fire','special'),(2492,610,'Tetsusaisen','combat'),(2493,610,'Chisouba','combat'),(2494,610,'Butei Tenshin','combat'),(2495,611,'Special Placeholder','special'),(2496,611,'Skill 1 Placeholder','combat'),(2497,611,'Skill 2 Placeholder','combat'),(2498,611,'Skill 3 Placeholder','combat'),(2499,612,'Tenka-chizan','special'),(2500,612,'Brutal Slash Kai','combat'),(2501,612,'Kagenui Yonshiki','combat'),(2502,612,'Skill 3 Placeholder','combat'),(2503,613,'Futsunomitama','special'),(2504,613,'Samidare-Giri','combat'),(2505,613,'Fuma-jin Nishiki','combat'),(2506,613,'Yoroi-kuzushii Nishiki','combat'),(2507,614,'Shimenawanomitama','special'),(2508,614,'Tora-giri','combat'),(2509,614,'Shining Katana','combat'),(2510,614,'Kourin-jin','combat'),(2511,615,'Furin-kazan','special'),(2512,615,'Catalpa Katana','combat'),(2513,615,'Kekkai-jin Sanshiki','combat'),(2514,615,'Ichino-Gata Gekishin','combat'),(2515,616,'Special Placeholder','special'),(2516,616,'Skill 1 Placeholder','combat'),(2517,616,'Skill 2 Placeholder','combat'),(2518,616,'Skill 3 Placeholder','combat'),(2519,617,'SpecialPlaceholder','special'),(2520,617,'Skill1','combat'),(2521,617,'skill2','combat'),(2522,617,'skill3','combat');
/*!40000 ALTER TABLE `adventurerskill` ENABLE KEYS */;
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
