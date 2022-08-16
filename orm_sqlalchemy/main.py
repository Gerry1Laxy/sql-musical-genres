import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import (
    create_table,
    Publisher,
    Book,
    Shop,
    Stock,
    Sale
)


DSN = f'postgresql://{config.USER}:{config.PASSWORD}@{config.HOST}:{config.PORT}/{config.DB_NAME}'


def open_data_json(file_name):
    with open(file_name) as f:
        if f:
            return json.load(f)


def insert_data(data, session):
    models = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale
    }
    for model, records in data.items():
        for record in records:
            session.add(models[model](**record))


def get_publisher_id(session):
    user_input = input('Введите имя или id издателя:\n')

    if user_input.isdecimal():
        publisher = session.query(Publisher).filter(
            Publisher.id == user_input
        ).first()
    else:
        publisher = session.query(Publisher).filter(
            Publisher.name == user_input
        ).first()

    if publisher:
        return publisher.id
    else:
        return None


def find_publishers_shop(session, publ_id):
    query = session.query(Shop).join(
        Stock,
        Book,
        Publisher
    ).filter(Publisher.id == publ_id).all()
    return query


def main():
    engine = create_engine(DSN)
    create_table(engine)

    # Session = sessionmaker(bind=engine)
    # session = Session()

    session = sessionmaker(bind=engine, autocommit=True)()

    name_test_data_file = 'fixtures/test_data.json'
    test_data = open_data_json(name_test_data_file)

    insert_data(test_data, session)

    publisher_id = get_publisher_id(session)
    publishers_shops = find_publishers_shop(session, publisher_id)

    if publishers_shops:
        print('Магазины этого издателя')
        for shop in publishers_shops:
            print(f'Shop id: {shop.id}, {shop.name}')


if __name__ == '__main__':
    main()
