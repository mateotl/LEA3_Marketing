---preprocesamientos---

--- Crear tabla con los usuarios que tienen entre 30 y 300 ratings---

DROP TABLE IF EXISTS usuarios_selectos;

CREATE TABLE usuarios_selectos AS

SELECT userId AS user_id, COUNT(*) AS cnt_rat
FROM ratings
GROUP BY userId
HAVING cnt_rat > 30 AND cnt_rat < 300;

-- Crear tabla con las películas que tienen más de 10 ratings
DROP TABLE IF EXISTS Pelis_selectas;

CREATE TABLE Pelis_selectas AS

SELECT movieId AS movie_id, COUNT(*) AS cnt_rat
FROM ratings
GROUP BY movieId
HAVING cnt_rat > 10;


---Crear tablas filtradas de movies y ratings---
DROP TABLE IF EXISTS ratings_final;

CREATE TABLE ratings_final AS
SELECT a.userId AS user_id,
       a.movieId AS movie_id,
       a.rating AS movie_rating
FROM ratings a
INNER JOIN Pelis_selectas b ON a.movieId = b.movie_id
INNER JOIN usuarios_selectos c ON a.userId = c.user_id;


DROP TABLE IF EXISTS movies_final;

CREATE TABLE movies_final AS
SELECT a.movieId AS movie_id,
       a.title AS movie_title,
       a.genres AS movie_genres
FROM movies a
INNER JOIN Pelis_selectas c ON a.movieId = c.movie_id;

DROP TABLE IF EXISTS full_ratings;

CREATE TABLE full_ratings AS -- revisar
SELECT a.*,  -- Todas las calificaciones de ratings_final
       c.movie_title,
       c.movie_genres
FROM ratings_final a
INNER JOIN movies_final c ON a.movie_id = c.movie_id;
