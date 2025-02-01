-- my_wellness.session_exercise definition

CREATE TABLE `session_exercise` (
  `machine_type_uuid` varchar(100) DEFAULT NULL,
  `activity_uuid` varchar(64) DEFAULT NULL,
  `session_date` datetime DEFAULT NULL,
  `fc_max` int DEFAULT NULL,
  `fc_avg` int DEFAULT NULL,
  `duration_minutes` float DEFAULT NULL,
  `power_avg` int DEFAULT NULL,
  `moves` int DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `uuid` varchar(64) NOT NULL,
  `row_created_at` datetime NOT NULL,
  `row_updated_at` datetime DEFAULT NULL,
  `calories` int DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `activity_uuid` (`activity_uuid`),
  KEY `machine_type_uuid` (`machine_type_uuid`),
  CONSTRAINT `session_exercise_ibfk_1` FOREIGN KEY (`machine_type_uuid`) REFERENCES `machine_type` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;