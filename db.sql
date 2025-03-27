CREATE DATABASE elections_brazil;
USE elections_brazil;

SHOW TABLES;
SELECT * FROM country;
SELECT * FROM election WHERE id > 10000;
SELECT * FROM election_history WHERE id IN (SELECT MAX(id) FROM election_history);
SELECT * FROM party ORDER BY id ASC;
SELECT * FROM result;

CREATE TABLE person (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_year INT NOT NULL,
    title VARCHAR(255) NULL,
    party_id INT UNIQUE, -- UNIQUE osigurava 1:1 vezu
    CONSTRAINT fk_person_party FOREIGN KEY (party_id) REFERENCES party(id)
);

SELECT * FROM person;

SELECT id FROM party ORDER BY id asc;

INSERT INTO person (first_name, last_name, birth_year, title, party_id) VALUES
('João', 'Silva', 1965, 'Dr.', 1), 
('Carlos', 'Pereira', 1970, 'Eng.', 2),
('Rafael', 'Costa', 1982, NULL, 3),
('Miguel', 'Fernandes', 1958, 'Prof.', 4),
('Ana', 'Santos', 1975, 'Dra.', 5),
('Bruno', 'Almeida', 1980, NULL, 6),
('Ricardo', 'Neves', 1967, NULL, 7),
('Fernanda', 'Martins', 1973, 'Eng.', 8),
('Gustavo', 'Lima', 1988, NULL, 9),
('Patricia', 'Ramos', 1990, 'Dra.', 10),
('Tiago', 'Moreira', 1969, NULL, 11),
('Vasco', 'Mendes', 1972, NULL, 12),
('Diogo', 'Faria', 1960, 'Dr.', 13),
('Helena', 'Cruz', 1985, NULL, 14),
('Sofia', 'Teixeira', 1978, 'Prof.', 15),
('André', 'Rodrigues', 1955, 'Eng.', 16),
('Catarina', 'Barros', 1992, NULL, 17),
('José', 'Nogueira', 1983, NULL, 18),
('Mariana', 'Henriques', 1976, 'Dra.', 19),
('Filipe', 'Coelho', 1991, NULL, 20),
('Eduardo', 'Gomes', 1963, 'Dr.', 21);
