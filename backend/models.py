from sqlalchemy import Column, Integer, String, Text, ForeignKey
from backend.database import Base




# PROJECTS (completed + progress)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    location = Column(String)
    description = Column(Text)
    section = Column(String)   # completed or progress
    image_path = Column(String)


# BEFORE & AFTER

class BeforeAfter(Base):
    __tablename__ = "before_after"

    id = Column(Integer, primary_key=True)
    before_image = Column(String)
    after_image = Column(String)
    description = Column(Text)
    location = Column(String)


# COMMENTS / REVIEWS

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    comment = Column(Text)
