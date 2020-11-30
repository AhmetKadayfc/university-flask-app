from my_app import db

class Classroom(db.Model):
    building=db.Column(db.String(15),primary_key=True)
    room_number = db.Column(db.String(7),primary_key=True)
    capacity = db.Column(db.Integer)

    def __init__(self,building,room_number, capacity):
        self.building = building
        self.room_number = room_number
        self.capacity = capacity

    def __repr__(self):
        return '<Classroom %s>'% (self.building, self.room_number)

class Department(db.Model):
    dept_name = db.Column(db.String(20),primary_key=True)
    building= db.Column(db.String(15))
    budget = db.Column(db.Numeric(12,2), db.CheckConstraint('budget>0'))

    def __init__(self,dept_name,building,budget):
        self.dept_name = dept_name
        self.building = building
        self.budget = budget

    def __repr__(self):
        return '<Department %s>'% self.dept_name

class Course(db.Model):
    course_id = db.Column(db.String(8),primary_key=True)
    title = db.Column(db.String(50))
    dept_name = db.Column(db.String(20),db.ForeignKey('department.dept_name',ondelete='SET NULL'))
    credits = db.Column(db.Numeric(2,0), db.CheckConstraint('credits>0'))
    department = db.relationship('Department',backref=db.backref('courses',lazy='dynamic'))

    def __init__(self,course_id,title,department,credits):
        self.course_id = course_id
        self.title = title
        self.department =department
        self.credits = credits

    def __repr__(self):
        return '<Course %s>'% self.course_id

class Instructor(db.Model):
    ID = db.Column(db.String(5),primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    dept_name = db.Column(db.String(20),db.ForeignKey('department.dept_name',ondelete='SET NULL'))
    salary = db.Column(db.Numeric(8,2), db.CheckConstraint('salary>29000'))
    department = db.relationship('Department',backref=db.backref('instructors',lazy='dynamic'))

    def __init__(self,ID,name,department,salary):
        self.ID = ID
        self.name = name
        self.department = department
        self.salary = salary

    def __repr__(self):
        return '<Instructor %s>'% self.ID

class Section(db.Model):
    course_id = db.Column(db.String(8),db.ForeignKey('course.course_id',ondelete='CASCADE'))
    sec_id = db.Column(db.String(8))
    semester = db.Column(db.String(6),db.CheckConstraint('semester in ("Fall","Winter","Spring","Summer")'))
    year = db.Column(db.Numeric(4,0), db.CheckConstraint('year>1701 and year<2100'))
    building = db.Column(db.String(15))
    room_number = db.Column(db.String(7))
    time_slot_id = db.Column(db.String(4))
    
    course = db.relationship('Course',backref=db.backref('sections',lazy='dynamic'))
   
    classroom = db.relationship('Classroom',
                        backref=db.backref('sections',lazy='dynamic'))
    __table_args__ = (
        db.PrimaryKeyConstraint('course_id','sec_id','semester','year'),
        db.ForeignKeyConstraint(['building', 'room_number'],
                                           ['classroom.building', 'classroom.room_number'],ondelete='SET NULL'),)

    def __init__(self,course,sec_id,semester,year,classroom,time_slot_id):
        self.course = course
        self.sec_id = sec_id
        self.semester = semester
        self.year = year
        self.classroom = classroom
        self.time_slot_id = time_slot_id


    def __repr__(self):
        return '<Section %s %s %s>'%self.course_id,self.sec_id,self.semester

class Teaches(db.Model):
    ID = db.Column(db.String(5),db.ForeignKey('instructor.ID',ondelete='CASCADE'))
    course_id = db.Column(db.String(8))
    sec_id = db.Column(db.String(8))
    semester = db.Column(db.String(6))
    year = db.Column(db.Numeric(4,0))

    instructor = db.relationship('Instructor',backref=db.backref('teaches',lazy='dynamic'))
    section = db.relationship('Section',backref=db.backref('teaches',lazy='dynamic'))

    __table_args__ = (
        db.PrimaryKeyConstraint('ID','course_id','sec_id','semester','year'),
        db.ForeignKeyConstraint(['course_id','sec_id','semester','year'],['section.course_id','section.sec_id','section.semester','section.year'],ondelete='CASCADE'),
    )

    def __init__(self,instructor,section):
        self.instructor = instructor
        self.section = section

    def __repr__(self):
        return '<Teaches %s-%d>'%(self.ID,self.course_id,self.sec_id,self.semester),(self.year)


class Student(db.Model):
    ID = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    dept_name = db.Column(db.String(20),db.ForeignKey('department.dept_name',ondelete='SET NULL'))
    tot_cred = db.Column(db.Numeric(3,0),db.CheckConstraint('tot_cred>=0'))

    department = db.relationship('Department',backref = db.backref('students',lazy='dynamic'))

    def __init__(self,name,tot_cred):
        name
        tot_cred

    def __repr__(self):
        return '<Student %s>' %self.ID

class Takes(db.Model):
    ID = db.Column(db.String(5),db.ForeignKey('student.ID',ondelete='CASCADE'))
    course_id = db.Column(db.String(8))
    sec_id = db.Column(db.String(8))
    semester = db.Column(db.String(6))
    year = db.Column(db.Numeric(4,0))
    grade = db.Column(db.String(2))
    
    section = db.relationship('Section',backref=db.backref('takes',lazy='dynamic'))
    student = db.relationship('Student',backref=db.backref('takes',lazy='dynamic'))

    __table_args__ = (
        db.PrimaryKeyConstraint('ID','course_id','sec_id','semester','year'),
        db.ForeignKeyConstraint(['course_id','sec_id','semester','year'],['section.course_id','section.sec_id','section.semester','section.year'],ondelete='CASCADE'),
    )

    def __init__(self,grade):
        grade

    def __repr__(self):
        return '<Takes %s>'%(self.ID,self.course_id,self.sec_id,self.semester,self.year)

class Advisor(db.Model):
    s_ID = db.Column(db.String(5),db.ForeignKey('student.ID',ondelete='CASCADE'),primary_key=True)
    i_ID = db.Column(db.String(5),db.ForeignKey('instructor.ID',ondelete='SET NULL'))

    student = db.relationship('Student',backref=db.backref('advisors',lazy='dynamic'))
    instructor = db.relationship('Instructor',backref=db.backref('advisors',lazy='dynamic'))

    def __repr__(self):
        return '<Advisor %s>'%self.s_ID

    
class Time_Slot(db.Model):
    __tablename__ = 'time_slot'
    time_slot_id = db.Column(db.String(4))
    day = db.Column(db.String(1))
    start_hr = db.Column(db.Numeric(2),db.CheckConstraint('start_hr >= 0 and start_hr < 24'))
    start_min = db.Column(db.Numeric(2),db.CheckConstraint('start_min >= 0 and start_min < 60'))
    end_hr = db.Column(db.Numeric(2),db.CheckConstraint('end_hr >= 0 and end_hr < 24'))
    end_min = db.Column(db.Numeric(2),db.CheckConstraint('end_min >= 0 and end_min < 60'))

    __table_args__ = (
        db.PrimaryKeyConstraint('time_slot_id','day','start_hr','start_min'),
    )

    def __init__(self,end_hr,end_min):
        end_hr
        end_min

    def __repr__(self):
        return '<Time_Slot %s>'%(self.time_slot_id,self.day,self.start_hr,self.start_min)

class Prereq(db.Model):
    course_id = db.Column(db.String(8))
    prereq_id = db.Column(db.String(8))

    course = db.relationship('Course',foreign_keys=[course_id])
    prereq = db.relationship('Course',foreign_keys=[prereq_id])

    __table_args__ = (
        db.PrimaryKeyConstraint('course_id','prereq_id'),
        db.ForeignKeyConstraint(['course_id'],['course.course_id'],ondelete='CASCADE'),
        db.ForeignKeyConstraint(['prereq_id'],['course.course_id']),
    )

    def __repr__(self):
        return '<Prereq %s>'%(self.course_id,self.prereq_id)