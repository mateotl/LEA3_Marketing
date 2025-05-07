---preprocesamientos---

--- Crear tabla con los usuarios que tienen entre 30 y 300 ratings---

drop table if exists usuarios_selectos;

create table usuarios_selectos
select userId AS user_id, COUNT(*) AS cnt_rat
from ratings
group by userId
having cnt_rat >30 AND cnt_rat < 300
Order by cnt_rat desc;

---Crear tabla con las peliculas que tienen mas de 10 ratings---
drop table if exists Pelis_selectas;

create table Pelis_selectas
select movieId AS movie_id, COUNT(*) AS cnt_rat
from ratings
group by movieId
having cnt_rat > 10
Order by cnt_rat desc;

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
       a.genres AS movie_genres,
FROM movies a
INNER JOIN Pelis_selectas c ON a.movieId = c.movie_id;

DROP TABLE IF EXISTS full_ratings;

CREATE TABLE full_ratings AS ## revisar
SELECT a.*,  -- Todas las calificaciones de ratings_final
       c.movie_title,
FROM ratings_final a
INNER JOIN users_final b ON a.user_id = b.user_id
INNER JOIN movies_final c ON a.movie_id = c.movie_id;
