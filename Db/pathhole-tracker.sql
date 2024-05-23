-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 14, 2023 at 04:03 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pathhole-tracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `pathhole_detail_image`
--

CREATE TABLE `pathhole_detail_image` (
  `pathhole_id` int(5) NOT NULL,
  `user_id` varchar(40) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `status` varchar(40) DEFAULT NULL,
  `imagename` varchar(40) DEFAULT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pathhole_detail_image`
--

INSERT INTO `pathhole_detail_image` (`pathhole_id`, `user_id`, `location`, `status`, `imagename`, `subject`, `message`, `timestamp`) VALUES
(1, '2', 'Tiruchchirappalli Bypass, Ward 48, Trichy Zone II, Trichy Corporation Limits, Tiruchirappalli, Tiruchchirāppalli, Tiruchirappalli District, Tamil Nadu, 620020, India', '1', 'detectedtwo.jpg', 'd', 'gt', '2023-11-13 23:09:00'),
(2, '2', 'Tiruchchirappalli Bypass, Ward 48, Trichy Zone II, Trichy Corporation Limits, Tiruchirappalli, Tiruchchirāppalli, Tiruchirappalli District, Tamil Nadu, 620020, India', '1', 'detectedistockphoto-531854696-612x612.jp', '', '', '2023-11-13 23:10:31');

-- --------------------------------------------------------

--
-- Table structure for table `user_details`
--

CREATE TABLE `user_details` (
  `user_id` int(20) NOT NULL,
  `user_name` varchar(40) DEFAULT NULL,
  `user_phone` varchar(15) DEFAULT NULL,
  `user_mail` varchar(40) DEFAULT NULL,
  `user_password` varchar(40) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_details`
--

INSERT INTO `user_details` (`user_id`, `user_name`, `user_phone`, `user_mail`, `user_password`, `created_at`) VALUES
(1, 'tTt', '9874563746', 't', '12', '2023-11-13 09:44:02'),
(2, 'tTt', '9874563747', 't', 'aaa', '2023-11-13 09:46:05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pathhole_detail_image`
--
ALTER TABLE `pathhole_detail_image`
  ADD PRIMARY KEY (`pathhole_id`);

--
-- Indexes for table `user_details`
--
ALTER TABLE `user_details`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pathhole_detail_image`
--
ALTER TABLE `pathhole_detail_image`
  MODIFY `pathhole_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user_details`
--
ALTER TABLE `user_details`
  MODIFY `user_id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
