CREATE DATABASE elections_brazil;
USE elections_brazil;

# ran a few tests here
SHOW TABLES;
SELECT * FROM country;
SELECT * FROM election WHERE id > 10000;
SELECT * FROM election_history WHERE id > 10000;
SELECT * FROM party;
SELECT * FROM result;
