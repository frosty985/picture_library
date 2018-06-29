-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 28, 2018 at 09:35 PM
-- Server version: 5.7.22-0ubuntu0.16.04.1
-- PHP Version: 7.0.30-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `picture_library`
--
CREATE DATABASE IF NOT EXISTS `picture_library` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `picture_library`;

-- --------------------------------------------------------

--
-- Table structure for table `contains`
--
-- Creation: Jun 24, 2018 at 08:09 PM
-- Last update: Jun 28, 2018 at 08:09 PM
--

DROP TABLE IF EXISTS `contains`;
CREATE TABLE `contains` (
  `id` char(32) NOT NULL,
  `contains` varchar(75) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- RELATIONS FOR TABLE `contains`:
--

--
-- Dumping data for table `contains`
--

INSERT INTO `contains` (`id`, `contains`) VALUES
('1d19c03d7b0f11e899675254004146e6', 'Uncatagorised'),
('36247d427a4911e899675254004146e6', 'Face'),
('d42200f377ea11e899675254004146e6', 'People');

-- --------------------------------------------------------

--
-- Table structure for table `pictures`
--
-- Creation: Jun 24, 2018 at 11:56 AM
-- Last update: Jun 24, 2018 at 12:13 PM
--

DROP TABLE IF EXISTS `pictures`;
CREATE TABLE `pictures` (
  `id` char(32) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `orgdatetime` datetime DEFAULT NULL,
  `resolution` varchar(15) DEFAULT NULL,
  `lat` decimal(11,7) DEFAULT NULL,
  `lon` decimal(11,7) DEFAULT NULL,
  `make` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `inserted` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- RELATIONS FOR TABLE `pictures`:
--

-- --------------------------------------------------------

--
-- Table structure for table `pic_con`
--
-- Creation: Jun 27, 2018 at 07:28 PM
-- Last update: Jun 28, 2018 at 08:32 PM
--

DROP TABLE IF EXISTS `pic_con`;
CREATE TABLE `pic_con` (
  `id` char(32) NOT NULL,
  `pid` char(32) NOT NULL,
  `cid` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- RELATIONS FOR TABLE `pic_con`:
--   `cid`
--       `contains` -> `id`
--   `pid`
--       `pictures` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `pic_who`
--
-- Creation: Jun 27, 2018 at 07:27 PM
-- Last update: Jun 28, 2018 at 08:33 PM
--

DROP TABLE IF EXISTS `pic_who`;
CREATE TABLE `pic_who` (
  `id` char(32) NOT NULL,
  `pid` char(32) NOT NULL,
  `wid` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- RELATIONS FOR TABLE `pic_who`:
--   `pid`
--       `pictures` -> `id`
--   `wid`
--       `who` -> `id`
--

-- --------------------------------------------------------

--
-- Table structure for table `who`
--
-- Creation: Jun 27, 2018 at 07:21 PM
--

DROP TABLE IF EXISTS `who`;
CREATE TABLE `who` (
  `id` char(32) NOT NULL,
  `frid` int(3) UNSIGNED ZEROFILL NOT NULL,
  `who` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- RELATIONS FOR TABLE `who`:
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contains`
--
ALTER TABLE `contains`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pictures`
--
ALTER TABLE `pictures`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pic_con`
--
ALTER TABLE `pic_con`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pid` (`pid`),
  ADD KEY `cid` (`cid`),
  ADD KEY `cid_2` (`cid`);

--
-- Indexes for table `pic_who`
--
ALTER TABLE `pic_who`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pid` (`pid`),
  ADD KEY `wid` (`wid`);

--
-- Indexes for table `who`
--
ALTER TABLE `who`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pic_con`
--
ALTER TABLE `pic_con`
  ADD CONSTRAINT `pic_con_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `contains` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `pic_con_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `pictures` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `pic_who`
--
ALTER TABLE `pic_who`
  ADD CONSTRAINT `pic_who_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `pictures` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `pic_who_ibfk_2` FOREIGN KEY (`wid`) REFERENCES `who` (`id`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;