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
-- Table structure for table `running_poi_final`
--

DROP TABLE IF EXISTS `running_poi_final`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `running_poi_final` (
  `segment` int NOT NULL,
  `segment_info` varchar(50) DEFAULT NULL,
  `direction` varchar(50) DEFAULT NULL,
  `center_location` varchar(50) DEFAULT NULL,
  `total_poi_count` int DEFAULT NULL,
  `average_poi_distance` float DEFAULT NULL,
  `place_of_worship` int DEFAULT NULL,
  `place_of_education` int DEFAULT NULL,
  `hospital` int DEFAULT NULL,
  `healthcare` int DEFAULT NULL,
  `tourist_attractions` int DEFAULT NULL,
  `commercial_places` int DEFAULT NULL,
  `nearby_bus_stops` int DEFAULT NULL,
  `public_places` int DEFAULT NULL,
  `fuel_station` int DEFAULT NULL,
  `place_of_accommodation` int DEFAULT NULL,
  PRIMARY KEY (`segment`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `running_poi_final`
--

LOCK TABLES `running_poi_final` WRITE;
/*!40000 ALTER TABLE `running_poi_final` DISABLE KEYS */;
INSERT INTO `running_poi_final` VALUES (1,'BT01 - 101','Kandy-Digana','(7.2918241214999995, 80.636319825)',16,0.00235647,10,2,0,3,48,3,4,13,1,0),(2,'101 - 102','Kandy-Digana','(7.288573159, 80.644768605)',19,0.00643677,8,13,2,6,35,1,1,11,0,0),(3,'102 - 103','Kandy-Digana','(7.290925475, 80.64413128000001)',13,0.00371363,9,11,2,5,15,0,0,2,1,0),(4,'103 - 104','Kandy-Digana','(7.289621492, 80.65685642)',7,0.00761673,6,3,0,0,5,0,0,2,1,0),(5,'104 - 105','Kandy-Digana','(7.283234888, 80.664755335)',6,0.00359699,4,1,0,0,1,0,0,3,1,0),(6,'105 - 106','Kandy-Digana','(7.279895397, 80.675194515)',9,0.00320519,2,1,0,3,6,0,0,20,1,0),(7,'106 - 107','Kandy-Digana','(7.2795021774999995, 80.67779338)',9,0.00220875,1,0,0,3,5,0,0,18,1,0),(8,'107 - 108','Kandy-Digana','(7.279222128, 80.68046291)',13,0.00313367,2,0,1,6,5,0,0,10,1,0),(9,'108 - 109','Kandy-Digana','(7.2810372885, 80.684907075)',11,0.0017069,1,0,1,4,4,0,0,7,0,0),(10,'109 - 110','Kandy-Digana','(7.281714827, 80.691720285)',11,0.00595751,2,0,0,3,4,0,0,9,0,0),(11,'110 - 111','Kandy-Digana','(7.2826061515, 80.699184005)',4,0.00407945,2,0,0,1,0,0,0,2,0,0),(12,'111 - 112','Kandy-Digana','(7.2860636595, 80.70979107)',4,0.00497894,1,1,0,1,0,0,0,0,0,0),(13,'112 - 113','Kandy-Digana','(7.285331669, 80.716724465)',4,0.00286301,1,1,0,0,0,0,0,0,1,0),(14,'113 - 114','Kandy-Digana','(7.2878903075, 80.72173721)',4,0.00441749,3,2,0,0,0,0,0,0,1,0),(15,'114 - BT02','Kandy-Digana','(7.293090067, 80.72330829)',11,0.00951149,5,4,2,2,1,0,4,0,1,0);
/*!40000 ALTER TABLE `running_poi_final` ENABLE KEYS */;
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
