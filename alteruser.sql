PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM utilisateur;

DROP TABLE utilisateur;

CREATE TABLE utilisateur (
    id      INTEGER     NOT NULL,
    nom     TEXT,
    modif   TEXT,
    hashpwd TEXT        NOT NULL,
    admin   INTEGER (1),
    PRIMARY KEY (
        id
    )
);

INSERT INTO utilisateur (
                            id,
                            nom,
                            modif,
                            hashpwd
                        )
                        SELECT id,
                               nom,
                               modif,
                               hashpwd
                          FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;

alter table utilisateur add admin INTEGER(1);
