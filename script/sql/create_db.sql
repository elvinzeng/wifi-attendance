-- -----------------------------------
-- desc: create database and user
-- author: Elvin Zeng
-- date: 2017-5-29
-- -----------------------------------
CREATE DATABASE wifi_attendance_db;
CREATE USER wifi_attendance_user IDENTIFIED BY 'wifi_attendance_user_password';
GRANT ALL PRIVILEGES ON wifi_attendance_db.* TO wifi_attendance_user IDENTIFIED BY 'wifi_attendance_user_password'