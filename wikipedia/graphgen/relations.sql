DROP TABLE IF EXISTS relations;

CREATE TABLE relations (
    source      STRING NOT NULL,
    dest        STRING NOT NULL,
    PRIMARY KEY (source, dest)
);
