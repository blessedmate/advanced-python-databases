import os
import mysql.connector as mysql


def connect(db_name):
    try:
        return mysql.connect(
            host="localhost",
            user="root",
            password=os.environ["MYSQLPASSWORD"],
            database=db_name,
        )
    except Exception as e:
        print(e)


def add_project(
    cursor: mysql.connection.CursorBase,
    project_title: str,
    project_description: str,
    tasks: [str],
):
    project_data = (project_title, project_description)
    cursor.execute(
        """INSERT INTO projects(title, description) VALUES (%s, %s)""",
        project_data,
    )
    tasks_data = []
    for task in tasks:
        task_data = (cursor.lastrowid, task)
        tasks_data.append(task_data)
    cursor.executemany(
          """INSERT INTO tasks(project_id, description) VALUES (%s, %s)""",
        tasks_data,
    )


if __name__ == "__main__":
    db = connect("projects")
    cursor = db.cursor()

    # create new project with associated tasks
    tasks = ["Clean bathroom", "Clean kitchen", "Clean living room"]
    add_project(cursor, "Clean house", "Clean house by room", tasks)

    # select and visualize
    cursor.execute("SELECT * FROM projects")
    project_records = cursor.fetchall()
    print(project_records)

    cursor.execute("SELECT * FROM tasks")
    tasks_records = cursor.fetchall()
    print(tasks_records)

    db.close()
