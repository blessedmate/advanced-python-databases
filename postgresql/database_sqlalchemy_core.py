from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, Integer, Float, String, MetaData
import os

engine = create_engine(
    f'postgresql+psycopg2://postgres:{os.environ["POSTGRESQLPASSWORD"]}@localhost/red30',
    echo=True,
)
metadata = MetaData()

sales_table = Table("sales", metadata, autoload_with=engine)

metadata.create_all(engine)

# CRUD with sqlalchemy core
with engine.connect() as conn:
    # Read
    for row in conn.execute(select(sales_table)):
        print(row)

    # Create
    insert_statement = sales_table.insert().values(
        order_num=1105910,
        cust_name="Syman Mapstone",
        prod_number="EB521",
        prod_name="Understanding Artificial Intelligence",
        quantity=3,
        price=19.5,
        discount=0,
        order_total=58.5,
    )
    conn.execute(insert_statement)

    # Update
    update_statement = (
        sales_table.update()
        .where(sales_table.c.order_num == 1105910)
        .values(quantity=2, order_total=39)
    )
    conn.execute(update_statement)

    # Confirm Update
    reselect_statement = sales_table.select().where(sales_table.c.order_num == 1105910)
    updated_sale = conn.execute(reselect_statement).first()
    print(updated_sale)

    # Delete
    delete_statement = sales_table.delete().where(sales_table.c.order_num == 1105910)
    conn.execute(delete_statement)

    # Confirm delete
    not_found_set = conn.execute(reselect_statement)
    print(not_found_set.rowcount)
