CREATE DATABASE AIGC_TASK;

CREATE TABLE `SD_TASK_EXCHAGE` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `requestid` varchar(128) NOT NULL,
  `image` varchar(1024) NOT NULL COMMENT '输入图像',
  `image2` varchar(1024) NOT NULL COMMENT '风格图像',
  `model_param` text COMMENT '全局参数，json格式',
  `cnt` int NOT NULL COMMENT '生成张数',
  `res_img` varchar(1024) DEFAULT NULL COMMENT '输出图像',
  `status` tinyint(1) DEFAULT '1' COMMENT '-1=失败，0=正在处理，1=排队中，2=生成成功',
  `create_time` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `update_time` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `delete_time` datetime(3) DEFAULT NULL,
  `extra1` varchar(1024) DEFAULT NULL,
  `extra2` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=737 DEFAULT CHARSET=utf8mb4 ;



ALTER TABLE SD_TASK_EXCHAGE ADD INDEX idx_requestid (requestid);
ALTER TABLE SD_TASK_EXCHAGE ADD INDEX idx_status (status);
