from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()



def query_data(model, limit=None, order_by=None, filter_by=None, all=True):
    query = db.session.query(model)

    if order_by is not None:
        query = query.order_by(order_by)

    if limit is not None:
        query = query.limit(limit)

    if filter_by is not None:
        query = query.filter_by(**filter_by)

    if limit is not None and order_by is not None:
        query = query.order_by(order_by).limit(limit)

    if limit is not None and filter_by is not None:
        query = query.filter_by(**filter_by).limit(limit)

    if all is False:
        return query.first()

    return query.all()