from database import session_creater


class BaseServices:
    
    model = None
    
    @classmethod
    def get_object_by_uuid(cls, uuid: int):
        with session_creater() as s:
            object = s.query(cls.model).filter_by(uuid = uuid).first()
            return object
    
    
    @classmethod
    def delete_object_by_uuid(cls, uuid: int):
        with session_creater() as s:
            s.query(cls.model).filter_by(uuid = uuid).delete()
            s.commit()
    
    