-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: flask_ssis
-- ------------------------------------------------------
-- Server version	8.4.0

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
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `students_id` int NOT NULL AUTO_INCREMENT,
  `idNumber` varchar(20) DEFAULT NULL,
  `firstName` varchar(150) DEFAULT NULL,
  `lastName` varchar(150) DEFAULT NULL,
  `courseCode` varchar(100) DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `yearLevel` varchar(20) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `image_id` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`students_id`),
  UNIQUE KEY `students_id` (`students_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course_table` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'1231-2322','Bernard','Dadula','BSCA',NULL,'4th-Year','Male','http://res.cloudinary.com/sbpvdb61/image/upload/c_fill,h_50,w_50/jlqfjka4qs5psjnc3x5y'),(3,'2025-1001','John','Santos','BSCA',NULL,'1st-Year','Male',NULL),(4,'2025-1002','Maria','Reyes','BSCA',NULL,'2nd-Year','Female',NULL),(5,'2025-1003','Joshua','Dela Cruz','BSCA',NULL,'3rd-Year','Male',NULL),(6,'2025-1004','Angela','Garcia','BSCA',NULL,'4th-Year','Female',NULL),(7,'2025-1005','Kevin','Torres','BSCA',NULL,'1st-Year','Male',NULL),(8,'2025-1006','Nicole','Flores','BSCA',NULL,'2nd-Year','Female',NULL),(9,'2025-1007','Christian','Mendoza','BSCA',NULL,'3rd-Year','Male',NULL),(10,'2025-1008','Patricia','Castro','BSCA',NULL,'4th-Year','Female',NULL),(11,'2025-1009','Mark','Villanueva','BSCA',NULL,'2nd-Year','Male',NULL),(12,'2025-1010','Kimberly','Ramos','BSCA',NULL,'1st-Year','Female',NULL),(13,'2025-1011','Jerome','Aquino','BSCA',NULL,'4th-Year','Male',NULL),(14,'2025-1012','Christine','Navarro','BSCA',NULL,'3rd-Year','Female',NULL),(15,'2025-1013','Paul','Fernandez','BSCA',NULL,'2nd-Year','Male',NULL),(16,'2025-1014','Alyssa','Morales','BSCA',NULL,'1st-Year','Female',NULL),(17,'2025-1015','Ryan','Lopez','BSCA',NULL,'4th-Year','Male',NULL),(18,'2025-1016','Jasmine','Cruz','BSCA',NULL,'3rd-Year','Female',NULL),(19,'2025-1017','Carl','Domingo','BSCA',NULL,'2nd-Year','Male',NULL),(20,'2025-1018','Faith','Perez','BSCA',NULL,'1st-Year','Female',NULL),(21,'2025-1019','Nathan','Bautista','BSCA',NULL,'3rd-Year','Male',NULL),(22,'2025-1020','Shane','Gutierrez','BSCA',NULL,'4th-Year','Female',NULL),(23,'2025-1021','Ethan','Herrera','BSCA',NULL,'1st-Year','Male',NULL),(24,'2025-1022','Claire','Salazar','BSCA',NULL,'2nd-Year','Female',NULL),(25,'2025-1023','Noel','Valdez','BSCA',NULL,'3rd-Year','Male',NULL),(26,'2025-1024','Angel','Alvarez','BSCA',NULL,'4th-Year','Female',NULL),(27,'2025-1025','Miguel','Lim','BSCA',NULL,'2nd-Year','Male',NULL),(28,'2025-1026','Sophia','Tan','BSN',NULL,'1st-Year','Female',NULL),(29,'2025-1027','Daniel','Uy','BSN',NULL,'2nd-Year','Male',NULL),(30,'2025-1028','Grace','Chua','BSN',NULL,'3rd-Year','Female',NULL),(31,'2025-1029','Vincent','Go','BSN',NULL,'4th-Year','Male',NULL),(32,'2025-1030','Hannah','Yu','BSN',NULL,'1st-Year','Female',NULL),(33,'2025-1031','Sean','Co','BSN',NULL,'2nd-Year','Male',NULL),(34,'2025-1032','Rica','Ong','BSN',NULL,'3rd-Year','Female',NULL),(35,'2025-1033','Adrian','Sy','BSN',NULL,'4th-Year','Male',NULL),(36,'2025-1034','Ella','Lee','BSN',NULL,'2nd-Year','Female',NULL),(37,'2025-1035','Bryan','Chan','BSN',NULL,'1st-Year','Male',NULL),(38,'2025-1036','Julia','Kho','BSN',NULL,'3rd-Year','Female',NULL),(39,'2025-1037','Marco','Lao','BSN',NULL,'4th-Year','Male',NULL),(40,'2025-1038','Denise','Ang','BSN',NULL,'1st-Year','Female',NULL),(41,'2025-1039','Patrick','Tan','BSN',NULL,'2nd-Year','Male',NULL),(42,'2025-1040','Camille','Lim','BSN',NULL,'3rd-Year','Female',NULL),(43,'2025-1041','Joshua','Villareal','BSN',NULL,'4th-Year','Male',NULL),(44,'2025-1042','Bea','Rivera','BSN',NULL,'1st-Year','Female','http://res.cloudinary.com/sbpvdb61/image/upload/c_fill,h_50,w_50/uimuxigp1guhr7mpgkcv'),(45,'2025-1043','Ian','Soriano','BSN',NULL,'2nd-Year','Male',NULL),(46,'2025-1044','Karen','Mercado','BSN',NULL,'3rd-Year','Female',NULL),(47,'2025-1045','Ralph','Pascual','BSN',NULL,'4th-Year','Male',NULL),(48,'2025-1046','Trisha','Espino','BSN',NULL,'2nd-Year','Female',NULL),(49,'2025-1047','Kenneth','Abad','BSN',NULL,'1st-Year','Male',NULL),(50,'2025-1048','Monica','Rosales','BSN',NULL,'3rd-Year','Female',NULL),(51,'2025-1049','Cedric','Del Rosario','BSN',NULL,'4th-Year','Male',NULL),(52,'2025-1050','Louise','Manalo','BSN',NULL,'2nd-Year','Female',NULL);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-02 22:31:23
