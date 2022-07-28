
CREATE DATABASE /*!32312 IF NOT EXISTS*/`info` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `info`;

/*Table structure for table `balance` */

DROP TABLE IF EXISTS `balance`;

CREATE TABLE `balance` (
  `id` bigint(20) NOT NULL auto_increment,
  `Account` text,
  `Currency` text,
  `Balance` double default NULL,
  `AsOfDateTS` text,
  PRIMARY KEY  (`id`),
  KEY `ix_balance_index` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3;

/*Table structure for table `bals` */

DROP TABLE IF EXISTS `bals`;

CREATE TABLE `bals` (
  `id` int(11) NOT NULL auto_increment,
  `account` varchar(32) default NULL,
  `Cd` varchar(32) default NULL,
  `Ccy` varchar(32) default NULL,
  `Amt` varchar(32) default NULL,
  `CdtDbtInd` varchar(32) default NULL,
  `Dt` varchar(32) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Table structure for table `ntrys` */

DROP TABLE IF EXISTS `ntrys`;

CREATE TABLE `ntrys` (
  `id` int(11) NOT NULL auto_increment,
  `account` varchar(32) default NULL,
  `NbOfTxs` varchar(32) default NULL,
  `Ccy` varchar(32) default NULL,
  `Amt` varchar(32) default NULL,
  `CdtDbtInd` varchar(32) default NULL,
  `Cd` varchar(32) default NULL,
  `DtTm` varchar(32) default NULL,
  `Dt` varchar(32) default NULL,
  `MsgId` varchar(32) default NULL,
  `PmtInfId` varchar(32) default NULL,
  `EndToEndId` varchar(32) default NULL,
  `UETR` varchar(32) default NULL,
  `TtlAmt` varchar(32) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Table structure for table `swift` */

DROP TABLE IF EXISTS `swift`;

CREATE TABLE `swift` (
  `id` int(11) NOT NULL auto_increment,
  `account` varchar(32) default NULL,
  `fr` varchar(32) default NULL,
  `isto` varchar(32) default NULL,
  `msgid` varchar(32) default NULL,
  `CreDtTm` varchar(32) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Table structure for table `transactions` */

DROP TABLE IF EXISTS `transactions`;

CREATE TABLE `transactions` (
  `id` bigint(20) NOT NULL auto_increment,
  `Account` text,
  `ValueDate` text,
  `Currency` text,
  `CreditDebit` text,
  `Amount` bigint(20) default NULL,
  `TransactionReference` text,
  PRIMARY KEY  (`id`),
  KEY `ix_transactions_index` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

