from sqlalchemy_dbtoolkit.orm.base import Base
from sqlalchemy import Column, Integer, String


class MediaBase:
    id = Column(Integer, primary_key=True)
    title = Column(String(length=255), nullable=False)
    artists = Column(String(length=255))
    track = Column(String(length=255))
    album = Column(String(length=255))
    duration = Column(Integer)
    filename = Column(String(length=255), nullable=False)
    original_url = Column(String(length=255), nullable=False)


class Song(MediaBase, Base):
    __tablename__ = 'songs'


class Video(MediaBase, Base):
    __tablename__ = 'videos'
