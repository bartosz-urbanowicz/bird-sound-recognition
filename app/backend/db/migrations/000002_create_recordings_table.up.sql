CREATE TABLE IF NOT EXISTS recordings(
    recording_id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    user_id INT,
    CONSTRAINT fk_customer
        FOREIGN KEY(user_id)
            REFERENCES users(user_id)
);