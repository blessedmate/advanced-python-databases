import sqlalchemy

engine = sqlalchemy.create_engine("sqlite:///movies.db", echo=True)

# with engine.connect() as conn:
#     result = conn.execute(sqlalchemy.text("SELECT * FROM Movies"))
#     for row in result:
#         print(row)

metadata = sqlalchemy.MetaData()

movies_table = sqlalchemy.Table(
    "Movies",
    metadata,
    sqlalchemy.Column("title", sqlalchemy.Text),
    sqlalchemy.Column("director", sqlalchemy.Text),
    sqlalchemy.Column("year", sqlalchemy.Integer),
)

metadata.create_all(engine)

with engine.connect() as connection:
    for row in connection.execute(sqlalchemy.select(movies_table)):
        print(row)
