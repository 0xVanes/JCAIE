show databases;

/*CREATE DATABASE*/
CREATE DATABASE RENTALMOBIL;
SHOW DATABASES;
USE rentalmobil;

/*CREATE TABLE carrent2026 & COLUMN */
CREATE TABLE carrent2026 (
vehicle_no int(5),
vehicle_brand varchar(20),
vehicle_model varchar(20),
vehicle_type varchar(20),
vehicle_year int(4),
fuel_type varchar(20),
rental_id int(5), /*Kode rental mobil*/
date_rented date, /*Sudah dipinjam dari tanggal sekian oleh beberapa orang */
date_returned date, /*Tanggal terakhir dipinjam oleh orang terakhir*/
distance_travelled_in_km int,
cost_of_rent_per_day int,
trips_taken int(5), /*Sudah dipinjam oleh berapa orang*/
review_count int, /*Semua orang yang meminjam sudah mereview*/
rating int(1) /*Rating secara keseluruhan*/
);

/* SEE THE TABLE */
SELECT *
FROM carrent2026;

/* MASUKIN MIN 10 data*/
INSERT INTO carrent2026 VALUES(1,'Toyota','Agya','MiniBus',2021,'Bensin',10100,'2026-04-25','2026-05-25',1000,100000,3,3,4.2);
INSERT INTO carrent2026 VALUES(2,'Toyota','Camry','Sedan',2025,'Bensin',10101,'2025-04-25','2026-12-12',20120,500000,1,1,5);
INSERT INTO carrent2026 VALUES(2,'Toyota','Vellfire','Minivan',2015,'Bensin',10102,'2019-04-25','2025-11-20',100255,700000,5,4,4.4);
INSERT INTO carrent2026 VALUES(2,'Toyota','Avanza','Minivan',2015,'Bensin',10103,'2015-04-25','2025-10-08',202167,300000,20,15,4.5);

/* SALAH NOMOR vehicle_no*/
SET SQL_SAFE_UPDATES = 0; /*karena WHERE nya pakai key column dan yg diubah primary key (vehicle_no)*/
Update carrent2026
SET vehicle_no = 3
WHERE vehicle_model = 'Vellfire';
Update carrent2026
SET vehicle_no = 4
WHERE vehicle_model = 'Avanza';

/* Lanjut masukin data */
INSERT INTO carrent2026 VALUES(5,'Daihatsu','Terios','SUV',2020,'Bensin',10104,'2020-10-25','2025-11-05',400000,300000,34,26,4.4);
INSERT INTO carrent2026 VALUES(6,'Isuzu','Mux','MiniBus',2015,'Diesel',10105,'2016-01-24','2025-04-01',24003,200000,4,4,3.9);

/*Ganti date_returned jadi last_maintenance_date & hapus date_rented*/
ALTER TABLE carrent2026
RENAME COLUMN date_returned TO date_maintenance;
ALTER TABLE carrent2026
DROP COLUMN date_rented;
ALTER TABLE carrent2026
RENAME COLUMN date_maintenance TO last_maintenance_date;

/*Ganti semua tahun 2026 last_maintenance_date*/
UPDATE carrent2026
SET last_maintenance_date = '2025-12-20'
WHERE trips_taken = 3;

UPDATE carrent2026
SET last_maintenance_date = '2025-12-12'
WHERE trips_taken = 1;

/*Ganti nama column cost_of_rent_per_day*/
ALTER  TABLE carrent2026
RENAME COLUMN cost_of_rent_per_day TO cost_per_day_in_RP;

/*Ganti format rating jadi float*/
ALTER TABLE carrent2026
MODIFY rating FLOAT(2,1);

/*Ganti hasil semua rating*/
UPDATE carrent2026
SET rating=4.2
WHERE trips_taken =3;

UPDATE carrent2026
SET rating = 4.4
WHERE trips_taken=5;

UPDATE carrent2026
SET rating=4.5
WHERE trips_taken = 34;

UPDATE carrent2026
SET rating=3.9
WHERE trips_taken=4;

/*Ganti value distance travelled*/
UPDATE carrent2026
SET distance_travelled_in_km = 2
WHERE trips_taken=3;

UPDATE carrent2026
SET distance_travelled_in_km = 1
WHERE trips_taken=1;

UPDATE carrent2026
SET distance_travelled_in_km = 3
WHERE trips_taken=5;

UPDATE carrent2026
SET distance_travelled_in_km = 10
WHERE trips_taken=20;

UPDATE carrent2026
SET distance_travelled_in_km = 22
WHERE trips_taken=34;

UPDATE carrent2026
SET distance_travelled_in_km = 6
WHERE trips_taken=4;

/*Tambah status mobil*/
ALTER TABLE carrent2026
ADD status varchar(15);

/*Ini bikin row dan column baru tapi eror karena masukin semua values ke row baru
INSERT INTO carrent2026 (status)
Values('Available'),
('In Use'),
('Available'),
('In Use'),
('In Use'),
('Available');

HAPUS NULL VALUE
DELETE FROM carrent2026
WHERE vehicle_no IS NULL;*/

/*Tambahin status di mobil*/
UPDATE carrent2026
SET status='Available'
WHERE vehicle_no =1;

UPDATE carrent2026
SET status='Available'
WHERE vehicle_no =3;

UPDATE carrent2026
SET status='In Use'
WHERE vehicle_no =2;

UPDATE carrent2026
SET status='In Use'
WHERE vehicle_no =4;

UPDATE carrent2026
SET status='In Use'
WHERE vehicle_no =5;

UPDATE carrent2026
SET status='Available'
WHERE vehicle_no =6;

/*Lanjutin tambah data*/
INSERT INTO carrent2026 VALUES(7,'Hyundai','Palisade','SUV',2026,'Bensin',10108,'2026-01-01',3,800000,5,5,5.0,'Available');
INSERT INTO carrent2026 VALUES(8,'Hyundai','Hiace','Minivan',2016,'Diesel',10109,'2026-02-02',3,200000,12,12,3.8,'Available');
INSERT INTO carrent2026 VALUES(9,'Wuling','Air EV','BEV',2023,'Listrik',10110,'2026-02-01',4,100000,47,39,4.0,'Available');
INSERT INTO carrent2026 VALUES(10,'BYD','M6','MPV',2024,'Listrik',10111,'2026-05-12',15,500000,89,82,4.9,'Available');
INSERT INTO carrent2026 VALUES(11,'Mercedes Benz','S400','Sedan',2014,'Bensin',10112,'2026-09-08',3,2000000,3,3,5.0,'In Use');

/*DELETE rental_id*/
ALTER TABLE carrent2026
DROP COLUMN rental_id;

SELECT *
FROM carrent2026;