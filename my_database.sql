
CREATE TABLE Category (
                id INTEGER NOT NULL,
                nom VARCHAR(100) NOT NULL,
                CONSTRAINT category_pk PRIMARY KEY (id)
);


CREATE TABLE Aliment (
                id INTEGER NOT NULL,
                nom VARCHAR(100) NOT NULL,
                nutriscore VARCHAR(100),
                category VARCHAR(100) NOT NULL,
                CONSTRAINT aliment_pk PRIMARY KEY (id)
);


CREATE TABLE Historic (
                id INTEGER NOT NULL,
                nom VARCHAR(100) NOT NULL,
                Date_added DATE NOT NULL,
                CONSTRAINT historic_pk PRIMARY KEY (id)
);


CREATE TABLE Substitute (
                id INTEGER NOT NULL,
                nom VARCHAR(100) NOT NULL,
                lien VARCHAR(250) NOT NULL,
                magasin VARCHAR(100) NOT NULL,
                nutriscore VARCHAR(100) NOT NULL,
                CONSTRAINT substitute_pk PRIMARY KEY (id)
);


ALTER TABLE Aliment ADD CONSTRAINT category_aliment_fk
FOREIGN KEY (id)
REFERENCES Category (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Substitute ADD CONSTRAINT aliment_substitut_fk
FOREIGN KEY (id)
REFERENCES Aliment (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE Historic ADD CONSTRAINT aliment_historic_fk
FOREIGN KEY (id)
REFERENCES Aliment (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
