-- my_wellness.machine_type definition

CREATE TABLE `machine_type` (
  `exercise_type_uuid` varchar(64) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `machine_data_uuid` varchar(64) DEFAULT NULL,
  `uuid` varchar(64) NOT NULL,
  `row_created_at` datetime NOT NULL,
  `row_updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `name` (`name`),
  KEY `exercise_type_uuid` (`exercise_type_uuid`),
  KEY `machine_data_uuid` (`machine_data_uuid`),
  CONSTRAINT `machine_type_ibfk_1` FOREIGN KEY (`exercise_type_uuid`) REFERENCES `exercise_type` (`uuid`),
  CONSTRAINT `machine_type_ibfk_2` FOREIGN KEY (`machine_data_uuid`) REFERENCES `machine_data` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;