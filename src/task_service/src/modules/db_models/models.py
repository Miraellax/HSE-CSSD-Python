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

class PrimitivePredictions(Base):
    __tablename__ = "primitive_predictions"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="cascade"), nullable=False)
    primitive_class_id = Column(Integer, ForeignKey("primitive_class.id"), nullable=False)
    x1_coord = Column(Float, CheckConstraint("x1_coord >= 0 AND x1_coord <= 1"), nullable=False)
    y1_coord = Column(Float, CheckConstraint("y1_coord >= 0 AND y1_coord <= 1"), nullable=False)
    x2_coord = Column(Float, CheckConstraint("x2_coord >= 0 AND x2_coord <= 1"), nullable=False)
    y2_coord = Column(Float, CheckConstraint("y2_coord >= 0 AND y2_coord <= 1"), nullable=False)
    x3_coord = Column(Float, CheckConstraint("x3_coord >= 0 AND x3_coord <= 1"), nullable=False)
    y3_coord = Column(Float, CheckConstraint("y3_coord >= 0 AND y3_coord <= 1"), nullable=False)
    x4_coord = Column(Float, CheckConstraint("x4_coord >= 0 AND x4_coord <= 1"), nullable=False)
    y4_coord = Column(Float, CheckConstraint("y4_coord >= 0 AND y4_coord <= 1"), nullable=False)
    probability = Column(Float, CheckConstraint("probability >= 0 AND probability <= 1"), nullable=False)

class SceneClassPredictions(Base):
    __tablename__ = "scene_class_predictions"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="cascade"), nullable=False)
    scene_class_id = Column(Integer, ForeignKey("primitive_class.id"), nullable=False)
    scene_class_prob = Column(Float, CheckConstraint("scene_class_prob >= 0 AND scene_class_prob <= 1"), nullable=False)
