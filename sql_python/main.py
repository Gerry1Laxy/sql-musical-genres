import psycopg2
import settings


def drop_tables(cur):
    cur.execute(
        """
        DROP TABLE phone;
        DROP TABLE client;
        """
    )


def create_tables(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS client (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(80) NOT NULL,
            last_name VARCHAR(80) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS phone (
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(id) ON DELETE CASCADE,
            number VARCHAR(20)
        );
        """
    )


def add_client(cur, first_name, last_name, email, phone=None):
    try:
        cur.execute(
            """
            INSERT INTO client(first_name, last_name, email) VALUES(
                %s, %s, %s
            ) RETURNING id;
            """,
            (first_name, last_name, email)
        )
        client_id = cur.fetchone()[0]
        if phone:
            add_phone(cur, client_id, phone)
    except Exception as error:
        print(error)


def add_phone(cur, client_id, phone):
    cur.execute(
        """
        INSERT INTO phone(client_id, number) VALUES(%s, %s);
        """,
        (client_id, phone)
    )


def update_client(
        cur,
        client_id,
        first_name=None,
        last_name=None,
        email=None,
        old_phone=None,
        new_phone=None
):
    if first_name:
        cur.execute(
            """
            UPDATE client
            SET first_name = %s
            WHERE id = %s;
            """,
            (first_name, client_id)
        )
    if last_name:
        cur.execute(
            """
            UPDATE client
            SET last_name = %s
            WHERE id = %s;
            """,
            (last_name, client_id)
        )
    if email:
        cur.execute(
            """
            UPDATE client
            SET email = %s
            WHERE id = %s;
            """,
            (email, client_id)
        )
    if old_phone or new_phone:
        if old_phone and new_phone:
            cur.execute(
                """
                UPDATE phone
                SET number = %s
                WHERE client_id = %s AND number = %s;
                """,
                (new_phone, client_id, old_phone)
            )
        else:
            print('Укажите номер, который нужно заменить и новый номер.')


def delete_phone(cur, client_id, phone=None):
    cur.execute(
        """
        DELETE FROM phone
        WHERE client_id = %s AND number = %s;
        """,
        (client_id, phone)
    )


def delete_client(cur, client_id):
    cur.execute(
        """
        DELETE FROM client
        WHERE id = %s;
        """,
        (client_id, )
    )


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    cur.execute(
        """
        SELECT client.id FROM client
        JOIN phone ON phone.client_id = client.id
        WHERE first_name = %s OR last_name = %s OR email = %s OR number = %s;
        """,
        (first_name, last_name, email, phone)
    )
    response = cur.fetchone()
    if response:
        return response[0]
    else:
        print('Клиент не найден')
        return None


def main():
    with psycopg2.connect(
        database=settings.db,
        user=settings.user,
        password=settings.password
    ) as connection:
        with connection.cursor() as cursor:
            drop_tables(cursor)
            create_tables(cursor)
            add_client(
                cursor, 'Marry', 'Watson', 'marrywat@gmail.com', '23-23-23'
            )
            add_phone(cursor, 1, '55-55-55')
            update_client(
                cursor, 1,
                'John', 'Fox', 'johnfox@gmail.com',
                '55-55-55', '44-44-44'
            )
            delete_phone(cursor, 1, '23-23-23')
            delete_client(cursor, 1)
            add_client(
                cursor, 'Marry', 'Watson', 'marrywat@gmail.com', '23-23-23'
            )
            client = find_client(cursor, 'Marry')
            print(f'id клиента: {client}')
            connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
