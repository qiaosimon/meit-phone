CREATE SCHEMA `phone` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;

CREATE TABLE `city` (
                        `CITYID` int NOT NULL COMMENT '城市的编号',
                        `CITYNAME` varchar(45) DEFAULT NULL COMMENT '城市名称',
                        `ABBR` varchar(45) DEFAULT NULL COMMENT '城市简称，例如北京，简称是bj',
                        `STATE` int DEFAULT '0' COMMENT '状态 0-不收集 1-收集',
                        PRIMARY KEY (`CITYID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='城市'

CREATE TABLE `cate` (
                        `CATEID` int NOT NULL COMMENT '分类编号',
                        `NAME` varchar(45) DEFAULT NULL COMMENT '分类名称',
                        `COUNT` int DEFAULT NULL COMMENT '该分类保存的数据条数',
                        PRIMARY KEY (`CATEID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分类'

CREATE TABLE `account` (
                           `USERID` int NOT NULL COMMENT '用户ID，需要登录系统查看',
                           `COOKEIE` varchar(1024) DEFAULT NULL COMMENT '浏览器cookie',
                           PRIMARY KEY (`USERID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='网站的账号'

CREATE TABLE `shop` (
                        `ID` int NOT NULL COMMENT '商家编号',
                        `SHOPNAME` varchar(512) DEFAULT NULL COMMENT '商家名称',
                        `ADDRESS` varchar(512) DEFAULT NULL COMMENT '商家地址',
                        `PHONE` varchar(45) DEFAULT NULL COMMENT '手机号码',
                        `CITYID` int NOT NULL COMMENT '城市编号',
                        `CATEID` int DEFAULT NULL COMMENT '分类编号',
                        `AVGSCORE` varchar(45) DEFAULT NULL COMMENT '综合评分',
                        `COMMENTS` int DEFAULT NULL COMMENT '评论数',
                        `HISTORYCOUPONCOUNT` int DEFAULT NULL COMMENT '历史成交单数',
                        `STATE` int DEFAULT '0' COMMENT '0-初始状态 1-有用 2-无用',
                        PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='商家信息'