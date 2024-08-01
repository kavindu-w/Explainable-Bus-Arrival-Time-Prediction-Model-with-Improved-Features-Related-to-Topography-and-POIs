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
-- Table structure for table `bus_stops`
--

DROP TABLE IF EXISTS `bus_stops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_stops` (
  `stop_id` varchar(10) DEFAULT NULL,
  `route_id` varchar(10) DEFAULT NULL,
  `direction` varchar(50) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_stops`
--

LOCK TABLES `bus_stops` WRITE;
/*!40000 ALTER TABLE `bus_stops` DISABLE KEYS */;
INSERT INTO `bus_stops` VALUES ('BT01','654','Kandy-Digana','Kandy',7.29246223,80.63497780),('101','654','Kandy-Digana','Wales Park',7.29118602,80.63766185),('102','654','Kandy-Digana','Mahamaya',7.28784000,80.64584000),('103','654','Kandy-Digana','Lewella junction',7.29443000,80.65003000),('104','654','Kandy-Digana','Thalwatta',7.28670100,80.66033570),('105','654','Kandy-Digana','Thennekumbura Bridge',7.28186600,80.66603000),('106','654','Kandy-Digana','Kalapura Junction Busstop',7.27983000,80.67621000),('107','654','Kandy-Digana','Nattarampotha Junction Bus Stop',7.27911700,80.67945000),('108','654','Kandy-Digana','Kundasale New town',7.28090000,80.68416000),('109','654','Kandy-Digana','Warapitiya',7.28149000,80.68635000),('110','654','Kandy-Digana','Pallekele (Provincial Council)',7.28132237,80.69676000),('111','654','Kandy-Digana','Pachchakaatuwa',7.28473000,80.70539000),('112','654','Kandy-Digana','Balagolla',7.28734902,80.71400511),('113','654','Kandy-Digana','BOI',7.28411000,80.72210000),('114','654','Kandy-Digana','Kengalla',7.29152000,80.72133000),('BT02','654','Kandy-Digana','Digana',7.29896000,80.73472000);
/*!40000 ALTER TABLE `bus_stops` ENABLE KEYS */;
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
