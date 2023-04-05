from sqlalchemy.orm.exc import NoResultFound

class ModelMixin:
    @classmethod
    def get_or_create(cls, session, **kwargs):
        try:
            instance = session.query(cls).filter_by(**kwargs).one()
            created = False
        except NoResultFound:
            instance = cls(**kwargs)
            created = True
        return instance, created