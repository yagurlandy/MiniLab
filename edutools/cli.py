from dotenv import load_dotenv
load_dotenv()

import typer
from edutools.canvas import CanvasLMS

app = typer.Typer()


@app.command()
def courses():
    """List current Canvas courses"""
    try:
        canvas = CanvasLMS()
        courses = canvas.get_courses()

        print("\nCurrent Canvas Courses")
        print("-" * 50)

        for c in courses:
            name = c.get("name") or c.get("course_code") or "Untitled Course"
            workflow = c.get("workflow_state", "")
            if "ARCHIVED" in name.upper():
                continue
            if workflow and workflow != "available":
                continue

            course_id = c.get("id", "no-id")
            print(f"{course_id} - {name}")

    except Exception as e:
        print(f"Error: {e}")


@app.command()
def assignments(course_id: int):
    """List assignments for a course"""
    try:
        canvas = CanvasLMS()
        assignments = canvas.get_assignments(course_id)

        print(f"\nAssignments for Course {course_id}")
        print("-" * 50)

        for a in assignments:
            assignment_id = a.get("id", "no-id")
            assignment_name = a.get("name", "Untitled Assignment")
            print(f"{assignment_id} - {assignment_name}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    app()