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

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    
    assignment_id = incoming_payload.get('id')
    new_grade = incoming_payload.get('grade')
    assignment  = Assignment.get_by_id(assignment_id)


    if assignment.state == AssignmentStateEnum.DRAFT:
        return APIResponse.error(message='Assignment in DRAFT state cannot be graded', status_code=400)

    assertions.assert_found(assignment, 'No assignment with this ID was found')

    updated_assignment = Assignment.mark_grade(
        _id = assignment_id,
        grade = new_grade,
        auth_principal=p
    )

    db.session.commit()

    updated_assignment_dump = AssignmentSchema().dump(updated_assignment)

    return APIResponse.respond(data = updated_assignment_dump)