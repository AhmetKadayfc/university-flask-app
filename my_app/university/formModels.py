from flask_wtf import Form
from wtforms import TextField,SelectField, DecimalField, IntegerField,validators
from wtforms.validators import InputRequired

class CourseForm(Form):
    course_id = TextField('Course Id', [validators.required()])
    title = TextField('Title', [validators.required()])
    credits = TextField('Credits')
    department = SelectField('Department',coerce=str)

class InstructorForm(Form):
    ID = TextField('ID', [validators.required()])
    name = TextField('Name', [validators.required()])
    salary = DecimalField('Salary')
    department = SelectField('Department',coerce=str)

class SectionForm(Form):
    course = SelectField('Course',validators=[InputRequired()],coerce=str)
    sec_id = TextField('Section ID')
    semester = SelectField('Semester', choices=[('Fall','Fall'),('Winter','Winter'),('Spring','Spring'),('Summer','Summer')])
    year =  IntegerField('Year', [validators.required(), validators.length(min=1701,max=2100)])
    classroom = SelectField('Classroom', coerce=str)
    time_slot_id = TextField('Time Slot', [validators.required()])

class TeachesForm(Form):
    instructor = SelectField('Instructor',validators=[InputRequired()],coerce=str)
    section = SelectField('Section',validators=[InputRequired()],coerce=str)

class StudentForm(Form):
    ID = TextField('Student Id',[validators.required()])
    name = TextField('Name',[validators.required()])
    department = SelectField('Department',coerce=str)
    tot_credit = TextField('Total Credit', [validators.length(min=0)])