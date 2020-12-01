from flask import Blueprint,request,jsonify,render_template,flash,redirect,url_for
from my_app import app,db
from my_app.university.models import Classroom,Department,Course,Instructor,Section,Teaches,Student,Takes,Advisor,Time_Slot,Prereq
from my_app.university.formModels import CourseForm, InstructorForm, SectionForm,TeachesForm, StudentForm
import ast

university = Blueprint('university',__name__)

@university.route('/')
@university.route('/home')
def home():
    table_names = []
    for clazz in db.Model._decl_class_registry.values():
        try:
            table_names.append(clazz.__tablename__)
        except:
            pass

    return render_template('index.html',models = table_names)


#classroom
@university.route('/classroom-create',methods=['GET','POST'])
def classroom_create():
    if request.method == 'POST':
        building = request.form.get('building')
        room_number = request.form.get('room_number')
        capacity = request.form.get('capacity')
        classroom = Classroom(building,room_number,capacity)
        db.session.add(classroom)
        db.session.commit()
        flash('The classroom has been created', 'success')
        return redirect(url_for('university.classroom', id=classroom.building,key=classroom.room_number))
    return render_template('classroom/create.html')

@university.route('/classroom/<id>/<key>')
def classroom(id=None,key=None):
    classroom = Classroom.query.get_or_404([id,key])
    return render_template('classroom/details.html',classroom=classroom)

@university.route('/classroom')
@university.route('/classroom/page/<int:page>')
def classrooms(page=1):
    classrooms = Classroom.query.paginate(page,8)
    return render_template('classroom/list.html', classrooms=classrooms)


#department
@university.route('/department-create',methods=['GET','POST'])
def department_create():
    if request.method == 'POST':
        dept_name = request.form.get('dept_name')
        building = request.form.get('building')
        budget = request.form.get('budget')
        department = Department(dept_name,building,budget)
        db.session.add(department)
        db.session.commit()
        flash('The department has been created', 'success')
        return redirect(url_for('university.department',id=department.dept_name))
    return render_template('department/create.html')

@university.route('/department/<id>')
def  department(id):
    department = Department.query.get_or_404(id)
    return render_template('department/details.html',department=department)

@university.route('/department')
@university.route('/department/<int:page>')
def departments(page=1):
    departments = Department.query.paginate(page,8)
    return render_template('department/list.html', departments=departments)


#course
@university.route('/course-create',methods=['GET','POST'])
def course_create():
    form = CourseForm(request.form,csrf_enable=False)
    departments = [(d.dept_name, d.dept_name) for d in Department.query.all()]
    form.department.choices= departments

    if request.method == 'POST':
        course_id = request.form.get('course_id')
        title = request.form.get('title')
        department = Department.query.get_or_404(request.form.get('department'))
        credits = request.form.get('credits')
        course = Course(course_id,title,department,credits)
        db.session.add(course)
        db.session.commit()
        flash('The course has been created','success')
        return redirect(url_for('university.course',id=course.course_id))
    return render_template('course/create.html',form=form)

@university.route('/course/<id>')
def course(id):
    course = Course.query.get_or_404(id)
    return render_template('course/details.html', course=course)

@university.route('/course')
@university.route('/course/<int:page>')
def courses(page=1):
    courses = Course.query.paginate(page,8)
    return render_template('course/list.html',courses=courses)


#instructor
@university.route('/instructor-create', methods=['GET', 'POST'])
def instructor_create():
    form = InstructorForm(request.form, csrf_enable=False)
    departments = [(d.dept_name,d.dept_name) for d in Department.query.all()]
    form.department.choices = departments

    if request.method == 'POST':
        ID = request.form.get('ID')
        name = request.form.get('name')
        salary = request.form.get('salary')
        department = Department.query.get_or_404(request.form.get('department'))
        instructor = Instructor(ID,name,department,salary)
        db.session.add(instructor)
        db.session.commit()
        flash('The instructor has been created','success')
        return redirect(url_for('university.instructor',id=instructor.ID))
    return render_template('instructor/create.html',form=form)

@university.route('/instructor/<id>')
def instructor(id):
    instructor = Instructor.query.get_or_404(id)
    return render_template('instructor/details.html', instructor=instructor)

@university.route('/instructor')
@university.route('/instructor/page/<int:page>')
def instructors(page=1):
    instructors = Instructor.query.paginate(page,8)
    return render_template('instructor/list.html', instructors=instructors)


#section
@university.route('/section-create', methods=['GET','POST'])
def section_create():
    form = SectionForm(request.form, csrf_enable=False)
    courses = [(c.course_id,c.title) for c in Course.query.all()]
    classrooms = [([c.building,c.room_number],(c.room_number)) for c in Classroom.query.all()]
    form.course.choices = courses
    form.classroom.choices = classrooms
    if request.method == 'POST':
        classroom_Keys = ast.literal_eval(request.form.get('classroom'))
        course = Course.query.get_or_404(request.form.get('course'))
        sec_id = request.form.get('sec_id')
        semester = request.form.get('semester')
        year =  request.form.get('year')
        classroom =  Classroom.query.get_or_404([classroom_Keys[0],classroom_Keys[1]])
        time_slot_id = request.form.get('time_slot_id')
        section = Section(course,sec_id,semester,year,classroom,time_slot_id)
        db.session.add(section)
        db.session.commit()
        flash('The section has been created','success')
        return redirect(url_for('university.section',id=section.course_id,id2=section.sec_id,id3=section.semester,id4=section.year))
    return render_template('section/create.html',form=form)
    
@university.route('/section/<id>/<id2>/<id3>/<id4>')
def section(id=None,id2=None,id3=None,id4=None):
    section = Section.query.get_or_404([id,id2,id3,id4])
    return render_template('section/details.html', section = section)

@university.route('/section')
@university.route('/section/page/<int:page>')
def sections(page=1):
    sections = Section.query.paginate(page,8)
    return render_template('section/list.html',sections=sections)


#teaches
@university.route('/teaches-create',methods=['GET','POST'])
def teaches_create():
    form = TeachesForm(request.form, csrf_enable=False)
    instructors = [(i.ID,i.name) for i in Instructor.query.all()]
    sections = [([s.course_id,s.sec_id,s.semester,str(s.year)],s.course_id) for s in Section.query.all()]

    form.instructor.choices = instructors
    form.section.choices = sections
    if request.method == 'POST':
        section_Keys = ast.literal_eval(request.form.get('section'))
        instructor = Instructor.query.get_or_404(request.form.get('instructor'))
        section = Section.query.get_or_404(section_Keys)
        teaches = Teaches(instructor,section)
        db.session.add(teaches)
        db.session.commit()
        flash('The teaches has been created', 'success')
        return redirect(url_for('university.teach',id=instructor.ID,id2=section_Keys[0],id3=section_Keys[1],id4=section_Keys[2],id5=section_Keys[3]))
    return render_template('teach/create.html',form=form)


@university.route('/teaches/<id>/<id2>/<id3>/<id4>/<id5>')
def teach(id=None,id2=None,id3=None,id4=None,id5=None):
    teach=Teaches.query.get_or_404([id,id2,id3,id4,id5])
    return render_template('teach/details.html', teach = teach)

@university.route('/teaches')
@university.route('/teaches/page/<int:page>')
def teaches(page=1):
    teaches = Teaches.query.paginate(page,8)
    return render_template('teach/list.html',teaches=teaches)


#student
@university.route('/student-create', methods = ['GET','POST'])
def student_create():
    form = StudentForm(request.form, csrf_enable = False)
    departments = [(d.dept_name,d.dept_name) for d in Department.query.all()]
    form.department.choices = departments

    if request.method == 'POST':
        ID = request.form.get('ID')
        name = request.form.get('name')
        department = Department.query.get_or_404(request.form.get('department'))
        tot_credit = request.form.get('tot_credit')
        student = Student(ID,name,department,tot_credit)
        db.session.add(student)
        db.session.commit()
        flash('The student %s has been created' %name,'success')
        return redirect(url_for('university.student', id=ID))
    return render_template('student/create.html',form=form)

@university.route('/student/<id>')
def student(id):
    student = Student.query.get_or_404(id)
    return render_template('student/details.html', student = student)

@university.route('/student')
@university.route('/student/page/<int:page>')
def students(page=1):
    students = Student.query.paginate(page,8)
    return render_template('student/list.html',students=students)


#takes
@university.route('/takes/<id>/<id2>/<id3>/<id4>/<id5>')
def take(id=None,id2=None,id3=None,id4=None,id5=None):
    take = Takes.query.get_or_404([id,id2,id3,id4,id5])
    return render_template('take/details.html', take=take)

@university.route('/takes')
@university.route('/takes/page/<int:page>')
def takes(page=1):
    takes= Takes.query.paginate(page,8)
    return render_template('take/list.html', takes=takes)


#advisor
@university.route('/advisor/<id>')
def advisor(id):
    advisor = Advisor.query.get_or_404(id)
    return render_template('advisor/details.html', advisor=advisor)

@university.route('/advisor')
@university.route('/advisor/page/<int:page>')
def advisors(page=1):
    advisors = Advisor.query.paginate(page,8)
    return render_template('advisor/list.html', advisors=advisors)


#time slots
@university.route('/time_slot')
@university.route('/time_slot/page/<int:page>')
def time_slots(page=1):
    time_slots = Time_Slot.query.paginate(page,8)
    res={}
    return render_template('time_slots.html', time_slots=time_slots)

    
#prereq    
@university.route('/prereq')
@university.route('/prereq/page/<int:page>')
def prereqs(page=1):
    prereqs = Prereq.query.paginate(page,8)
    return render_template('prereqs.html',prereqs=prereqs)