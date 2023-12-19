-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.2.1-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for pilot_simulator
CREATE DATABASE IF NOT EXISTS `pilot_simulator` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `pilot_simulator`;

-- Dumping structure for table pilot_simulator.airports
CREATE TABLE IF NOT EXISTS `airports` (
  `id` int(11) NOT NULL,
  `ident` varchar(50) DEFAULT NULL,
  `name` varchar(250) DEFAULT NULL,
  `latitude_deg` double DEFAULT NULL,
  `longitude_deg` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ident_UNIQUE` (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pilot_simulator.airports: ~117 rows (approximately)
INSERT INTO `airports` (`id`, `ident`, `name`, `latitude_deg`, `longitude_deg`) VALUES
	(123, 'BIKF', 'Keflavik International Airport', 63.985001, -22.6056),
	(2155, 'EBBR', 'Brussels Airport', 50.901401519800004, 4.48443984985),
	(2212, 'EDDF', 'Frankfurt am Main Airport', 50.036249, 8.559294),
	(2214, 'EDDH', 'Hamburg Helmut Schmidt Airport', 53.630402, 9.98823),
	(2216, 'EDDK', 'Cologne Bonn Airport', 50.8658981323, 7.1427397728),
	(2217, 'EDDL', 'D?sseldorf Airport', 51.289501, 6.76678),
	(2218, 'EDDM', 'Munich Airport', 48.353802, 11.7861),
	(2219, 'EDDN', 'Nuremberg Airport', 49.498699, 11.078056),
	(2220, 'EDDP', 'Leipzig/Halle Airport', 51.423889, 12.236389),
	(2222, 'EDDS', 'Stuttgart Airport', 48.689899444599995, 9.22196006775),
	(2224, 'EDDV', 'Hannover Airport', 52.461101532, 9.685079574580001),
	(2301, 'EETN', 'Lennart Meri Tallinn Airport', 59.41329956049999, 24.832799911499997),
	(2307, 'EFHK', 'Helsinki Vantaa Airport', 60.3172, 24.963301),
	(2385, 'EGAA', 'Belfast International Airport', 54.6575012207, -6.2158298492399995),
	(2389, 'EGBB', 'Birmingham International Airport', 52.453899383499994, -1.74802994728),
	(2398, 'EGCC', 'Manchester Airport', 53.349375, -2.279521),
	(2419, 'EGGW', 'London Luton Airport', 51.874698638916016, -0.36833301186561584),
	(2429, 'EGKK', 'London Gatwick Airport', 51.148102, -0.190278),
	(2434, 'EGLL', 'London Heathrow Airport', 51.4706, -0.461941),
	(2461, 'EGPF', 'Glasgow International Airport', 55.871899, -4.43306),
	(2462, 'EGPH', 'Edinburgh Airport', 55.950145, -3.372288),
	(2476, 'EGSS', 'London Stansted Airport', 51.8849983215, 0.234999999404),
	(2513, 'EHAM', 'Amsterdam Airport Schiphol', 52.308601, 4.76389),
	(2518, 'EHEH', 'Eindhoven Airport', 51.4500999451, 5.37452983856),
	(2533, 'EIDW', 'Dublin Airport', 53.421299, -6.27007),
	(2537, 'EINN', 'Shannon Airport', 52.702, -8.92482),
	(2541, 'EKBI', 'Billund Airport', 55.7402992249, 9.15178012848),
	(2542, 'EKCH', 'Copenhagen Kastrup Airport', 55.617900848389, 12.656000137329),
	(2563, 'ELLX', 'Luxembourg-Findel International Airport', 49.6233333, 6.2044444),
	(2570, 'ENBR', 'Bergen Airport, Flesland', 60.2934, 5.21814),
	(2578, 'ENGM', 'Oslo Airport, Gardermoen', 60.193901, 11.1004),
	(2599, 'ENTC', 'Troms? Airport, Langnes', 69.683296, 18.9189),
	(2601, 'ENVA', 'Trondheim Airport, V?rnes', 63.457802, 10.924),
	(2602, 'ENZV', 'Stavanger Airport, Sola', 58.876701, 5.63778),
	(2608, 'EPGD', 'Gda?sk Lech Wa??sa Airport', 54.377601623535156, 18.46619987487793),
	(2609, 'EPKK', 'Krak?w John Paul II International Airpor', 50.077702, 19.7848),
	(2637, 'EPWA', 'Warsaw Chopin Airport', 52.1656990051, 20.967100143399996),
	(2648, 'ESGG', 'Gothenburg-Landvetter Airport', 57.662799835205, 12.279800415039),
	(2701, 'ESSA', 'Stockholm-Arlanda Airport', 59.651901245117, 17.918600082397),
	(2758, 'EVRA', 'Riga International Airport', 56.92359924316406, 23.971099853515625),
	(2766, 'EYVI', 'Vilnius International Airport', 54.634102, 25.285801),
	(3077, 'GCFV', 'Fuerteventura Airport', 28.4527, -13.8638),
	(3081, 'GCLP', 'Gran Canaria Airport', 27.9319, -15.3866),
	(3082, 'GCRR', 'C?sar Manrique-Lanzarote Airport', 28.945499, -13.6052),
	(3083, 'GCTS', 'Tenerife Sur Airport', 28.0445, -16.5725),
	(3972, 'LATI', 'Tirana International Airport Mother Tere', 41.4146995544, 19.7206001282),
	(3974, 'LBBG', 'Burgas Airport', 42.56959915161133, 27.515199661254883),
	(3977, 'LBSF', 'Sofia Airport', 42.696693420410156, 23.411436080932617),
	(3979, 'LBWN', 'Varna Airport', 43.232101, 27.8251),
	(3993, 'LDZA', 'Zagreb Airport', 45.7429008484, 16.0687999725),
	(3997, 'LEAL', 'Alicante-Elche Miguel Hern?ndez Airport', 38.2822, -0.558156),
	(4004, 'LEBL', 'Josep Tarradellas Barcelona-El Prat Airp', 41.2971, 2.07846),
	(4013, 'LEIB', 'Ibiza Airport', 38.872898, 1.37312),
	(4019, 'LEMD', 'Adolfo Su?rez Madrid?Barajas Airport', 40.471926, -3.56264),
	(4020, 'LEMG', 'M?laga-Costa del Sol Airport', 36.6749, -4.49911),
	(4035, 'LEPA', 'Palma de Mallorca Airport', 39.551701, 2.73881),
	(4038, 'LEST', 'Santiago-Rosal?a de Castro Airport', 42.896301, -8.41514),
	(4060, 'LFBD', 'Bordeaux-M?rignac Airport', 44.8283, -0.715556),
	(4070, 'LFBO', 'Toulouse-Blagnac Airport', 43.629101, 1.36382),
	(4137, 'LFLL', 'Lyon Saint-Exup?ry Airport', 45.725556, 5.081111),
	(4155, 'LFML', 'Marseille Provence Airport', 43.439271922, 5.22142410278),
	(4156, 'LFMN', 'Nice-C?te d\'Azur Airport', 43.6584014893, 7.215869903560001),
	(4185, 'LFPG', 'Charles de Gaulle International Airport', 49.012798, 2.55),
	(4189, 'LFPO', 'Paris-Orly Airport', 48.7233333, 2.3794444),
	(4226, 'LFSB', 'EuroAirport Basel-Mulhouse-Freiburg Airp', 47.59, 7.529167),
	(4251, 'LGAV', 'Athens Eleftherios Venizelos Internation', 37.936401, 23.9445),
	(4258, 'LGIR', 'Heraklion International Nikos Kazantzaki', 35.3396987915, 25.180299758900002),
	(4293, 'LGTS', 'Thessaloniki Macedonia International Air', 40.51969909667969, 22.97089958190918),
	(4296, 'LHBP', 'Budapest Liszt Ferenc International Airp', 47.42976, 19.261093),
	(4318, 'LICC', 'Catania-Fontanarossa Airport', 37.466801, 15.0664),
	(4321, 'LICJ', 'Falcone?Borsellino Airport', 38.175999, 13.091),
	(4332, 'LIEE', 'Cagliari Elmas Airport', 39.251499, 9.05428),
	(4340, 'LIMC', 'Malpensa International Airport', 45.6306, 8.72811),
	(4341, 'LIME', 'Milan Bergamo Airport', 45.673901, 9.70417),
	(4342, 'LIMF', 'Turin Airport', 45.200802, 7.64963),
	(4354, 'LIPE', 'Bologna Guglielmo Marconi Airport', 44.5354, 11.2887),
	(4366, 'LIPX', 'Verona Villafranca Airport', 45.395699, 10.8885),
	(4368, 'LIPZ', 'Venice Marco Polo Airport', 45.505299, 12.3519),
	(4372, 'LIRF', 'Rome?Fiumicino Leonardo da Vinci Interna', 41.804532, 12.251998),
	(4378, 'LIRN', 'Naples International Airport', 40.886002, 14.2908),
	(4379, 'LIRP', 'Pisa International Airport', 43.683899, 10.3927),
	(4386, 'LJLJ', 'Ljubljana Jo?e Pu?nik Airport', 46.223701, 14.4576),
	(4408, 'LKPR', 'V?clav Havel Airport Prague', 50.1008, 14.26),
	(4427, 'LMML', 'Malta International Airport', 35.857498, 14.4775),
	(4434, 'LOWW', 'Vienna International Airport', 48.110298, 16.5697),
	(4448, 'LPFR', 'Faro Airport', 37.0144004822, -7.96590995789),
	(4456, 'LPPD', 'Jo?o Paulo II Airport', 37.7411994934, -25.6979007721),
	(4459, 'LPPR', 'Francisco de S? Carneiro Airport', 41.2481002808, -8.68138980865),
	(4461, 'LPPT', 'Humberto Delgado Airport (Lisbon Portela', 38.7813, -9.13592),
	(4482, 'LROP', 'Henri Coand? International Airport', 44.5711111, 26.085),
	(4490, 'LSGG', 'Geneva Cointrin International Airport', 46.23809814453125, 6.108950138092041),
	(4505, 'LSZH', 'Z?rich Airport', 47.458056, 8.548056),
	(4573, 'LWSK', 'Skopje International Airport', 41.961601, 21.621401),
	(4610, 'LYBE', 'Belgrade Nikola Tesla Airport', 44.8184013367, 20.3090991974),
	(4613, 'LYPG', 'Podgorica Airport / Podgorica Golubovci ', 42.359402, 19.2519),
	(4617, 'LZIB', 'M. R. ?tef?nik Airport', 48.17020034790039, 17.21269989013672),
	(6462, 'UHWW', 'Vladivostok International Airport', 43.396256, 132.148155),
	(6467, 'UKBB', 'Boryspil International Airport', 50.345001220703125, 30.894699096679688),
	(6481, 'UKLL', 'Lviv International Airport', 49.8125, 23.9561),
	(6489, 'ULLI', 'Pulkovo Airport', 59.80030059814453, 30.262500762939453),
	(6501, 'UMMS', 'Minsk National Airport', 53.888071, 28.039964),
	(6506, 'UNKL', 'Krasnoyarsk International Airport', 56.173077, 92.492437),
	(6507, 'UNNT', 'Novosibirsk Tolmachevo Airport', 55.019756, 82.618675),
	(6519, 'URSS', 'Sochi International Airport', 43.449902, 39.9566),
	(26394, 'UUDD', 'Domodedovo International Airport', 55.40879821777344, 37.90629959106445),
	(26396, 'UUEE', 'Sheremetyevo International Airport', 55.972599, 37.4146),
	(26401, 'UUWW', 'Vnukovo International Airport', 55.5914993286, 37.2615013123),
	(26404, 'UWKD', 'Kazan International Airport', 55.606201171875, 49.278701782227),
	(26411, 'UWUU', 'Ufa International Airport', 54.557498931885, 55.874401092529),
	(26412, 'UWWW', 'Kurumoch International Airport', 53.504901885986, 50.16429901123),
	(35046, 'RU-4464', 'Olenya Air Base', 68.151802062988, 33.463901519775),
	(41136, 'RU-0016', 'Lipetsk Air Base', 52.6349983215332, 39.44499969482422),
	(42924, 'RU-0035', 'Grozny North Airport', 43.388302, 45.698601),
	(42967, 'UUBW', 'Zhukovsky International Airport', 55.553299, 38.150002),
	(301881, 'EDDB', 'Berlin Brandenburg Airport', 52.351389, 13.493889),
	(326363, 'URRP', 'Platov International Airport', 47.493888, 39.924722),
	(339001, 'UWSG', 'Gagarin International Airport', 51.712778, 46.171111);

-- Dumping structure for table pilot_simulator.euro_balance
CREATE TABLE IF NOT EXISTS `euro_balance` (
  `euro_transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(16,0) DEFAULT NULL,
  PRIMARY KEY (`euro_transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pilot_simulator.euro_balance: ~3 rows (approximately)

-- Dumping structure for table pilot_simulator.fuel_account
CREATE TABLE IF NOT EXISTS `fuel_account` (
  `fuel_transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `normal_fuel` int(11) DEFAULT NULL,
  `saf_fuel` int(11) DEFAULT NULL,
  PRIMARY KEY (`fuel_transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pilot_simulator.fuel_account: ~4 rows (approximately)

-- Dumping structure for table pilot_simulator.game_profile
CREATE TABLE IF NOT EXISTS `game_profile` (
  `profile_id` int(11) NOT NULL AUTO_INCREMENT,
  `profile_name` varchar(45) DEFAULT NULL,
  `username` varchar(45) NOT NULL,
  `aeroplane_model` varchar(45) DEFAULT NULL,
  `consumption_fullload` int(11) DEFAULT NULL,
  `consumption_base` int(11) DEFAULT NULL,
  PRIMARY KEY (`profile_id`),
  UNIQUE KEY `profile_name_UNIQUE` (`profile_name`),
  KEY `username_idx` (`username`),
  CONSTRAINT `username` FOREIGN KEY (`username`) REFERENCES `profiles` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pilot_simulator.game_profile: ~6 rows (approximately)

-- Dumping structure for table pilot_simulator.profiles
CREATE TABLE IF NOT EXISTS `profiles` (
  `username` varchar(45) NOT NULL,
  `full_name` varchar(45) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pilot_simulator.profiles: ~2 rows (approximately)

-- Dumping structure for table pilot_simulator.purchases
CREATE TABLE IF NOT EXISTS `purchases` (
  `purchase_id` int(11) NOT NULL AUTO_INCREMENT,
  `profile_id` int(11) NOT NULL,
  `euro_transaction_id` int(11) DEFAULT NULL,
  `fuel_transaction_id` int(11) DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`purchase_id`),
  KEY `euro_transaction_id_idx` (`euro_transaction_id`),
  KEY `profile_id_idx` (`profile_id`),
  KEY `profile_id_purchase_idx` (`profile_id`),
  KEY `fuel_transaction_id_purchase_idx` (`fuel_transaction_id`),
  KEY `euro_transaction_id_purchase_idx` (`euro_transaction_id`),
  CONSTRAINT `euro_transaction_id_purchase` FOREIGN KEY (`euro_transaction_id`) REFERENCES `euro_balance` (`euro_transaction_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fuel_transaction_id_purchase` FOREIGN KEY (`fuel_transaction_id`) REFERENCES `fuel_account` (`fuel_transaction_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `profile_id_purchase` FOREIGN KEY (`profile_id`) REFERENCES `game_profile` (`profile_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pilot_simulator.purchases: ~0 rows (approximately)

-- Dumping structure for table pilot_simulator.trips
CREATE TABLE IF NOT EXISTS `trips` (
  `trip_id` int(11) NOT NULL AUTO_INCREMENT,
  `profile_id` int(11) NOT NULL,
  `from_airport` int(11) NOT NULL,
  `to_airport` int(11) NOT NULL,
  `passenger` int(11) NOT NULL,
  `fuel_transaction_id` int(11) NOT NULL,
  `distance` int(11) NOT NULL,
  `euro_transaction_id` int(11) NOT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`trip_id`),
  KEY `euro_transaction_id_idx` (`euro_transaction_id`),
  KEY `profile_id_trip_idx` (`profile_id`),
  KEY `fuel_transaction_id_trip_idx` (`fuel_transaction_id`),
  KEY `from_idx` (`from_airport`) USING BTREE,
  KEY `to_idx` (`to_airport`) USING BTREE,
  CONSTRAINT `euro_transaction_id` FOREIGN KEY (`euro_transaction_id`) REFERENCES `euro_balance` (`euro_transaction_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `from_airport_trip` FOREIGN KEY (`from_airport`) REFERENCES `airports` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fuel_transaction_id_trip` FOREIGN KEY (`fuel_transaction_id`) REFERENCES `fuel_account` (`fuel_transaction_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `profile_id_trip` FOREIGN KEY (`profile_id`) REFERENCES `game_profile` (`profile_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `to_airport_trip` FOREIGN KEY (`to_airport`) REFERENCES `airports` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pilot_simulator.trips: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
