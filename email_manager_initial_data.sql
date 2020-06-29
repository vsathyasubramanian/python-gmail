create database email_manager;
use email_manager;
CREATE TABLE `email_snapshot` (
  `email_snapshot_id` int NOT NULL AUTO_INCREMENT,
  `msg_id` varchar(50) NOT NULL,
  `labels` varchar(100) DEFAULT NULL,
  `from_address` varchar(100) NOT NULL,
  `to_address` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `subject` text,
  `content` text,
  UNIQUE KEY `pri_key` (`email_snapshot_id`) USING BTREE,
  KEY `msg_id_idx` (`msg_id`) USING BTREE,
  KEY `from_addr_idx` (`from_address`) USING BTREE,
  KEY `to_addr_idx` (`to_address`) USING BTREE,
  KEY `date_idx` (`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci