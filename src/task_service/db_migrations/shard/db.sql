BEGIN;

CREATE TABLE predictions (
    id SERIAL NOT NULL,
    task_id INTEGER NOT NULL,
    primitive_class_id INTEGER NOT NULL,
    x_coord FLOAT NOT NULL,
    y_coord FLOAT NOT NULL,
    width FLOAT NOT NULL,
    height FLOAT NOT NULL,
    rotation FLOAT NOT NULL,
    probability FLOAT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id)
);

COMMIT;
