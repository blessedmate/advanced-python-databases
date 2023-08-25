import sqlalchemy

engine = sqlalchemy.create_engine("sqlite:///users.db", echo=True)

metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "Users",
    metadata,
    sqlalchemy.column("user_id", sqlalchemy.Integer),
    sqlalchemy.column("first_name", sqlalchemy.Text),
    sqlalchemy.column("last_name", sqlalchemy.Text),
    sqlalchemy.column("email_address", sqlalchemy.Text),
)

metadata.create_all(engine)

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
    for row in connection.execute(sqlalchemy.insert(users_table).values(users_list)):
        print(row)
