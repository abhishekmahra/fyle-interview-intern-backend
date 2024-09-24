from core.libs import assertions
from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum, Teacher
from .schema import AssignmentSchema, TeacherSchema
from core import db

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_principal_assignments(p):
    """Returns list of all assignments that are submitted or graded"""
    
    filtered_assignments = Assignment.query.filter(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()

    filtered_assignments_dump = AssignmentSchema().dump(filtered_assignments, many=True)

    return APIResponse.respond(data=filtered_assignments_dump)

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_principal_teachers(p):
    """Returns list of all teachers"""

    all_teachers = Teacher.query.all()

    teachers_dump = TeacherSchema().dump(all_teachers, many=True)

    return APIResponse.respond(data=teachers_dump)
