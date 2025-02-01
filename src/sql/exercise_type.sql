-- my_wellness.exercise_type definition

CREATE TABLE `exercise_type` (
  `name` varchar(100) DEFAULT NULL,
  `uuid` varchar(64) NOT NULL,
  `row_created_at` datetime NOT NULL,
  `row_updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


