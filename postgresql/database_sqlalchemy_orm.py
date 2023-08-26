from sqlalchemy import create_engine, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import os

engine = create_engine(
    f'postgresql+psycopg2://postgres:{os.environ["POSTGRESQLPASSWORD"]}@localhost/red30'
)

Base = automap_base()

Base.prepare(autoload_with=engine)

Sales = Base.classes.sales

# CRUD with sqlalchemy orm
with Session(engine) as session:
    # Read
    smallest_sale = session.execute(select(Sales).order_by(Sales.order_total)).scalar()
    print(smallest_sale.order_total)

    # Insert
    recent_sale = Sales(
        order_num=1105910,
        cust_name="Syman Mapstone",
        prod_number="EB521",
        prod_name="Understanding Artificial Intelligence",
        quantity=3,
        price=19.5,
        discount=0,
        order_total=58.5,
    )
    session.add(recent_sale)
    session.commit()

    # Update
    recent_sale.quantity = 2
    recent_sale.order_total = 39
    updated_sale = session.execute(
        select(Sales).filter(Sales.order_num == 1105910)
    ).scalar()
    print(updated_sale.quantity)
    print(updated_sale.order_total)
    session.commit()

    # Delete
    returned_sale = session.execute(
        select(Sales).filter(Sales.order_num == 1105910)
    ).scalar()
    session.delete(returned_sale)
    session.commit()
