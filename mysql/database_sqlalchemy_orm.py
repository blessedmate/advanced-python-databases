import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, select
from sqlalchemy.orm import registry, relationship, Session

engine = create_engine(
    f"mysql+mysqlconnector://root:{os.environ['MYSQLPASSWORD']}@localhost:3306/projects",
    echo=True,
)

mapper_registry = registry()
# mapper_resgistry.metadata

Base = mapper_registry.generate_base()


class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    title = Column(String(length=50))
    description = Column(String(length=50))

    def __repr__(self):
        return f"<Project(title='{self.title}, description={self.description})>"


class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    description = Column(String(length=50))

    # relationship between models
    project = relationship("Project")

    def __repr__(self):
        return f"<Task(description='{self.description})>"


Base.metadata.create_all(engine)


# Add data using a session
with Session(engine) as session:
    organize_closet_project = Project(
        title="Organize closet", description="Organize closet by color and style"
    )

    session.add(organize_closet_project)

    session.flush()

    tasks = [
        Task(
            project_id=organize_closet_project.project_id,
            description="Organize what clothes to donate",
        ),
        Task(
            project_id=organize_closet_project.project_id,
            description="Organize summer clothes",
        ),
        Task(
            project_id=organize_closet_project.project_id,
            description="Organize winter clothes",
        ),
    ]

    session.bulk_save_objects(tasks)

    session.commit()

# Retrieve data using a session
with Session(engine) as session:
    smt = select(Project).where(Project.title == "Organize closet")
    results = session.execute(smt)
    # scalar() returns the first row
    organize_closet_project = results.scalar()

    smt2 = select(Task).where(Task.project_id == organize_closet_project.project_id)
    results = session.execute(smt2)
    for task in results:
        print(task)
