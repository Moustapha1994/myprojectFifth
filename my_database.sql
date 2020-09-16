SET NAMES utf8;

-- Table category
CREATE TABLE IF NOT EXISTS Category (
  id smallint(3) NOT NULL AUTO_INCREMENT,
  name varchar(50) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB;

-- Table product
CREATE TABLE IF NOT EXISTS Product (
  id smallint(3) NOT NULL AUTO_INCREMENT,
  name varchar(200) NOT NULL,
  store varchar(100) NOT NULL,
  link text NOT NULL,
  nutriscore varchar(4) NOT NULL,
  category smallint(3) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_product FOREIGN KEY (category) REFERENCES Category(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Table substitue
CREATE TABLE IF NOT EXISTS Substitute (
  id smallint(3) NOT NULL AUTO_INCREMENT,
  id_product_to_substitute smallint(3) NOT NULL,
  id_substitute_product smallint(3) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_substitute_product FOREIGN KEY (id_substitute_product) REFERENCES Product (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_product_to_substitute FOREIGN KEY (id_product_to_substitute) REFERENCES Product (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;
