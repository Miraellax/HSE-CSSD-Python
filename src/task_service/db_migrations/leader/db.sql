BEGIN;

CREATE EXTENSION postgres_fdw;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> fb76fd147766

CREATE TABLE classification_models (
    id SERIAL NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (name)
);

CREATE TABLE detection_models (
    id SERIAL NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (name)
);

CREATE TABLE primitive_class (
    id SERIAL NOT NULL, 
    primitive_class VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (primitive_class)
);

CREATE TABLE scene_class (
    id SERIAL NOT NULL, 
    scene_class VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (scene_class)
);

CREATE TABLE status (
    id SERIAL NOT NULL, 
    status VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (status)
);

CREATE TABLE users (
    id SERIAL NOT NULL, 
    username VARCHAR NOT NULL, 
    hashed_password VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (username)
);

CREATE TABLE tasks (
    id SERIAL NOT NULL, 
    owner_id INTEGER NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() at time zone 'utc'),
    scene_class_id INTEGER, 
    detection_model_id INTEGER NOT NULL, 
    classification_model_id INTEGER NOT NULL, 
    status_id INTEGER NOT NULL, 
    input_path VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(classification_model_id) REFERENCES classification_models (id), 
    FOREIGN KEY(detection_model_id) REFERENCES detection_models (id), 
    FOREIGN KEY(owner_id) REFERENCES users (id), 
    FOREIGN KEY(scene_class_id) REFERENCES scene_class (id), 
    FOREIGN KEY(status_id) REFERENCES status (id)
);

CREATE TABLE predictions (
    id SERIAL NOT NULL, 
    task_id INTEGER NOT NULL, 
    primitive_class_id INTEGER NOT NULL, 
    x_coord FLOAT NOT NULL, 
    y_coord FLOAT NOT NULL, 
    width FLOAT NOT NULL, 
    height FLOAT NOT NULL, 
    rotation FLOAT NOT NULL, 
    probability FLOAT NOT NULL
--    ,
--    PRIMARY KEY (id, task_id),
--    FOREIGN KEY(primitive_class_id) REFERENCES primitive_class (id),
--    FOREIGN KEY(task_id) REFERENCES tasks (id) ON DELETE cascade
) PARTITION BY HASH (task_id);

-- foreign shard tables
CREATE SERVER foreign_server_1
        FOREIGN DATA WRAPPER postgres_fdw
        OPTIONS (host 'postgres_foreign_1', port '5432', dbname 'task-service');

CREATE SERVER foreign_server_2
        FOREIGN DATA WRAPPER postgres_fdw
        OPTIONS (host 'postgres_foreign_2', port '5432', dbname 'task-service');

CREATE SERVER foreign_server_3
        FOREIGN DATA WRAPPER postgres_fdw
        OPTIONS (host 'postgres_foreign_3', port '5432', dbname 'task-service');

CREATE USER MAPPING FOR CURRENT_USER
        SERVER foreign_server_1
        OPTIONS (user 'task-service', password '123963');

CREATE USER MAPPING FOR CURRENT_USER
        SERVER foreign_server_2
        OPTIONS (user 'task-service', password '123963');

CREATE USER MAPPING FOR CURRENT_USER
        SERVER foreign_server_3
        OPTIONS (user 'task-service', password '123963');

CREATE FOREIGN TABLE predictions_1 PARTITION OF predictions
    FOR VALUES WITH (MODULUS 4, REMAINDER 0)
    SERVER foreign_server_1
    OPTIONS (schema_name 'public', table_name 'predictions');

CREATE FOREIGN TABLE predictions_2 PARTITION OF predictions
    FOR VALUES WITH (MODULUS 4, REMAINDER 1)
    SERVER foreign_server_2
    OPTIONS (schema_name 'public', table_name 'predictions');

CREATE FOREIGN TABLE predictions_3 PARTITION OF predictions
    FOR VALUES WITH (MODULUS 4, REMAINDER 2)
    SERVER foreign_server_3
    OPTIONS (schema_name 'public', table_name 'predictions');

CREATE TABLE predictions_4 PARTITION OF predictions
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);

INSERT INTO scene_class (scene_class) VALUES
    ('office'),
    ('beach'),
    ('street');

INSERT INTO primitive_class (primitive_class) VALUES
    ('cuboid'),
    ('sphere'),
    ('pyramid'),
    ('torus'),
    ('cylinder');

INSERT INTO status (status) VALUES
    ('queued'),
    ('in progress'),
    ('done');

INSERT INTO detection_models (name) VALUES
    ('YOLO'),
    ('SSD');

INSERT INTO classification_models (name) VALUES
    ('model_v1');

INSERT INTO users (username, hashed_password) VALUES
    ('first', '$2b$12$SmZBPfFaw78FguMgRarX5e1iKckloh6Pi/3Q1ZSGuOzC345gHRL8C'),
    ('second', '$2b$12$n8evGhlqi4pJHmiykHfFzuEqPnE2qLhl1apdj9/.D8cbHCGZmTejO');

INSERT INTO tasks (owner_id,
                   scene_class_id,
                   detection_model_id,
                   classification_model_id,
                   status_id,
                   input_path) VALUES
    (1, 1, 1, 1, 3, 'img_1.png'),
    (1, null, 2, 1, 1, 'img_2.png'),
    (1, null, 1, 1, 2, 'img_3.png'),
    (1, 1, 1, 1, 3, 'img_4.png');

INSERT INTO predictions (task_id,
                         primitive_class_id,
                         x_coord,
                         y_coord,
                         width,
                         height,
                         rotation,
                         probability) VALUES
    (1, 1, 0.5, 0.5, 0.1, 0.1, 0.2, 0.8),
    (1, 2, 0.2, 0.2, 0.1, 0.1, 0.2, 0.88),
    (1, 3, 0.8, 0.8, 0.1, 0.1, 0.2, 0.85),
    (4, 3, 0.8, 0.8, 0.1, 0.1, 0.2, 0.28);

INSERT INTO alembic_version (version_num) VALUES ('fb76fd147766') RETURNING alembic_version.version_num;

COMMIT;

