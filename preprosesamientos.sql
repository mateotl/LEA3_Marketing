---preprosesamientos---

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

---Crear tablas filtradas---
