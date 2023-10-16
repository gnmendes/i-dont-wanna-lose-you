from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from typing import Union, List

class _Config:

    def __init__(self):
        self.__engine = None
        self.__url = None
    
    def get_instance(self):
        if not self.__engine:
            url = self.__create_url()
            self.__engine = create_engine(url)
        
        return self.__engine
                
    def __create_url(self):
        if not self.__url:
            self.__url = URL.create(
                drivername="postgresql",
                database="contentdb",
                username="root",
                host="localhost",
                password="1234",
                port=5432
            )
        
        return self.__url

class Content:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.category = kwargs.get("category")
        self.duration = kwargs.get("duration")
        self.format = kwargs.get("format")
        self.description = kwargs.get("description")
        self.local_y_n = kwargs.get("local") or "Y"
        self.stored_at = kwargs.get("stored_at")

class ContentRepository(object):
    
    def __init__(self):
        self.__config = _Config()
    
    async def save(self, items):
        if not isinstance(items, list):
            items = [items]
            
        sql = text("""
            WITH content_insert AS(
                INSERT INTO CONTENT (NAME, CATEGORY, DURATION, FORMAT, DESCRIPTION)
                VALUES (:name, :category, :duration, :format, :description)
                RETURNING ID
            )
            
            INSERT INTO STORAGE (LOCAL_Y_N, STORED_AT, CONTENT_ID)
            VALUES(:local_y_n, :stored_at, (SELECT ID FROM CONTENT_INSERT))
        """)

        values = tuple([item.__dict__ for item in items])
        
        with Session(self.__config.get_instance()) as session:
            with session.begin():
                session.execute(sql, values)
