BEGIN;

CREATE TABLE primitive_predictions (
    id SERIAL NOT NULL,
    task_id INTEGER NOT NULL,
    primitive_class_id INTEGER NOT NULL,
    x1_coord FLOAT NOT NULL,
    y1_coord FLOAT NOT NULL,
    x2_coord FLOAT NOT NULL,
    y2_coord FLOAT NOT NULL,
    x3_coord FLOAT NOT NULL,
    y3_coord FLOAT NOT NULL,
    x4_coord FLOAT NOT NULL,
    y4_coord FLOAT NOT NULL,
    probability FLOAT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id)
);

COMMIT;
