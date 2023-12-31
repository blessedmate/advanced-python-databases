import os
from sqlalchemy import (
    Column,
    String,
    Integer,
    create_engine,
    select,
    func,
    Numeric,
)
from sqlalchemy.orm import registry, Session

engine = create_engine(
    f"mysql+mysqlconnector://root:{os.environ['MYSQLPASSWORD']}@localhost:3306/red30",
    echo=True,
)

mapper_registry = registry()

Base = mapper_registry.generate_base()


class Sale(Base):
    __tablename__ = "sales"
    order_num = Column(Integer, primary_key=True)
    cust_name = Column(String)
    prod_number = Column(Integer)
    prod_name = Column(String)
    quantity = Column(Integer)
    price = Column(Numeric)
    discount = Column(Numeric)
    order_total = Column(Numeric)

    def __repr__(self):
        return f"<Sale(order_num='{self.order_num}, cust_name={self.cust_name}, prod_number={self.prod_number}, prod_name={self.prod_name}, quantity={self.quantity}, price={self.price}, discount={self.discount},order_total={self.order_total})>"


Base.metadata.create_all(engine)


# Add data using a session
# with Session(engine) as session:
#     sale_1 = Sale(
#         order_num=1100935,
#         cust_name="Spencer Educators",
#         prod_number="DK204",
#         prod_name="BYOD-300",
#         quantity=2,
#         price=89,
#         discount=0,
#         order_total=178,
#     )
#     sale_2 = Sale(
#         order_num=1100948,
#         cust_name="Ewan Ladd",
#         prod_number="TV810",
#         prod_name="Understanding Automation",
#         quantity=1,
#         price=44.95,
#         discount=0,
#         order_total=44.95,
#     )
#     sale_3 = Sale(
#         order_num=1100963,
#         cust_name="Stehr Group",
#         prod_number="DS301",
#         prod_name="DA-SA702 Drone",
#         quantity=3,
#         price=399,
#         discount=0.1,
#         order_total=1077.3,
#     )
#     sale_4 = Sale(
#         order_num=1100971,
#         cust_name="Hettinger and Sons",
#         prod_number="DS306",
#         prod_name="DA-SA702 Drone",
#         quantity=12,
#         price=250,
#         discount=0.5,
#         order_total=1500,
#     )
#     sale_5 = Sale(
#         order_num=1100998,
#         cust_name="Luz O'Donoghue",
#         prod_number="TV809",
#         prod_name="Understanding 3D Printing",
#         quantity=1,
#         price=42.99,
#         discount=0,
#         order_total=42.99,
#     )

#     sales = [sale_1, sale_2, sale_3, sale_4, sale_5]

#     session.bulk_save_objects(sales)
#     session.flush()
#     session.commit()

# Retrieve data
with Session(engine) as session:
    max_query = select(func.max(Sale.order_total))
    max_order_total = session.execute(max_query).scalar()
    print(max_order_total)

    results_query = select(Sale).order_by(Sale.order_total.desc())
    results_in_order = session.execute(results_query)
    for order in results_in_order:
        print(order)
