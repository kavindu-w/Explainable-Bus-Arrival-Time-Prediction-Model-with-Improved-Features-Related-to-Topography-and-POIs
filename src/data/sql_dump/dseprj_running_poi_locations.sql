-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: dseprj
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `running_poi_locations`
--

DROP TABLE IF EXISTS `running_poi_locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `running_poi_locations` (
  `segment` int DEFAULT NULL,
  `segment_info` varchar(50) DEFAULT NULL,
  `direction` varchar(50) DEFAULT NULL,
  `center_location` varchar(100) DEFAULT NULL,
  `amenity_place_of_worship` varchar(512) DEFAULT NULL,
  `amenity_school` varchar(512) DEFAULT NULL,
  `amenity_college` varchar(255) DEFAULT NULL,
  `amenity_university` varchar(255) DEFAULT NULL,
  `amenity_kindergarten` varchar(255) DEFAULT NULL,
  `amenity_library` varchar(255) DEFAULT NULL,
  `amenity_hospital` varchar(255) DEFAULT NULL,
  `amenity_clinic` varchar(255) DEFAULT NULL,
  `amenity_doctors` varchar(255) DEFAULT NULL,
  `amenity_dentist` varchar(255) DEFAULT NULL,
  `amenity_pharmacy` varchar(255) DEFAULT NULL,
  `amenity_veterinary` varchar(255) DEFAULT NULL,
  `amenity_public_building` varchar(255) DEFAULT NULL,
  `amenity_shopping_center` varchar(255) DEFAULT NULL,
  `amenity_marketplace` varchar(255) DEFAULT NULL,
  `amenity_bus_station` varchar(255) DEFAULT NULL,
  `amenity_taxi` varchar(255) DEFAULT NULL,
  `amenity_charging_station` varchar(255) DEFAULT NULL,
  `amenity_ferry_terminal` varchar(255) DEFAULT NULL,
  `amenity_parking` varchar(512) DEFAULT NULL,
  `amenity_parking_entrance` varchar(255) DEFAULT NULL,
  `amenity_parking_space` varchar(255) DEFAULT NULL,
  `amenity_traffic_park` varchar(255) DEFAULT NULL,
  `amenity_fuel` varchar(255) DEFAULT NULL,
  `amenity_hotel` varchar(255) DEFAULT NULL,
  `amenity_motel` varchar(255) DEFAULT NULL,
  `amenity_hostel` varchar(255) DEFAULT NULL,
  `amenity_camp_site` varchar(255) DEFAULT NULL,
  `amenity_cinema` varchar(255) DEFAULT NULL,
  `amenity_theatre` varchar(255) DEFAULT NULL,
  `amenity_nightclub` varchar(255) DEFAULT NULL,
  `amenity_restaurant` varchar(1024) DEFAULT NULL,
  `amenity_cafe` varchar(1024) DEFAULT NULL,
  `amenity_fast_food` varchar(255) DEFAULT NULL,
  `amenity_pub` varchar(255) DEFAULT NULL,
  `amenity_post_office` varchar(255) DEFAULT NULL,
  `amenity_bank` varchar(255) DEFAULT NULL,
  `amenity_atm` varchar(255) DEFAULT NULL,
  `amenity_social_facility` varchar(255) DEFAULT NULL,
  `amenity_public_transport` varchar(255) DEFAULT NULL,
  `amenity_shelter` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `running_poi_locations`
--

LOCK TABLES `running_poi_locations` WRITE;
/*!40000 ALTER TABLE `running_poi_locations` DISABLE KEYS */;
/*!40000 ALTER TABLE `running_poi_locations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-30 13:13:58
