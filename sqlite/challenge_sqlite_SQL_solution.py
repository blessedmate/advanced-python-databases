import sqlalchemy

engine = sqlalchemy.create_engine("sqlite:///users.db", echo=True)


users_list = [
    {
        "first_name": "Sarah",
        "last_name": "Perry",
        "email_address": "sarah.perry@gmail.com",
    },
    {
        "first_name": "John",
        "last_name": "Pork",
        "email_address": "john.pork@gmail.com",
    },
    {
        "first_name": "Martin",
        "last_name": "Ramirez",
        "email_address": "martin.ramirez@gmail.com",
    },
]

with engine.connect() as connection:
    connection.execute(
        sqlalchemy.text(
            """
CREATE TABLE IF NOT EXISTS Users (user_id integer primary key autoincrement, first_name text, last_name text, email_address text)
"""
        )
    )

    connection.execute(
        sqlalchemy.text(
            """
INSERT INTO Users (first_name, last_name, email_address) VALUES (:first_name, :last_name, :email_address)
"""
        ),
        users_list,
    )

    result = connection.execute(
        sqlalchemy.text(
            """
SELECT * FROM Users
"""
        )
    )

    for row in result:
        print(row)

    connection.commit()
