-- 1.1. количество исполнителей в каждом жанре
SELECT (SELECT genre_name FROM genre WHERE id = genre_id), COUNT(artist_id) FROM genreartist
GROUP BY genre_id
ORDER BY COUNT(artist_id) DESC;
-- 1.2. количество исполнителей в каждом жанре
SELECT  g.genre_name, COUNT(ga.artist_id) FROM genreartist ga
LEFT JOIN genre g ON ga.genre_id = g.id
GROUP BY g.genre_name
ORDER BY COUNT(ga.artist_id) DESC;

-- 2. количество треков, вошедших в альбомы 2019-2020 годов;
SELECT COUNT(*) FROM album a
LEFT JOIN track t ON a.id = t.album_id
WHERE a.year_release >= '2019' AND a.year_release <= '2020';

-- 3. средняя продолжительность треков по каждому альбому;
SELECT a.title, AVG(t.duration) FROM album a
LEFT JOIN track t ON a.id = t.album_id
GROUP BY a.id
ORDER BY AVG(t.duration) DESC;

-- 4. все исполнители, которые не выпустили альбомы в 2020 году;
SELECT ar.artist_name, al.year_release FROM artist ar
JOIN albumartist aa ON ar.id = aa.artist_id
JOIN album al ON al.id = aa.album_id
WHERE al.year_release <> '2020';

-- 5. названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
SELECT c.title FROM collection c 
JOIN collectiontrack ct ON c.id = ct.collection_id
JOIN track t ON t.id = ct.track_id 
JOIN album ON album.id = t.album_id
JOIN albumartist a ON a.album_id = album.id
JOIN artist ON artist.id = a.artist_id
GROUP BY c.title, artist.artist_name
HAVING artist.artist_name = 'Billie Eilish';

-- 6. название альбомов, в которых присутствуют исполнители более 1 жанра;
SELECT album.title FROM album
JOIN albumartist a ON a.album_id = album.id
JOIN artist ON artist.id = a.artist_id
JOIN genreartist ga ON ga.artist_id = artist.id
JOIN genre ON genre.id = ga.genre_id
GROUP BY album.id
HAVING COUNT(genre.id) > 1;

-- 7. наименование треков, которые не входят в сборники;
SELECT track.track_name FROM track
LEFT JOIN collectiontrack c ON c.track_id = track.id
GROUP BY track.id, c.track_id
HAVING c.track_id IS NULL;

-- 8. исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
SELECT artist.artist_name FROM artist
JOIN albumartist a ON a.artist_id = artist.id
JOIN track t ON t.album_id = a.album_id
GROUP BY artist.id, t.duration
HAVING t.duration = (SELECT MIN(duration) FROM track);

-- 9. название альбомов, содержащих наименьшее количество треков.
SELECT a.title FROM album a
JOIN track t ON a.id = t.album_id
GROUP BY a.id, t.album_id
HAVING COUNT(t.album_id) = (SELECT MIN(tc.track_count)
FROM (SELECT album_id, COUNT(album_id) AS track_count FROM track GROUP BY album_id) AS tc);
