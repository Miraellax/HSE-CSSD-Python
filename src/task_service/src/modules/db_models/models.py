import enum

from sqlalchemy import ForeignKey, String, Column, Integer, Float, DateTime, CheckConstraint, func
from sqlalchemy.orm import declarative_base


# Базовый класс для таблиц базы данных
Base = declarative_base()
base_metadata = Base.metadata

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    scene_class_id = Column(Integer, ForeignKey("scene_class.id"))
    detection_model_id = Column(Integer, ForeignKey("detection_models.id"), nullable=False)
    classification_model_id = Column(Integer, ForeignKey("classification_models.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    input_path = Column(String, nullable=False)

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    status = Column(String, unique=True, nullable=False)

class SceneClass(Base):
    __tablename__ = "scene_class"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    scene_class = Column(String, unique=True, nullable=False)

class PrimitiveClass(Base):
    __tablename__ = "primitive_class"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    primitive_class = Column(String, unique=True, nullable=False)

class DetectionModels(Base):
    __tablename__ = "detection_models"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String, unique=True, nullable=False)

class ClassificationModels(Base):
    __tablename__ = "classification_models"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String, unique=True, nullable=False)

class Predictions(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="cascade"), nullable=False)
    primitive_class_id = Column(Integer, ForeignKey("primitive_class.id"), nullable=False)
    x_coord = Column(Float, CheckConstraint("x_coord >= 0 AND x_coord <= 1"), nullable=False)
    y_coord = Column(Float, CheckConstraint("y_coord >= 0 AND y_coord <= 1"), nullable=False)
    width = Column(Float, CheckConstraint("width >= 0 AND width <= 1"), nullable=False)
    height = Column(Float, CheckConstraint("height >= 0 AND height <= 1"), nullable=False)
    rotation = Column(Float, CheckConstraint("rotation >= 0 AND rotation <= 1"), nullable=False)
    probability = Column(Float, CheckConstraint("probability >= 0 AND probability <= 1"), nullable=False)
