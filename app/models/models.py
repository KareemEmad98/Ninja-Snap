import logging


from app import db

db_logger = logging.getLogger("db_logger")


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            db_logger.info(f"Saved new {self.__class__.__name__} with ID {self.id}")
        except Exception as e:
            db_logger.error(
                f"Error saving {self.__class__.__name__}: {e}", exc_info=True
            )
            raise

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            db_logger.info(f"Deleted {self.__class__.__name__} with ID {self.id}")
        except Exception as e:
            db_logger.error(
                f"Error deleting {self.__class__.__name__}: {e}", exc_info=True
            )
            raise

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            db_logger.info(
                f"Updated {self.__class__.__name__} with ID {self.id}: {kwargs}"
            )
        except Exception as e:
            db_logger.error(
                f"Error updating {self.__class__.__name__}: {e}", exc_info=True
            )
            raise


class IdentifierType(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Segment(BaseModel):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))


class Identifier(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("identifier_type.id"), nullable=False)
    segment_id = db.Column(db.String(255), db.ForeignKey("segment.id"), nullable=False)

    type = db.relationship(
        "IdentifierType", backref=db.backref("identifiers", lazy=True)
    )
    segment = db.relationship("Segment", backref=db.backref("identifiers", lazy=True))

    def save(self):
        existing_identifier = Identifier.query.filter_by(
            value=self.value, segment_id=self.segment_id
        ).first()
        if not existing_identifier:
            super().save()
