from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, entity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, model, entity_id):
        return self.db.query(model).filter(model.id == entity_id).first()

    def get_all(self, model):
        return self.db.query(model).all()

    def delete(self, entity):
        self.db.delete(entity)
        self.db.commit()