/* NOMOR 1 */
SHOW DATABASES;
USE sakila;
SHOW tables;
SELECT *
FROM payment
LIMIT 10;

/* NOMOR 2*/
SHOW DATABASES;
USE sakila;
SHOW tables;
SELECT title, release_year, rental_duration
FROM film
WHERE title LIKE 'S%'
LIMIT 10;

/* NOMOR 3*/
SHOW DATABASES;
USE sakila;
SHOW tables;
DESC film;
SELECT rental_duration AS Durasi_Rental, COUNT(film_id) AS Banyak_Film, ROUND(AVG(length)) AS Rata_Rata_Durasi_Film
FROM film
GROUP BY Durasi_Rental
ORDER BY Durasi_Rental;

/* NOMOR 4*/
SHOW DATABASES;
USE sakila;
SHOW tables;
DESC film;
SELECT title, length, rating
FROM film
WHERE length > (
	SELECT AVG(length)
    FROM film
)
ORDER BY length DESC
LIMIT 25;

/* NOMOR 5*/
SHOW DATABASES;
USE sakila;
SHOW tables;
DESC film;
SELECT rating AS Rating, MAX(replacement_cost) AS Replacement_Cost_Tertinggi, MIN(rental_rate) AS Rental_Rate_Terendah, AVG(length) as Rata_Rata_Durasi
FROM film
GROUP BY Rating
ORDER BY Rating;

/* NOMOR 6*/

/* NOMOR 7*/

/* NOMOR 8*/

/* NOMOR 9*/

/* NOMOR 10*/
