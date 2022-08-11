SELECT title, year_release FROM album WHERE year_release = '2018';
SELECT track_name, duration FROM track
WHERE duration = (SELECT MAX(duration) FROM track);
SELECT track_name FROM track WHERE duration >= '210';
SELECT title FROM collection WHERE year_release >= '2018' AND year_release <= '2020';
SELECT * FROM artist WHERE artist_name NOT LIKE '% %';
SELECT track_name FROM track
WHERE LOWER(track_name) LIKE '%my%' OR LOWER(track_name) LIKE '%мой%';
