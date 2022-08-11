CREATE TABLE IF NOT EXISTS Genre (
	id SERIAL PRIMARY KEY,
	genre_name VARCHAR(40) NOT NULL
);
CREATE TABLE IF NOT EXISTS Artist (
	id SERIAL PRIMARY KEY,
	artist_name VARCHAR(80) NOT NULL
);
CREATE TABLE IF NOT EXISTS GenreArtist (
	genre_id INTEGER REFERENCES Genre(id),
	artist_id INTEGER REFERENCES Artist(id),
	CONSTRAINT pk_genre_artist PRIMARY KEY (genre_id, artist_id)
);
CREATE TABLE IF NOT EXISTS Album (
	id SERIAL PRIMARY KEY,
	title VARCHAR(80) NOT NULL,
	year_release VARCHAR(4) NOT NULL
);
CREATE TABLE IF NOT EXISTS AlbumArtist (
	album_id INTEGER REFERENCES Album(id),
	artist_id INTEGER REFERENCES Artist(id),
	CONSTRAINT pk_album_artist PRIMARY KEY (album_id, artist_id)
);
CREATE TABLE IF NOT EXISTS Track (
	id SERIAL PRIMARY KEY,
	track_name VARCHAR(100) NOT NULL,
	duration INTERVAL SECOND NOT NULL,
	album_id INTEGER REFERENCES Album(id)
);
CREATE TABLE IF NOT EXISTS Collection (
	id SERIAL PRIMARY KEY,
	title VARCHAR(80) NOT NULL,
	year_release VARCHAR(4) NOT NULL
);
CREATE TABLE IF NOT EXISTS CollectionTrack (
	collection_id INTEGER REFERENCES Collection(id),
	track_id INTEGER REFERENCES Track(id),
	CONSTRAINT pk_collection_track PRIMARY KEY (track_id, collection_id)
);
