-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: akcijars
-- ------------------------------------------------------
-- Server version	9.7.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'c9bf1245-5393-11f1-9ea7-005056c00001:1-27';

--
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrator` (
  `IdKor` int NOT NULL,
  PRIMARY KEY (`IdKor`),
  CONSTRAINT `FK_AdministratorKorisnik` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrator`
--

LOCK TABLES `administrator` WRITE;
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
/*!40000 ALTER TABLE `administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `akcija`
--

DROP TABLE IF EXISTS `akcija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `akcija` (
  `IdAkc` int NOT NULL AUTO_INCREMENT,
  `IdKor` int NOT NULL,
  `IdKat` int NOT NULL,
  `Naziv` varchar(100) NOT NULL,
  `Opis` varchar(1024) NOT NULL,
  `Datum` date NOT NULL,
  `Vreme` time NOT NULL,
  `Lokacija` varchar(50) NOT NULL,
  `MaxBrVolontera` int NOT NULL,
  `KontaktEmail` varchar(50) NOT NULL,
  `KontaktTelefon` varchar(20) NOT NULL,
  `Status` varchar(20) NOT NULL DEFAULT 'na_cekanju',
  `DatumKreiranja` date NOT NULL,
  `Slika` longblob,
  PRIMARY KEY (`IdAkc`),
  KEY `FK_AkcijaOrganizator` (`IdKor`),
  KEY `FK_AkcijaKategorija` (`IdKat`),
  CONSTRAINT `FK_AkcijaKategorija` FOREIGN KEY (`IdKat`) REFERENCES `kategorijaakcije` (`IdKat`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `FK_AkcijaOrganizator` FOREIGN KEY (`IdKor`) REFERENCES `organizator` (`IdKor`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `akcija`
--

LOCK TABLES `akcija` WRITE;
/*!40000 ALTER TABLE `akcija` DISABLE KEYS */;
/*!40000 ALTER TABLE `akcija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clanak`
--

DROP TABLE IF EXISTS `clanak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clanak` (
  `IdCla` int NOT NULL AUTO_INCREMENT,
  `IdKor` int NOT NULL,
  `Naslov` varchar(100) NOT NULL,
  `Tekst` text NOT NULL,
  `DatumKreiranja` date NOT NULL,
  `Status` varchar(20) NOT NULL DEFAULT 'na_cekanju',
  PRIMARY KEY (`IdCla`),
  KEY `FK_ClanakOrganizator` (`IdKor`),
  CONSTRAINT `FK_ClanakOrganizator` FOREIGN KEY (`IdKor`) REFERENCES `organizator` (`IdKor`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clanak`
--

LOCK TABLES `clanak` WRITE;
/*!40000 ALTER TABLE `clanak` DISABLE KEYS */;
/*!40000 ALTER TABLE `clanak` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dostignuce`
--

DROP TABLE IF EXISTS `dostignuce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dostignuce` (
  `IdDost` int NOT NULL AUTO_INCREMENT,
  `Naziv` varchar(50) NOT NULL,
  `Opis` varchar(255) NOT NULL,
  `Ikonica` blob,
  PRIMARY KEY (`IdDost`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dostignuce`
--

LOCK TABLES `dostignuce` WRITE;
/*!40000 ALTER TABLE `dostignuce` DISABLE KEYS */;
/*!40000 ALTER TABLE `dostignuce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fotografijaakcije`
--

DROP TABLE IF EXISTS `fotografijaakcije`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fotografijaakcije` (
  `IdFot` int NOT NULL AUTO_INCREMENT,
  `IdAkc` int NOT NULL,
  `Putanja` varchar(255) NOT NULL,
  PRIMARY KEY (`IdFot`),
  KEY `FK_FotografijaAkcija` (`IdAkc`),
  CONSTRAINT `FK_FotografijaAkcija` FOREIGN KEY (`IdAkc`) REFERENCES `akcija` (`IdAkc`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fotografijaakcije`
--

LOCK TABLES `fotografijaakcije` WRITE;
/*!40000 ALTER TABLE `fotografijaakcije` DISABLE KEYS */;
/*!40000 ALTER TABLE `fotografijaakcije` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kategorijaakcije`
--

DROP TABLE IF EXISTS `kategorijaakcije`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kategorijaakcije` (
  `IdKat` int NOT NULL AUTO_INCREMENT,
  `Naziv` varchar(50) NOT NULL,
  PRIMARY KEY (`IdKat`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kategorijaakcije`
--

LOCK TABLES `kategorijaakcije` WRITE;
/*!40000 ALTER TABLE `kategorijaakcije` DISABLE KEYS */;
/*!40000 ALTER TABLE `kategorijaakcije` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `komentar`
--

DROP TABLE IF EXISTS `komentar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `komentar` (
  `IdKom` int NOT NULL AUTO_INCREMENT,
  `IdKor` int NOT NULL,
  `IdCla` int NOT NULL,
  `Tekst` text NOT NULL,
  `DatumKomentara` date NOT NULL,
  PRIMARY KEY (`IdKom`),
  KEY `FK_KomentarKorisnik` (`IdKor`),
  KEY `FK_KomentarClanak` (`IdCla`),
  CONSTRAINT `FK_KomentarClanak` FOREIGN KEY (`IdCla`) REFERENCES `clanak` (`IdCla`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_KomentarKorisnik` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `komentar`
--

LOCK TABLES `komentar` WRITE;
/*!40000 ALTER TABLE `komentar` DISABLE KEYS */;
/*!40000 ALTER TABLE `komentar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik`
--

DROP TABLE IF EXISTS `korisnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik` (
  `IdKor` int NOT NULL AUTO_INCREMENT,
  `KorisnickoIme` varchar(50) NOT NULL,
  `Lozinka` varchar(50) NOT NULL,
  `Ime` varchar(50) NOT NULL,
  `Prezime` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `DatumRegistracije` date NOT NULL,
  PRIMARY KEY (`IdKor`),
  UNIQUE KEY `KorisnickoIme` (`KorisnickoIme`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik`
--

LOCK TABLES `korisnik` WRITE;
/*!40000 ALTER TABLE `korisnik` DISABLE KEYS */;
/*!40000 ALTER TABLE `korisnik` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizator`
--

DROP TABLE IF EXISTS `organizator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizator` (
  `IdKor` int NOT NULL,
  `BrTelefona` varchar(20) NOT NULL,
  `NazivOrganizacije` varchar(100) NOT NULL,
  `Status` varchar(20) NOT NULL DEFAULT 'na_cekanju',
  PRIMARY KEY (`IdKor`),
  CONSTRAINT `FK_OrganizatorKorisnik` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizator`
--

LOCK TABLES `organizator` WRITE;
/*!40000 ALTER TABLE `organizator` DISABLE KEYS */;
/*!40000 ALTER TABLE `organizator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prijavavolontera`
--

DROP TABLE IF EXISTS `prijavavolontera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prijavavolontera` (
  `IdKor` int NOT NULL,
  `IdAkc` int NOT NULL,
  `DatumPrijave` date NOT NULL,
  `Status` varchar(20) NOT NULL DEFAULT 'na_cekanju',
  `BrSati` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`IdKor`,`IdAkc`),
  KEY `FK_PrijavaAkcija` (`IdAkc`),
  CONSTRAINT `FK_PrijavaAkcija` FOREIGN KEY (`IdAkc`) REFERENCES `akcija` (`IdAkc`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_PrijavaVolonter` FOREIGN KEY (`IdKor`) REFERENCES `volonter` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prijavavolontera`
--

LOCK TABLES `prijavavolontera` WRITE;
/*!40000 ALTER TABLE `prijavavolontera` DISABLE KEYS */;
/*!40000 ALTER TABLE `prijavavolontera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `slikaclanka`
--

DROP TABLE IF EXISTS `slikaclanka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `slikaclanka` (
  `IdSli` int NOT NULL AUTO_INCREMENT,
  `IdCla` int NOT NULL,
  `Putanja` varchar(255) NOT NULL,
  PRIMARY KEY (`IdSli`),
  KEY `FK_SlikaClanak` (`IdCla`),
  CONSTRAINT `FK_SlikaClanak` FOREIGN KEY (`IdCla`) REFERENCES `clanak` (`IdCla`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slikaclanka`
--

LOCK TABLES `slikaclanka` WRITE;
/*!40000 ALTER TABLE `slikaclanka` DISABLE KEYS */;
/*!40000 ALTER TABLE `slikaclanka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponzor`
--

DROP TABLE IF EXISTS `sponzor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponzor` (
  `IdKor` int NOT NULL,
  `BrTelefona` varchar(20) NOT NULL,
  `NazivOrganizacije` varchar(100) NOT NULL,
  `Status` varchar(20) NOT NULL DEFAULT 'na_cekanju',
  PRIMARY KEY (`IdKor`),
  CONSTRAINT `FK_SponzorKorisnik` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponzor`
--

LOCK TABLES `sponzor` WRITE;
/*!40000 ALTER TABLE `sponzor` DISABLE KEYS */;
/*!40000 ALTER TABLE `sponzor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponzorskaponuda`
--

DROP TABLE IF EXISTS `sponzorskaponuda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponzorskaponuda` (
  `IdPon` int NOT NULL AUTO_INCREMENT,
  `IdKor` int NOT NULL,
  `IdAkc` int NOT NULL,
  `Vrednost` int NOT NULL,
  `Opis` varchar(1024) DEFAULT NULL,
  `Status` varchar(20) NOT NULL DEFAULT 'na_cekanju',
  `DatumSlanja` date NOT NULL,
  PRIMARY KEY (`IdPon`),
  KEY `FK_PonudaSponzor` (`IdKor`),
  KEY `FK_PonudaAkcija` (`IdAkc`),
  CONSTRAINT `FK_PonudaAkcija` FOREIGN KEY (`IdAkc`) REFERENCES `akcija` (`IdAkc`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_PonudaSponzor` FOREIGN KEY (`IdKor`) REFERENCES `sponzor` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponzorskaponuda`
--

LOCK TABLES `sponzorskaponuda` WRITE;
/*!40000 ALTER TABLE `sponzorskaponuda` DISABLE KEYS */;
/*!40000 ALTER TABLE `sponzorskaponuda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volonter`
--

DROP TABLE IF EXISTS `volonter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `volonter` (
  `IdKor` int NOT NULL,
  `UkupnoSati` int NOT NULL DEFAULT '0',
  `PrimaPreporuke` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`IdKor`),
  CONSTRAINT `FK_VolonterKorisnik` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volonter`
--

LOCK TABLES `volonter` WRITE;
/*!40000 ALTER TABLE `volonter` DISABLE KEYS */;
/*!40000 ALTER TABLE `volonter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volonterdostignuce`
--

DROP TABLE IF EXISTS `volonterdostignuce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `volonterdostignuce` (
  `IdKor` int NOT NULL,
  `IdDost` int NOT NULL,
  `DatumOstvarivanja` date NOT NULL,
  PRIMARY KEY (`IdKor`,`IdDost`),
  KEY `FK_VDDostignuce` (`IdDost`),
  CONSTRAINT `FK_VDDostignuce` FOREIGN KEY (`IdDost`) REFERENCES `dostignuce` (`IdDost`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_VDVolonter` FOREIGN KEY (`IdKor`) REFERENCES `volonter` (`IdKor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volonterdostignuce`
--

LOCK TABLES `volonterdostignuce` WRITE;
/*!40000 ALTER TABLE `volonterdostignuce` DISABLE KEYS */;
/*!40000 ALTER TABLE `volonterdostignuce` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-19 18:41:54
