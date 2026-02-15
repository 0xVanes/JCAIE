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
SHOW DATABASES;
USE sakila;
SHOW tables;
SELECT film.title AS Judul, film.length AS Durasi, language.name AS Bahasa_Film
FROM film
JOIN language
ON film.language_id = language.language_id
WHERE Judul LIKE '%K'
LIMIT 15;

/* NOMOR 7*/
SHOW DATABASES;
USE sakila;
SHOW tables;
DESC actor;
SELECT film.title, actor.first_name, actor.last_name
FROM film_actor
JOIN actor
ON actor.actor_id = film_actor.actor_id
JOIN film
ON film.film_id = film_actor.film_id
WHERE actor.actor_id = 14;

/* NOMOR 8*/
SHOW DATABASES;
USE sakila;
SHOW tables;
DESC city;
SELECT city, country_id
FROM city
WHERE city LIKE '%d%a'
LIMIT 15;

/* NOMOR 9*/
SHOW DATABASES;
USE sakila;
SHOW tables;
SELECT category.name AS Genre, count(category.name) AS Banyak_Film
FROM film_category
JOIN film
ON film_category.film_id = film.film_id
JOIN category
ON category.category_id = film_category.category_id
GROUP BY Genre
ORDER BY Banyak_Film;

/* NOMOR 10*/
SHOW DATABASES;
USE sakila;
SHOW tables;
DESC film;
SELECT title, description, length, rating
FROM film
WHERE title LIKE '%h' AND length > (
	SELECT AVG(length)
    FROM film
)
ORDER BY title
LIMIT 10;
