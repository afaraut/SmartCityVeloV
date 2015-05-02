BEGIN TRANSACTION;
CREATE TABLE `Weather_day` (
	`day`	INTEGER NOT NULL,
	`temperature`	REAL,
	`precipitation`	REAL,
	PRIMARY KEY(day)
);
CREATE TABLE `Weather` (
	`timestamp`	INTEGER NOT NULL,
	`temperatur`	INTEGER NOT NULL,
	`precipitation`	INTEGER NOT NULL,
	PRIMARY KEY(timestamp)
);
CREATE TABLE `Station` (
	`id`	INTEGER NOT NULL,
	`stationName`	TEXT NOT NULL,
	`adress`	TEXT NOT NULL,
	`totalBikes`	INTEGER NOT NULL,
	`longitude`	REAL NOT NULL,
	`latitude`	REAL NOT NULL,
	`bonus`	NUMERIC NOT NULL,
	`banking`	NUMERIC NOT NULL,
	PRIMARY KEY(id)
);
CREATE TABLE `Request` (
	`id`	INTEGER NOT NULL,
	`stationId`	INTEGER NOT NULL,
	`requestDate`	INTEGER NOT NULL,
	`previsionDate`	INTEGER NOT NULL,
	`realAvailableBikes`	INTEGER NOT NULL,
	`realAvailableStands`	INTEGER NOT NULL,
	`previsionAvailableBikes`	INTEGER NOT NULL,
	`previsionAvailableStands`	INTEGER NOT NULL,
	PRIMARY KEY(id)
);
CREATE TABLE `RecentResults` (
	`stationId`	INTEGER NOT NULL,
	`status`	TEXT NOT NULL,
	`lastUpdate`	INTEGER NOT NULL,
	`availableBikes`	INTEGER NOT NULL,
	`availableStands`	INTEGER NOT NULL,
	PRIMARY KEY(stationId)
);
CREATE TABLE "OldResults" (
	`stationId`	INTEGER NOT NULL,
	`timestamp`	INTEGER NOT NULL,
	`dayOfWeek`	TEXT NOT NULL,
	`hourOfDay`	INTEGER NOT NULL,
	`availableStand`	INTEGER NOT NULL,
	`availableBikes`	INTEGER NOT NULL,
	`vacation`	NUMERIC,
	PRIMARY KEY(stationId,timestamp)
);
;
COMMIT;
