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
-- Table structure for table `dwell_poi_final`
--

DROP TABLE IF EXISTS `dwell_poi_final`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dwell_poi_final` (
  `stop_id` varchar(10) DEFAULT NULL,
  `route_id` int DEFAULT NULL,
  `direction` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `attraction_count` decimal(10,2) DEFAULT NULL,
  `hotel_count` decimal(10,2) DEFAULT NULL,
  `total_poi_count` int DEFAULT NULL,
  `average_poi_distance` decimal(20,18) DEFAULT NULL,
  `place_of_worship` int DEFAULT NULL,
  `place_of_education` int DEFAULT NULL,
  `healthcare` int DEFAULT NULL,
  `tourist_attractions` int DEFAULT NULL,
  `commercial_places` int DEFAULT NULL,
  `public_places` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dwell_poi_final`
--

LOCK TABLES `dwell_poi_final` WRITE;
/*!40000 ALTER TABLE `dwell_poi_final` DISABLE KEYS */;
INSERT INTO `dwell_poi_final` VALUES ('BT01',654,'Kandy-Digana','Kandy',7.2924622,80.6349778,0.00,0.00,15,0.002017715220843085,8,2,2,39,3,16),('101',654,'Kandy-Digana','Wales Park',7.2911860,80.6376619,0.00,0.00,13,0.002210126169724122,3,1,1,23,1,8),('102',654,'Kandy-Digana','Mahamaya',7.2878400,80.6458400,0.00,0.00,6,0.002406391573226052,0,8,1,2,0,1),('103',654,'Kandy-Digana','Lewella junction',7.2944300,80.6500300,0.00,0.00,5,0.002080851249405684,4,0,0,2,0,2),('104',654,'Kandy-Digana','Thalwatta',7.2867010,80.6603357,0.00,0.00,3,0.001164535715439251,2,0,0,1,0,1),('105',654,'Kandy-Digana','Thennekumbura Bridge',7.2818660,80.6660300,0.00,0.00,3,0.001912947389835339,2,1,0,0,0,2),('106',654,'Kandy-Digana','Kalapura Junction Busstop',7.2798300,80.6762100,0.00,0.00,6,0.000855341095432533,0,0,2,3,0,14),('107',654,'Kandy-Digana','Nattarampotha Junction Bus Stop',7.2791170,80.6794500,0.00,0.00,8,0.001086879709568372,1,0,2,2,0,7),('108',654,'Kandy-Digana','Kundasale New town',7.2809000,80.6841600,0.00,0.00,11,0.001867384510126336,1,0,4,3,0,6),('109',654,'Kandy-Digana','Warapitiya',7.2814900,80.6863500,0.00,0.00,9,0.000793834405865272,0,0,3,4,0,6),('110',654,'Kandy-Digana','Pallekele (Provincial Council)',7.2813224,80.6967600,0.00,0.00,3,0.001108069486904393,1,0,0,0,2,0),('111',654,'Kandy-Digana','Pachchakaatuwa',7.2847300,80.7053900,0.00,0.00,1,0.001722334491313621,1,0,0,0,0,0),('112',654,'Kandy-Digana','Balagolla',7.2873490,80.7140051,0.00,0.00,1,0.000980432941109811,0,0,0,0,0,0),('113',654,'Kandy-Digana','BOI',7.2841100,80.7221000,0.00,0.00,1,0.001238522769266522,0,0,0,0,0,1),('114',654,'Kandy-Digana','Kengalla',7.2915200,80.7213300,0.00,0.00,3,0.001638154109439565,1,2,0,0,0,0),('BT02',654,'Kandy-Digana','Digana',7.2989600,80.7347200,0.00,0.00,7,0.001695264655136488,2,0,0,0,0,4);
/*!40000 ALTER TABLE `dwell_poi_final` ENABLE KEYS */;
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
