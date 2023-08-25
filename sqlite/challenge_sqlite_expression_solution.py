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

metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "Users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.Text),
    sqlalchemy.Column("last_name", sqlalchemy.Text),
    sqlalchemy.Column("email_address", sqlalchemy.Text),
)

metadata.create_all(engine)


with engine.connect() as connection:
    connection.execute(sqlalchemy.insert(users_table).values(users_list))
    for row in connection.execute(sqlalchemy.select(users_table)):
        print(row)

# Not so far from the initial attempt c:
