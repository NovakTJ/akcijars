-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: akcijars
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrator` (
  `IdKor` bigint NOT NULL,
  PRIMARY KEY (`IdKor`),
  CONSTRAINT `Administrator_IdKor_5b62c37a_fk_Korisnik_id` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrator`
--

LOCK TABLES `administrator` WRITE;
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
INSERT INTO `administrator` VALUES (1);
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
  `Naziv` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Opis` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Datum` date NOT NULL,
  `Vreme` time(6) NOT NULL,
  `Lokacija` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `MaxBrVolontera` int unsigned NOT NULL,
  `KontaktEmail` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `KontaktTelefon` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DatumKreiranja` date NOT NULL,
  `Slika` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `IdKor` bigint NOT NULL,
  `IdKat` int NOT NULL,
  `GeoSirina` double DEFAULT NULL,
  `GeoDuzina` double DEFAULT NULL,
  PRIMARY KEY (`IdAkc`),
  KEY `Akcija_IdKor_13b59a36_fk_Organizator_IdKor` (`IdKor`),
  KEY `Akcija_IdKat_85ae7aaa_fk_KategorijaAkcije_IdKat` (`IdKat`),
  CONSTRAINT `Akcija_IdKat_85ae7aaa_fk_KategorijaAkcije_IdKat` FOREIGN KEY (`IdKat`) REFERENCES `kategorijaakcije` (`IdKat`),
  CONSTRAINT `Akcija_IdKor_13b59a36_fk_Organizator_IdKor` FOREIGN KEY (`IdKor`) REFERENCES `organizator` (`IdKor`),
  CONSTRAINT `akcija_chk_1` CHECK ((`MaxBrVolontera` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `akcija`
--

LOCK TABLES `akcija` WRITE;
/*!40000 ALTER TABLE `akcija` DISABLE KEYS */;
INSERT INTO `akcija` VALUES (15,'Čišćenje Ade Ciganlije','Velika prolećna akcija čišćenja obala i staza Ade Ciganlije. Ponesite rukavice i vodu, kese obezbeđujemo mi.','2026-08-01','09:00:00.000000','Ada Ciganlija, Beograd',40,'kontakt@zelenibeograd.rs','011 2345678','aktivna','2026-07-11','akcije/cistenje_ade.jpg',28,10,44.7866,20.403),(16,'Sadnja drveća u Košutnjaku','Pošumljavanje šireg područja Košutnjaka. Sadnice i alat obezbeđeni. Akcija pogodna za sve uzraste.','2026-08-08','10:00:00.000000','Košutnjak, Beograd',60,'akcije@zelenibeograd.rs','011 2345678','aktivna','2026-07-11','akcije/sadnja_kosutnjak.jpg',28,10,44.775,20.4272),(17,'Prolećna akcija davanja krvi','Dobrovoljno davanje krvi u organizaciji Crvenog krsta. Svaka doza spašava život. Osveženje obezbeđeno.','2026-07-25','08:30:00.000000','Trg Nikole Pašića, Beograd',50,'krv@crvenikrst.rs','011 3456789','aktivna','2026-07-11','akcije/davanje_krvi.jpg',29,12,44.8125,20.4656),(18,'Pomoć starijim sugrađanima u Zemunu','Poseta i pomoć u kućnim poslovima i nabavci za starije sugrađane sa područja Zemuna.','2026-07-21','11:00:00.000000','Zemun, Beograd',3,'pomoc@crvenikrst.rs','011 3456789','popunjena','2026-07-11','akcije/pomoc_starima.jpg',29,11,44.8433,20.4011),(19,'Uređenje Dunavskog keja','Čišćenje i uređenje Dunavskog keja u Novom Sadu. Akcija je uspešno realizovana uz veliki odziv volontera.','2026-06-16','09:00:00.000000','Dunavski kej, Novi Sad',30,'info@vcns.rs','021 456789','zavrsena','2026-07-11','akcije/uredjenje_keja.jpg',30,10,45.253,19.851),(20,'Prikupljanje hrane za azil','Prikupljanje hrane, ćebadi i higijenskih potrepština za pse i mačke iz gradskog azila.','2026-07-29','12:00:00.000000','Futoški put, Novi Sad',25,'azil@vcns.rs','021 456789','aktivna','2026-07-11','akcije/azil_hrana.jpg',30,13,45.244,19.829),(21,'Ekološka radionica za decu','Edukativna radionica o reciklaži za decu osnovnoškolskog uzrasta. Akcija je otkazana zbog vremenskih uslova.','2026-07-18','11:00:00.000000','Kalemegdan, Beograd',20,'radionice@zelenibeograd.rs','011 2345678','otkazana','2026-07-11','akcije/radionica_deca.jpg',28,14,44.8225,20.451),(22,'Humanitarna trka kroz Beograd','Humanitarna trka čiji prihod ide deci bez roditeljskog staranja. Akcija čeka odobrenje administratora.','2026-08-25','10:00:00.000000','Ušće, Beograd',200,'trka@crvenikrst.rs','011 3456789','na_cekanju','2026-07-11','akcije/humanitarna_trka.jpg',29,11,44.819,20.438);
/*!40000 ALTER TABLE `akcija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Korisnik',12,'add_korisnik'),(22,'Can change Korisnik',12,'change_korisnik'),(23,'Can delete Korisnik',12,'delete_korisnik'),(24,'Can view Korisnik',12,'view_korisnik'),(25,'Can add Administrator profil',6,'add_administratorprofil'),(26,'Can change Administrator profil',6,'change_administratorprofil'),(27,'Can delete Administrator profil',6,'delete_administratorprofil'),(28,'Can view Administrator profil',6,'view_administratorprofil'),(29,'Can add Organizator profil',13,'add_organizatorprofil'),(30,'Can change Organizator profil',13,'change_organizatorprofil'),(31,'Can delete Organizator profil',13,'delete_organizatorprofil'),(32,'Can view Organizator profil',13,'view_organizatorprofil'),(33,'Can add Sponzor profil',16,'add_sponzorprofil'),(34,'Can change Sponzor profil',16,'change_sponzorprofil'),(35,'Can delete Sponzor profil',16,'delete_sponzorprofil'),(36,'Can view Sponzor profil',16,'view_sponzorprofil'),(37,'Can add Volonter profil',18,'add_volonterprofil'),(38,'Can change Volonter profil',18,'change_volonterprofil'),(39,'Can delete Volonter profil',18,'delete_volonterprofil'),(40,'Can view Volonter profil',18,'view_volonterprofil'),(41,'Can add Kategorija akcije',9,'add_kategorijaakcije'),(42,'Can change Kategorija akcije',9,'change_kategorijaakcije'),(43,'Can delete Kategorija akcije',9,'delete_kategorijaakcije'),(44,'Can view Kategorija akcije',9,'view_kategorijaakcije'),(45,'Can add Akcija',7,'add_akcija'),(46,'Can change Akcija',7,'change_akcija'),(47,'Can delete Akcija',7,'delete_akcija'),(48,'Can view Akcija',7,'view_akcija'),(49,'Can add Prijava volontera',14,'add_prijava'),(50,'Can change Prijava volontera',14,'change_prijava'),(51,'Can delete Prijava volontera',14,'delete_prijava'),(52,'Can view Prijava volontera',14,'view_prijava'),(53,'Can add Kategorija članka',10,'add_kategorijaclanka'),(54,'Can change Kategorija članka',10,'change_kategorijaclanka'),(55,'Can delete Kategorija članka',10,'delete_kategorijaclanka'),(56,'Can view Kategorija članka',10,'view_kategorijaclanka'),(57,'Can add Članak',8,'add_clanak'),(58,'Can change Članak',8,'change_clanak'),(59,'Can delete Članak',8,'delete_clanak'),(60,'Can view Članak',8,'view_clanak'),(61,'Can add Slika članka',15,'add_slikaclanka'),(62,'Can change Slika članka',15,'change_slikaclanka'),(63,'Can delete Slika članka',15,'delete_slikaclanka'),(64,'Can view Slika članka',15,'view_slikaclanka'),(65,'Can add Sponzorska ponuda',17,'add_sponzorskaponuda'),(66,'Can change Sponzorska ponuda',17,'change_sponzorskaponuda'),(67,'Can delete Sponzorska ponuda',17,'delete_sponzorskaponuda'),(68,'Can view Sponzorska ponuda',17,'view_sponzorskaponuda'),(69,'Can add Komentar',11,'add_komentar'),(70,'Can change Komentar',11,'change_komentar'),(71,'Can delete Komentar',11,'delete_komentar'),(72,'Can view Komentar',11,'view_komentar'),(73,'Can add Fotografija akcije',19,'add_fotografijaakcije'),(74,'Can change Fotografija akcije',19,'change_fotografijaakcije'),(75,'Can delete Fotografija akcije',19,'delete_fotografijaakcije'),(76,'Can view Fotografija akcije',19,'view_fotografijaakcije');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clanak`
--

DROP TABLE IF EXISTS `clanak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clanak` (
  `IdCla` int NOT NULL AUTO_INCREMENT,
  `Naslov` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Tekst` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `DatumKreiranja` date NOT NULL,
  `Status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `glavna_slika` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `IdKor` bigint NOT NULL,
  `IdKat` int NOT NULL,
  PRIMARY KEY (`IdCla`),
  KEY `Clanak_IdKor_58d68c84_fk_Organizator_IdKor` (`IdKor`),
  KEY `Clanak_IdKat_47fc63d8_fk_KategorijaClanka_IdKat` (`IdKat`),
  CONSTRAINT `Clanak_IdKat_47fc63d8_fk_KategorijaClanka_IdKat` FOREIGN KEY (`IdKat`) REFERENCES `kategorijaclanka` (`IdKat`),
  CONSTRAINT `Clanak_IdKor_58d68c84_fk_Organizator_IdKor` FOREIGN KEY (`IdKor`) REFERENCES `organizator` (`IdKor`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clanak`
--

LOCK TABLES `clanak` WRITE;
/*!40000 ALTER TABLE `clanak` DISABLE KEYS */;
INSERT INTO `clanak` VALUES (1,'Uspešno očišćena Ada Ciganlija','Prošlog vikenda više od 30 volontera učestvovalo je u čišćenju Ade Ciganlije. Prikupljeno je preko 200 kesa otpada, a obale su vraćene u pristojno stanje. Zahvaljujemo svima na odzivu!','2026-07-11','objavljen','clanci/clanak_ada.jpg',28,1),(2,'Preko 200 sadnica posađeno u Košutnjaku','Akcija pošumljavanja Košutnjaka okupila je rekordan broj volontera. Posađeno je preko 200 sadnica hrasta i lipe, čime doprinosimo očuvanju zelenih površina grada.','2026-07-11','objavljen','clanci/clanak_kosutnjak.jpg',28,1),(3,'Najava: velika humanitarna trka kroz Beograd','Pozivamo sve građane da se priključe humanitarnoj trci čiji prihod ide deci bez roditeljskog staranja. Prijave su otvorene, a učešće je besplatno.','2026-07-11','objavljen','clanci/clanak_humanitarna.jpg',29,2),(4,'Rezultati akcije davanja krvi','Sumiramo rezultate prethodne akcije dobrovoljnog davanja krvi. Članak čeka odobrenje administratora.','2026-07-11','na_cekanju','',29,3),(5,'Foto reportaža: dan proveden na čišćenju Ade','Donosimo vam foto reportažu sa nedavne akcije čišćenja Ade Ciganlije. Od ranih jutarnjih sati volonteri su marljivo radili na uređenju obala, a atmosfera je bila više nego prijatna. Pogledajte kako je izgledao dan.','2026-07-11','objavljen','clanci/reportaza_glavna.jpg',28,1);
/*!40000 ALTER TABLE `clanak` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_Korisnik_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_Korisnik_id` FOREIGN KEY (`user_id`) REFERENCES `korisnik` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(6,'main','administratorprofil'),(7,'main','akcija'),(8,'main','clanak'),(19,'main','fotografijaakcije'),(9,'main','kategorijaakcije'),(10,'main','kategorijaclanka'),(11,'main','komentar'),(12,'main','korisnik'),(13,'main','organizatorprofil'),(14,'main','prijava'),(15,'main','slikaclanka'),(16,'main','sponzorprofil'),(17,'main','sponzorskaponuda'),(18,'main','volonterprofil'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-07-09 11:41:10.124086'),(2,'contenttypes','0002_remove_content_type_name','2026-07-09 11:41:10.227530'),(3,'auth','0001_initial','2026-07-09 11:41:10.509282'),(4,'auth','0002_alter_permission_name_max_length','2026-07-09 11:41:10.575805'),(5,'auth','0003_alter_user_email_max_length','2026-07-09 11:41:10.581234'),(6,'auth','0004_alter_user_username_opts','2026-07-09 11:41:10.587829'),(7,'auth','0005_alter_user_last_login_null','2026-07-09 11:41:10.592776'),(8,'auth','0006_require_contenttypes_0002','2026-07-09 11:41:10.595467'),(9,'auth','0007_alter_validators_add_error_messages','2026-07-09 11:41:10.600419'),(10,'auth','0008_alter_user_username_max_length','2026-07-09 11:41:10.605111'),(11,'auth','0009_alter_user_last_name_max_length','2026-07-09 11:41:10.613360'),(12,'auth','0010_alter_group_name_max_length','2026-07-09 11:41:10.628011'),(13,'auth','0011_update_proxy_permissions','2026-07-09 11:41:10.633506'),(14,'auth','0012_alter_user_first_name_max_length','2026-07-09 11:41:10.638408'),(15,'main','0001_initial','2026-07-09 11:41:11.555207'),(16,'admin','0001_initial','2026-07-09 11:41:11.716530'),(17,'admin','0002_logentry_remove_auto_add','2026-07-09 11:41:11.724448'),(18,'admin','0003_logentry_add_action_flag_choices','2026-07-09 11:41:11.731459'),(19,'main','0002_kategorijaakcije_akcija','2026-07-09 11:41:11.914948'),(20,'main','0003_alter_akcija_status_prijava','2026-07-09 11:41:12.092814'),(21,'main','0004_kategorijaclanka_clanak_slikaclanka','2026-07-09 11:41:12.352376'),(22,'main','0005_sponzorska_ponuda','2026-07-09 11:41:12.496142'),(23,'main','0006_komentar','2026-07-09 11:41:12.649086'),(24,'sessions','0001_initial','2026-07-09 11:41:12.684738'),(25,'main','0007_akcija_geo','2026-07-09 17:40:35.627525'),(26,'main','0008_fotografijaakcije','2026-07-09 17:40:35.720782');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('01d0wi7lhmep9xch9kotbrklemxvg2gg','.eJxVjEEOwiAQAP-yZ0NKy8LSo3ffQIBdpGrapLQn499Nkx70OjOZN4S4bzXsTdYwMYzg4fLLUsxPmQ_BjzjfF5WXeVunpI5Enbap28Lyup7t36DGVmGEgli0j1rIGRGXSIg7r4sj7ovtS8neYjd4RrKoB5PYCbMMhAYTGYbPF_EyOAs:1whrMo:z9KXUUNLeqvJ_1igmkD0bXcBx6vK8Re5RDOocExjehk','2026-07-23 16:12:50.438496'),('1w11bfz1woyi3gmdr0mxtwie6rcuskiy','.eJxVjLsOwjAMAP_FM4qahKR2R3a-obJjQwqolfqYEP-OKnWA9e50b-h5W2u_LTb3g0IHAeH0C4XL08bd6IPH--TKNK7zIG5P3GEXd53UXpej_RtUXip0IM3NmIiJmmCZMcboC2kSia1aFo3eAp4pIKeMWX3OHAWRE5XGtwSfLxFMN78:1wiYSd:jDcX38OyIToxNdxSufJDEz69noVsOm0Iz3IBL62sghQ','2026-07-25 14:13:43.703668'),('aap6t2cncddsmm7cdo7r333dtw9nq8st','.eJxVjEEOwiAQAP-yZ0OAhWJ79N43kGWX2qqBpLQn499Nkx70OjOZN0TatznuLa9xERjAIFx-YSJ-5nIYeVC5V8W1bOuS1JGo0zY1Vsmv29n-DWZqMwwwWbyyFmcSekvCCY22TgfPoUfqvOQuiw0kLDhZ7x2aXvqJOxfYWWT4fAECaTf2:1whsl5:aqZtqs968vVfapi313o2mYTQAEoNwxrAN-f9uWH8Amo','2026-07-23 17:41:59.391322'),('gqv8uaeo5ld3npf0llwsb2pjcpkqhkbm','.eJxVjMsOwiAQAP9lz4awWyilR-9-A-GxSNVAUtqT8d9Nkx70OjOZNzi_b8XtnVe3JJiBEC6_MPj45HqY9PD13kRsdVuXII5EnLaLW0v8up7t36D4XmAGlqSCRcp2MsSGUYdRkfTDMOKgE-lsM1pD2RCSkRwV6YmSVTJrxajg8wXVjDaG:1wiCEb:ggzPW5cmh8o4T8zl1y9jmayMx5AZQRehYP2FAt4wzLo','2026-07-24 14:29:45.083025'),('i7tfof5dv4w7ml5gn8pdbby6lszlu336','.eJxVjDsOwyAQBe9CHSEM7AIp0_sMaPkFJxGWjF1FuXuE5CJp38y8N_N07NUfPW9-SezKJscuv2Og-MxtkPSgdl95XNu-LYEPhZ-083lN-XU73b-DSr2OWmcICMYaiVboEm3JsihHgoJIpAEFmOScNpPCGKwCBRA1oi4yF-XY5wv6_zdm:1whuXp:5jUgtzI343TugWyPbcsbhvjlqZuXnZqeFlV1bEqDVuo','2026-07-23 19:36:25.011737'),('lagcfas5demjfs7myry7he5b5p6rlevg','.eJxVjLsOwjAMAP_FM4qahKR2R3a-obJjQwqolfqYEP-OKnWA9e50b-h5W2u_LTb3g0IHAeH0C4XL08bd6IPH--TKNK7zIG5P3GEXd53UXpej_RtUXip0IM3NmIiJmmCZMcboC2kSia1aFo3eAp4pIKeMWX3OHAWRE5XGtwSfLxFMN78:1wiYP6:-RzrroUsyRUOP0opMI1aOVH2rLQITFmNiJ1j0JKN-2A','2026-07-25 14:10:04.139535'),('lvv6gjl555t9duwcdhgj5zco3yzij15w','.eJxVjMsOwiAQAP9lz4YA5dUevfsNBJZdqRqalPZk_HfTpAe9zkzmDTHtW417pzXOBSZQDi6_MCd8UjtMeaR2XwQubVvnLI5EnLaL21LodT3bv0FNvcIEI7KRFiUZR8is0Qepi3aW2SMqlpoGVB6dJztoVOxQKvIlh5LlaAJ8viHDOJg:1whsmE:Jljzt79FW043jRzxxBha_YfY-J_5qCGWIOtVr-BBsqg','2026-07-23 17:43:10.796557'),('p63z825dwm1ssibvigtgiv5o4t5fjus9','.eJxVjMsOwiAQAP9lz4bwBnv07jcQ2F2laiAp7cn476ZJD3qdmcwbUt7WmrbBS5oJJnBw-mUl45PbLuiR270L7G1d5iL2RBx2iGsnfl2O9m9Q86gwgUWKHnU0xhkO8ibZIEr0nqzErCga7UIIuihWzKw4ZpZRR1WonIP18PkC4FM3zw:1whrM4:jbv7DfGfKZ3STlEuRBvbJ5np2X2sLPIDMFKHegf0mko','2026-07-23 16:12:04.729318');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fotografijaakcije`
--

DROP TABLE IF EXISTS `fotografijaakcije`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fotografijaakcije` (
  `IdFot` int NOT NULL AUTO_INCREMENT,
  `Putanja` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Tip` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `IdAkc` int NOT NULL,
  PRIMARY KEY (`IdFot`),
  KEY `FotografijaAkcije_IdAkc_44467e50_fk_Akcija_IdAkc` (`IdAkc`),
  CONSTRAINT `FotografijaAkcije_IdAkc_44467e50_fk_Akcija_IdAkc` FOREIGN KEY (`IdAkc`) REFERENCES `akcija` (`IdAkc`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fotografijaakcije`
--

LOCK TABLES `fotografijaakcije` WRITE;
/*!40000 ALTER TABLE `fotografijaakcije` DISABLE KEYS */;
INSERT INTO `fotografijaakcije` VALUES (2,'akcije/keja_pre.jpg','pre',19),(3,'akcije/keja_posle.jpg','posle',19);
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
  `Naziv` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`IdKat`),
  UNIQUE KEY `Naziv` (`Naziv`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kategorijaakcije`
--

LOCK TABLES `kategorijaakcije` WRITE;
/*!40000 ALTER TABLE `kategorijaakcije` DISABLE KEYS */;
INSERT INTO `kategorijaakcije` VALUES (10,'Ekologija'),(11,'Humanitarni rad'),(14,'Obrazovanje'),(15,'Ostalo'),(13,'Zaštita životinja'),(12,'Zdravstvo');
/*!40000 ALTER TABLE `kategorijaakcije` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kategorijaclanka`
--

DROP TABLE IF EXISTS `kategorijaclanka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kategorijaclanka` (
  `IdKat` int NOT NULL AUTO_INCREMENT,
  `Naziv` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`IdKat`),
  UNIQUE KEY `Naziv` (`Naziv`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kategorijaclanka`
--

LOCK TABLES `kategorijaclanka` WRITE;
/*!40000 ALTER TABLE `kategorijaclanka` DISABLE KEYS */;
INSERT INTO `kategorijaclanka` VALUES (1,'Izveštaji'),(2,'Najave'),(4,'Ostalo'),(3,'Vesti');
/*!40000 ALTER TABLE `kategorijaclanka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `komentar`
--

DROP TABLE IF EXISTS `komentar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `komentar` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Tekst` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `DatumKomentara` datetime(6) NOT NULL,
  `IdCla` int NOT NULL,
  `IdKor` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Komentar_IdCla_b012d34f_fk_Clanak_IdCla` (`IdCla`),
  KEY `Komentar_IdKor_ba9660a4_fk_Korisnik_id` (`IdKor`),
  CONSTRAINT `Komentar_IdCla_b012d34f_fk_Clanak_IdCla` FOREIGN KEY (`IdCla`) REFERENCES `clanak` (`IdCla`),
  CONSTRAINT `Komentar_IdKor_ba9660a4_fk_Korisnik_id` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `komentar`
--

LOCK TABLES `komentar` WRITE;
/*!40000 ALTER TABLE `komentar` DISABLE KEYS */;
INSERT INTO `komentar` VALUES (1,'Bila sam tamo, sjajna akcija! Vidimo se na sledećoj.','2026-07-11 10:40:31.905260',1,22),(2,'Svaka čast organizatorima i svim volonterima.','2026-07-11 10:40:31.909594',1,23),(3,'Predivno, grad nam je lepši zahvaljujući ovome.','2026-07-11 10:40:31.913948',2,25),(4,'Prijavljujem se! Za divan cilj.','2026-07-11 10:40:31.918065',3,24);
/*!40000 ALTER TABLE `komentar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik`
--

DROP TABLE IF EXISTS `korisnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `KorisnickoIme` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Ime` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Prezime` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DatumRegistracije` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `KorisnickoIme` (`KorisnickoIme`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik`
--

LOCK TABLES `korisnik` WRITE;
/*!40000 ALTER TABLE `korisnik` DISABLE KEYS */;
INSERT INTO `korisnik` VALUES (1,'pbkdf2_sha256$1200000$NFLWNmHPsLk65HenxSx7K7$F5DyEuGI2zGYh6JNrkhlXSLmYyTK6Sb8g3fQooK3ik0=','2026-07-11 09:11:27.787644',1,'admin@akcijars.rs','admin_test','Admin','Testović','2026-07-09',1,1),(22,'pbkdf2_sha256$1200000$Ast7edwO9bwx6j28VJrYyv$1K1taHtAZKeTLPy2WQdORNAEe895mFrFK6R9S44riOM=','2026-07-11 11:18:55.976544',0,'jovana.petrovic93@gmail.com','jovana_p','Jovana','Petrović','2026-07-11',1,0),(23,'pbkdf2_sha256$1200000$UiEXtpQuTAlwvBs1SXauYl$usKpc4ojqiM3C4Ui+FZ65JwWjEYse1NYwnestTxINPI=','2026-07-11 11:12:52.876674',0,'marko.nikolic@gmail.com','marko_n','Marko','Nikolić','2026-07-11',1,0),(24,'pbkdf2_sha256$1200000$Fro7hW2Ubb9GdM9HlTcams$L/iD0BbREIKDuipbOf8Hu4hgtggMpEoGFeCrNWp2878=',NULL,0,'ana.jovanovic@yahoo.com','ana_j','Ana','Jovanović','2026-07-11',1,0),(25,'pbkdf2_sha256$1200000$4CDZHwv5ptodFWbKeLOSmE$RkAxLagMOJC+dIietORMRn2bsnYSrglWyQX9FLq+BJY=',NULL,0,'stefan.ilic@outlook.com','stefan_i','Stefan','Ilić','2026-07-11',1,0),(26,'pbkdf2_sha256$1200000$0DLKDhJQUaslTLoCq2ZtzK$Gl85KlDY6Fmauq5BOQKLwsdLfPpTEzvk3psTin6Nz9I=',NULL,0,'milica.djordjevic7@gmail.com','milica_dj','Milica','Đorđević','2026-07-11',1,0),(27,'pbkdf2_sha256$1200000$37FGvJonhG0WgMq9PVZKtb$UGI2err5Y1sX3xPNksXcROUfeL/qVUeBwtDcvVn8x7Y=',NULL,0,'nikola.markovic@gmail.com','nikola_m','Nikola','Marković','2026-07-11',1,0),(28,'pbkdf2_sha256$1200000$C2bqlDShDde9Veskwm4UTZ$Yn7jM5zZTVTGLjL+C8ymT7ZMQgo0vr6Y6+8xdoLMrrU=','2026-07-11 14:13:43.700629',0,'office.zelenibeograd@gmail.com','zeleni_bg','Nemanja','Radić','2026-07-11',1,0),(29,'pbkdf2_sha256$1200000$xq9DCqpLlm8XpWzuFrMih0$+l/FcEo5kmZ4e96wY56gs1/RW4s/g+vGeBWTK5FXd1g=',NULL,0,'crvenikrst.bg@gmail.com','crveni_krst','Ivana','Simić','2026-07-11',1,0),(30,'pbkdf2_sha256$1200000$cFifmj6KBzTTx07ZVy5ZE2$mFPBTFPf869vIFXjDDUzSJnnpQMVTODHKuB1GXfvicA=',NULL,0,'vcns.info@gmail.com','vcns','Đorđe','Popović','2026-07-11',1,0),(31,'pbkdf2_sha256$1200000$0NkguFK2OuoH8GGfZ9UJWP$nR2zfsHyK3RbjGr4P1TOmFeDJn5v606QUvxK7QoWg7w=',NULL,0,'ruka.prijateljstva@gmail.com','ruka_prij','Sara','Lukić','2026-07-11',1,0),(32,'pbkdf2_sha256$1200000$N1G6EJa0lnd47bq42zar2N$nnh2Iasn+Y5NrVNZNJKVVCPwUbWfoN3acejswugoJog=',NULL,0,'sponzorstva.delta@gmail.com','delta_h','Vladimir','Jović','2026-07-11',1,0),(33,'pbkdf2_sha256$1200000$Enq2t0cDPzXhgPxnCHkG9w$GJTT7K5TBBj1GcmRkaM4WWt6flRd8Omu82qy8pr7iiU=',NULL,0,'bojan.stojanovic.nis@gmail.com','nis_ad','Bojan','Stojanović','2026-07-11',1,0);
/*!40000 ALTER TABLE `korisnik` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik_groups`
--

DROP TABLE IF EXISTS `korisnik_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `korisnik_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Korisnik_groups_korisnik_id_group_id_db032ddd_uniq` (`korisnik_id`,`group_id`),
  KEY `Korisnik_groups_group_id_980cdc2e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `Korisnik_groups_group_id_980cdc2e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `Korisnik_groups_korisnik_id_a52b6905_fk_Korisnik_id` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnik` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik_groups`
--

LOCK TABLES `korisnik_groups` WRITE;
/*!40000 ALTER TABLE `korisnik_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `korisnik_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnik_user_permissions`
--

DROP TABLE IF EXISTS `korisnik_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnik_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `korisnik_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Korisnik_user_permission_korisnik_id_permission_i_6d3ef4bb_uniq` (`korisnik_id`,`permission_id`),
  KEY `Korisnik_user_permis_permission_id_c771180b_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Korisnik_user_permis_permission_id_c771180b_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `Korisnik_user_permissions_korisnik_id_1478424b_fk_Korisnik_id` FOREIGN KEY (`korisnik_id`) REFERENCES `korisnik` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnik_user_permissions`
--

LOCK TABLES `korisnik_user_permissions` WRITE;
/*!40000 ALTER TABLE `korisnik_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `korisnik_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizator`
--

DROP TABLE IF EXISTS `organizator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizator` (
  `IdKor` bigint NOT NULL,
  `BrTelefona` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `NazivOrganizacije` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`IdKor`),
  CONSTRAINT `Organizator_IdKor_86d3d33b_fk_Korisnik_id` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizator`
--

LOCK TABLES `organizator` WRITE;
/*!40000 ALTER TABLE `organizator` DISABLE KEYS */;
INSERT INTO `organizator` VALUES (28,'011 2345678','Zeleni Beograd','odobren'),(29,'011 3456789','Crveni krst Beograd','odobren'),(30,'021 456789','Volonterski centar Novi Sad','odobren'),(31,'011 5678901','Ruka prijateljstva','na_cekanju');
/*!40000 ALTER TABLE `organizator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prijavavolontera`
--

DROP TABLE IF EXISTS `prijavavolontera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prijavavolontera` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `DatumPrijave` date NOT NULL,
  `Status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `BrSati` int unsigned NOT NULL,
  `IdAkc` int NOT NULL,
  `IdKor` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `PrijavaVolontera_IdKor_IdAkc_517d51c6_uniq` (`IdKor`,`IdAkc`),
  KEY `PrijavaVolontera_IdAkc_b0cf53fd_fk_Akcija_IdAkc` (`IdAkc`),
  CONSTRAINT `PrijavaVolontera_IdAkc_b0cf53fd_fk_Akcija_IdAkc` FOREIGN KEY (`IdAkc`) REFERENCES `akcija` (`IdAkc`),
  CONSTRAINT `PrijavaVolontera_IdKor_e22f68ef_fk_Volonter_IdKor` FOREIGN KEY (`IdKor`) REFERENCES `volonter` (`IdKor`),
  CONSTRAINT `prijavavolontera_chk_1` CHECK ((`BrSati` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prijavavolontera`
--

LOCK TABLES `prijavavolontera` WRITE;
/*!40000 ALTER TABLE `prijavavolontera` DISABLE KEYS */;
INSERT INTO `prijavavolontera` VALUES (15,'2026-07-11','prihvacena',0,15,22),(16,'2026-07-11','prihvacena',0,15,23),(17,'2026-07-11','na_cekanju',0,15,24),(18,'2026-07-11','na_cekanju',0,15,25),(19,'2026-07-11','odbijena',0,15,27),(20,'2026-07-11','prihvacena',0,17,26),(21,'2026-07-11','na_cekanju',0,17,27),(22,'2026-07-11','prihvacena',0,18,22),(23,'2026-07-11','prihvacena',0,18,25),(24,'2026-07-11','prihvacena',0,18,24),(25,'2026-07-11','na_cekanju',0,20,27),(26,'2026-07-11','prihvacena',0,20,22),(27,'2026-07-11','prihvacena',6,19,23),(28,'2026-07-11','prihvacena',6,19,24),(29,'2026-07-11','prihvacena',5,19,26),(30,'2026-07-11','na_cekanju',0,16,22);
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
  `Putanja` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `IdCla` int NOT NULL,
  PRIMARY KEY (`IdSli`),
  KEY `SlikaClanka_IdCla_95a62d76_fk_Clanak_IdCla` (`IdCla`),
  CONSTRAINT `SlikaClanka_IdCla_95a62d76_fk_Clanak_IdCla` FOREIGN KEY (`IdCla`) REFERENCES `clanak` (`IdCla`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slikaclanka`
--

LOCK TABLES `slikaclanka` WRITE;
/*!40000 ALTER TABLE `slikaclanka` DISABLE KEYS */;
INSERT INTO `slikaclanka` VALUES (1,'clanci/clanak_kosutnjak.jpg',2),(2,'clanci/reportaza_1.jpg',5),(3,'clanci/reportaza_2.jpg',5),(4,'clanci/reportaza_3.jpg',5),(5,'clanci/reportaza_4.jpg',5);
/*!40000 ALTER TABLE `slikaclanka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponzor`
--

DROP TABLE IF EXISTS `sponzor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponzor` (
  `IdKor` bigint NOT NULL,
  `BrTelefona` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `NazivOrganizacije` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`IdKor`),
  CONSTRAINT `Sponzor_IdKor_d117df97_fk_Korisnik_id` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponzor`
--

LOCK TABLES `sponzor` WRITE;
/*!40000 ALTER TABLE `sponzor` DISABLE KEYS */;
INSERT INTO `sponzor` VALUES (32,'011 2010100','Delta Holding','odobren'),(33,'021 4810000','NIS a.d.','odobren');
/*!40000 ALTER TABLE `sponzor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponzorskaponuda`
--

DROP TABLE IF EXISTS `sponzorskaponuda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponzorskaponuda` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Vrednost` int unsigned NOT NULL,
  `Opis` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `Status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DatumSlanja` date NOT NULL,
  `IdAkc` int NOT NULL,
  `IdKor` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `SponzorskaPonuda_IdAkc_bccda336_fk_Akcija_IdAkc` (`IdAkc`),
  KEY `SponzorskaPonuda_IdKor_d43a3038_fk_Sponzor_IdKor` (`IdKor`),
  CONSTRAINT `SponzorskaPonuda_IdAkc_bccda336_fk_Akcija_IdAkc` FOREIGN KEY (`IdAkc`) REFERENCES `akcija` (`IdAkc`),
  CONSTRAINT `SponzorskaPonuda_IdKor_d43a3038_fk_Sponzor_IdKor` FOREIGN KEY (`IdKor`) REFERENCES `sponzor` (`IdKor`),
  CONSTRAINT `sponzorskaponuda_chk_1` CHECK ((`Vrednost` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponzorskaponuda`
--

LOCK TABLES `sponzorskaponuda` WRITE;
/*!40000 ALTER TABLE `sponzorskaponuda` DISABLE KEYS */;
INSERT INTO `sponzorskaponuda` VALUES (2,800,'Finansijska podrška i oprema za čišćenje (rukavice, kese, kontejneri).','prihvacena','2026-07-11',15,32),(3,300,'Donacija vode i osveženja za volontere.','na_cekanju','2026-07-11',15,33),(4,500,'Obezbeđivanje osveženja i promotivnog materijala.','prihvacena','2026-07-11',17,32),(5,400,'Donacija 100 sadnica i baštenskog alata.','na_cekanju','2026-07-11',16,33),(6,600,'Oprema za čišćenje i prevoz otpada.','prihvacena','2026-07-11',19,33);
/*!40000 ALTER TABLE `sponzorskaponuda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volonter`
--

DROP TABLE IF EXISTS `volonter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `volonter` (
  `IdKor` bigint NOT NULL,
  `UkupnoSati` int unsigned NOT NULL,
  `PrimaPreporuke` tinyint(1) NOT NULL,
  PRIMARY KEY (`IdKor`),
  CONSTRAINT `Volonter_IdKor_838b8df4_fk_Korisnik_id` FOREIGN KEY (`IdKor`) REFERENCES `korisnik` (`id`),
  CONSTRAINT `volonter_chk_1` CHECK ((`UkupnoSati` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volonter`
--

LOCK TABLES `volonter` WRITE;
/*!40000 ALTER TABLE `volonter` DISABLE KEYS */;
INSERT INTO `volonter` VALUES (22,0,1),(23,6,1),(24,6,0),(25,0,1),(26,5,0),(27,0,0);
/*!40000 ALTER TABLE `volonter` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-11 16:51:41
