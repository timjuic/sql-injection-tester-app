CREATE TABLE Users (
    username TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    registration_date DATE NOT NULL,
    last_login DATETIME,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    PRIMARY KEY (username)
);