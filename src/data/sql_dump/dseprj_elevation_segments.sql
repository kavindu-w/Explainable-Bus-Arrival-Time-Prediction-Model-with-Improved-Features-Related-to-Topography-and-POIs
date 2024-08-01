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
-- Table structure for table `elevation_segments`
--

DROP TABLE IF EXISTS `elevation_segments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `elevation_segments` (
  `segment` int DEFAULT NULL,
  `segment_info` varchar(50) DEFAULT NULL,
  `direction` varchar(50) DEFAULT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `max_elevation` decimal(10,2) DEFAULT NULL,
  `avg_elevation` decimal(10,2) DEFAULT NULL,
  `route_segment_info` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elevation_segments`
--

LOCK TABLES `elevation_segments` WRITE;
/*!40000 ALTER TABLE `elevation_segments` DISABLE KEYS */;
INSERT INTO `elevation_segments` VALUES (1,'BT01 - 101','Kandy-Digana',7.2911503,80.6376356,532.00,511.65,'\r'),(2,'101 - 102','Kandy-Digana',7.2911503,80.6376356,532.00,529.50,'Devon TP - Malwathu\r'),(3,'102 - 103','Kandy-Digana',7.2909727,80.6471298,544.00,529.10,'Dharmaraja - Lewella junction\r'),(4,'103 - 104','Kandy-Digana',7.2930162,80.6528942,527.00,515.71,'Lewella junction - Thalwatta\r'),(5,'104 - 105','Kandy-Digana',7.2865668,80.6602601,488.00,480.33,'Thennekumbura Mosque - Thennekumbura Filling Station\r'),(6,'105 - 106','Kandy-Digana',7.2820263,80.6697177,468.00,450.00,'Thennekumbura Bridge - Kirimatiya Junction\r'),(7,'106 - 107','Kandy-Digana',7.2790886,80.6792798,480.00,472.56,'\r'),(8,'107 - 108','Kandy-Digana',7.2802721,80.6823479,485.00,481.83,'Ruhunu Foods - Police College\r'),(9,'108 - 109','Kandy-Digana',7.2817583,80.6865632,494.00,487.83,'\r'),(10,'109 - 110','Kandy-Digana',7.2817583,80.6865632,494.00,489.33,'Warapitiya - Warapitiya Agriculture\r'),(11,'110 - 111','Kandy-Digana',7.2827155,80.6975258,494.00,488.56,'Singha Super - Rifle Brigade\r'),(12,'111 - 112','Kandy-Digana',7.2873251,80.7112917,467.00,457.71,'Balagolla Shanika Hotel - Balagolla Kovil\r'),(13,'112 - 113','Kandy-Digana',7.2868848,80.7143315,475.00,473.67,'Balagolla Kovil - Balagolla Mosque\r'),(14,'113 - 114','Kandy-Digana',7.2885481,80.7221614,473.00,464.71,'\r'),(15,'114 - BT02','Kandy-Digana',7.2980473,80.7331450,525.00,516.60,'Digana Village - Digana\r');
/*!40000 ALTER TABLE `elevation_segments` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-30 13:13:59
