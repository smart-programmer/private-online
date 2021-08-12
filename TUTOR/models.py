from flask import current_app
from TUTOR import db, login_manager, create_app
from TUTOR.utils.utils import get_dicts_with_key
from TUTOR.utils.mail import send_student_pay_for_course_email, send_tutor_course_start_email, send_student_course_join_email, send_student_course_ended_email, send_tutor_course_ended_email, send_student_course_start_email, send_student_course_canceled_email, send_tutor_course_canceled_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, current_user
from datetime import datetime, timedelta
import json

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

class UserModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(30), nullable=False)
    _gender = db.Column(db.Boolean, nullable=False, default=True)
    email_confirmation_code = db.Column(db.String(5), nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin_data_model = db.relationship('AdminDataModel', backref='user', uselist=False)
    tutor_data_model = db.relationship('TutorDataModel', backref='user', uselist=False)
    student_data_model = db.relationship('StudentDataModel', backref='user', uselist=False)

    # The Default Expire Time is Equal to 30 Mins

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def get_reset_token(self, expire_seconds=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expire_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return UserModel.query.get(user_id)

    def get_email_change_token(self, new_email, expire_seconds=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expire_seconds)
        return s.dumps({'user_id': self.id, 'user_email': new_email}).decode('utf-8')

    @staticmethod
    def verify_email_change_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        try:
            user_email = s.loads(token)['user_email']
        except:
            return None
        
        return UserModel.query.get(user_id), user_email

    @property
    def gender(self):
        return "male" if self._gender else "female"


    def __repr__(self):
        return f"{self.full_name}"



courses = db.Table('courses',
    db.Column('course_model_id', db.Integer, db.ForeignKey('course_model.id'), primary_key=True),
    db.Column('student_data_model_id', db.Integer, db.ForeignKey('student_data_model.id'), primary_key=True)
)



class AdminDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))



class CourseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(130), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    min_students = db.Column(db.Integer, nullable=False) 
    max_students = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    began = db.Column(db.Boolean, nullable=False, default=False)
    ended = db.Column(db.Boolean, nullable=False, default=False)
    course_type = db.Column(db.Integer, nullable=False) # 1 for start when min number # 2 for start with min and date
    _period = db.Column(db.Integer, nullable=True) # days
    _start_date = db.Column(db.DateTime, nullable=True)
    _end_date = db.Column(db.DateTime, nullable=True)
    links = db.Column(db.String(), nullable=False) # {"zoom": "link", ....}
    weekly_time_table_json  = db.Column(db.String(1000), nullable=False) # {"saturday": {"from": ..., "to": ...}, ...}
    _state = db.Column(db.String(), nullable=False, default=json.dumps({"state_code": 1, "state_string": "لم تبدأ بعد", "allowed_actions": ["join", "view", "start", "cancel"]})) # {"state_code": 2, "state_string": "قائم", "allowed_actions": ["view", "end"]} {"state_code": 3, "state_string": "انتهى", "allowed_actions": ["delete"]} {"state_code": 4, "state_string": "ملغي", "allowed_actions": ["delete"]}
    number_of_students_paid = db.Column(db.Integer, nullable=False, default=0)
    have_sent_first_payment_emails = db.Column(db.Boolean, nullable=False, default=False)
    created_by_admin = db.Column(db.Boolean, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_model = db.relationship('PaymentModel', backref='course', uselist=False)
    tutor_data_model_id = db.Column(db.Integer, db.ForeignKey('tutor_data_model.id'),
        nullable=False)


    @property
    def period(self):
        if not self._period:
            return int((datetime.date(self._end_date) - datetime.date(self._start_date)).days)
        else:
            return self._period

    @property
    def weekly_time_table(self):
        return json.loads(self.weekly_time_table_json)

    @property
    def start_date(self):
        return "يبدأ عند اكتمال الطلاب" if self._start_date == None else datetime.date(self._start_date)

    @property
    def end_date(self):
        return f"ينتهي بعد {self.period} ايام من بدأ الدورة" if self._end_date == None else datetime.date(self._end_date)

    @property
    def number_of_participants(self):
        return len(self.students)
    
    @property
    def empty_seats(self):
        return self.max_students - self.number_of_participants
    
    # ///////////////////////////// from here i start fixing course systems ///////////////////////////////

    @property
    def state(self): # hold the course's state for example (is it runnung or hasn't began yet...) this helps with determaning what to do with the couse next for example (if it's running we should look into if it should end)
        return json.loads(self._state)
        # if not self.began:
        #     return {"state_code": 1, "state_string": "لم تبدأ بعد", "allowed_actions": ["join", "view", "start", "cancel"]}
        # elif not self.ended:
        #     return {"state_code": 2, "state_string": "قائم", "allowed_actions": ["join", "view", "end"]}
        # else:
        #     return {"state_code": 3, "state_string": "انتهى", "allowed_actions": ["delete"]}

    @staticmethod
    def is_allowed_to_control_course(course, user):
        user_type = user.user_type
        if not user_type == "student":
            allow_tutors_edit_course_setting = SiteSettingsModel.instance().allow_tutors_to_edit_courses["setting_value"]
            if user_type == "tutor":
                if not allow_tutors_edit_course_setting:
                    return False
                else:
                    if user == course.tutor.user:
                        return True
                    else:
                        return False
            else:
                return True
        else:
            return False

    @staticmethod
    def is_allowed_to_create_course(user):
        user_type = user.user_type
        if not user_type == "student":
            allow_tutors_to_create_courses = SiteSettingsModel.instance().allow_tutors_to_create_courses["setting_value"]
            if user_type == "tutor":
                if not allow_tutors_to_create_courses:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

    # def should_send_first_payment_emails(self):
    #     if not self.have_sent_first_payment_emails:
    #         if self.number_of_participants >= self.min_students:
    #             return True

    # def send_all_payment_emails(self):
    #     for student in self.students:
    #         send_student_pay_for_course_email(student.user, self)
    #     self.have_sent_first_payment_emails = True
    #     db.session.commit()

    def start(self): 
        self.began = True
        self._state = json.dumps({"state_code": 2, "state_string": "قائم", "allowed_actions": ["view", "end"]})
        # NOTE: if it's type 2 then period is already calculated in self.period
        if self.course_type == 1:
            now = datetime.date(datetime.utcnow())
            self._start_date = now
            self._end_date = now + timedelta(days=self.period)
        db.session.commit()
        for sdm in self.students: # the paymetn is when a student joins not when the course begins bcz the course wont begin if students didn't pay
            send_student_course_start_email(sdm.user, self)
        send_tutor_course_start_email(self.tutor.user, self)
        return True

    def end(self):
        self.ended = True
        self._state = json.dumps({"state_code": 3, "state_string": "انتهى", "allowed_actions": ["delete"]})
        db.session.commit()
        for sdm in self.students:
            send_student_course_ended_email(sdm.user, self)
        send_tutor_course_ended_email(self.tutor.user, self)
        return True

    def should_start(self):# check should cancel: if it's not should cancel than it's a should start
        if self.startable:
            course_type = self.course_type
            if self.began == True: # this is dump bcz it wouldnt be startable if it has began
                return False
            else:
                course_min_students = self.min_students
                number_of_paid_students = self.payment_model.number_of_students_paid
                if course_type == 1:
                    #check if reached specified student paid number if yes start
                    if number_of_paid_students >= course_min_students:
                        return True
                    else:
                        return False
                elif course_type == 2:
                    # check if reached minimum student have paid number 
                    # check if date has been reached
                    delta = (datetime.date(datetime.utcnow()) - self.start_date).days
                    if delta <= 0:
                        if number_of_paid_students >= course_min_students:
                            return True
                        else:
                            return False
                    else:
                        return False

    def should_end(self): # both types end when end date come NOTE: type 1 end date is set in start method
        if self.endable:
            if not self.began:
                return False
            else:
                delta = (self.end_date - datetime.date(datetime.utcnow())).days
                if delta <= 0:
                    return True
                else:
                    return False
        else:
            return False

    def should_cancel(self): 
        # this is for deleting course and refunding
        # type 2 courses should be deleted when the course date has come but the minimum number of paid student is not met
        # type 1 courses should only be deleted by an authority not automatically and if a student doesn't wanna be wating anymore they could just choose to leave the course and a leave request will be sent to us so we can decide to refund or no
        # all types of courses should be deletd if and authority choses to
        if self.cancelable:
            if self.course_type == 2:
                remaining_days_to_start = (datetime.date(datetime.utcnow()) - self.start_date).days
                if remaining_days_to_start <= 0:
                    if self.payment_model.number_of_students_paid < self.min_students:
                        return True
                
        return False

    def cancel(self):
        # make state canceled
        self._state = json.dumps({"state_code": 4, "state_string": "ملغي", "allowed_actions": ["delete"]})
        db.session.commit()
        self.payment_model.refund_all()
        for sdm in self.students:
            send_student_course_canceled_email(sdm.user, self)
        send_tutor_course_canceled_email(self.tutor.user, self)

    def can_join(self, student):
        # depends on course state and if user has joined and number of students allowed
        if self.joinable:
            if not self.has_student(student):
                if len(self.students) < self.max_students:
                    if student.user.is_confirmed:
                        return True
        return False

    def add_student(self, student):
        student.courses.append(self)
        self.payment_model.add_student(student)
        send_student_course_join_email(student.user, self)
        db.session.commit()

    def has_student(self, student):
        return True if self in student.courses else False

    @property
    def joinable(self):
        return True if "join" in self.state["allowed_actions"] else False

    @property
    def deletable(self):
        return True if "delete" in self.state["allowed_actions"] else False

    @property
    def startable(self):
        return True if "start" in self.state["allowed_actions"] else False

    @property
    def cancelable(self):
        return True if "cancel" in self.state["allowed_actions"] else False

    @property
    def viewable(self):
        return True if "view" in self.state["allowed_actions"] else False

    @property
    def endable(self):
        return True if "end" in self.state["allowed_actions"] else False

    # def remove_action(self, action_name):
    #     self.state[]

    # ////////////////////////////////// from here i stop fixing //////////////////////////////




class TutorDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    nationality = db.Column(db.String(30), nullable=False)
    qualification = db.Column(db.String(35), nullable=False)
    major = db.Column(db.String(35), nullable=False)
    current_job = db.Column(db.String(50), nullable=False)
    _subjects = db.Column(db.String(), nullable=False) # [subject1, subject2, ...]
    years_of_experience = db.Column(db.Integer, nullable=False)
    _tools_used_for_online_tutoring = db.Column(db.String(), nullable=False) # [tool1, tool2, ...]
    is_accepted = db.Column(db.Boolean, nullable=False, default=False)
    courses = db.relationship('CourseModel', backref='tutor')
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))

    @property
    def age(self):
        return int((datetime.date(datetime.utcnow()) - datetime.date(self.date_of_birth)).days / 365)

    @property
    def subjects(self):
        return json.loads(self._subjects)
        # return self._subjects.split(",")
        
    @property
    def tools_used_for_online_tutoring(self):
        return json.loads(self._tools_used_for_online_tutoring)
        # return self._tools_used_for_online_tutoring.split(",")

    def add_to_tools_used_for_online_tutoring(self, tools_list):
        tools = self.tools_used_for_online_tutoring
        tools += tools_list
        self._tools_used_for_online_tutoring = json.dumps(tools)
        db.session.commit()

    # @staticmethod
    # def list_to_comma_seperated_string(ls):
    #     str_ls = str(ls)
    #     str_ls = str_ls.replace(str_ls[0], " ")
    #     str_ls = str_ls.replace(str_ls[-1], " ")
    #     new_ls = str_ls.strip().split(",")
    #     n = None
    #     for item in new_ls:
    #         n = item.strip()
    #         n = str_ls.replace(str_ls[1], "")
    #         n = str_ls.replace(str_ls[-2], "")
    #     return n.strip()
    




class StudentDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'))
    courses = db.relationship('CourseModel', secondary=courses, lazy='subquery',
        backref=db.backref('students', lazy=True))


    @property
    def age(self):
        return int((datetime.date(datetime.utcnow()) - datetime.date(self.date_of_birth)).days / 365)


# /////////////////////////// from here i start fixing billing and POS systems ///////////////////////////

class PaymentModel(db.Model): # a payment class for each course to register course transactions and payment data
    id = db.Column(db.Integer, primary_key=True)
    _transactions_objet = db.Column(db.String(), nullable=False, default="{}") # {"student1_id": [{payment: {date: ..., amount:..., currency:...}}, {refund: ...}], "student2_id": ...}
    last_payment_date = db.Column(db.DateTime, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course_model.id'))   
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def transactions_objet(self):
        if self._transactions_objet:
            return json.loads(self._transactions_objet)
        else:
            return None

    def pay(self, student, price, currency): # if student eligibal to pay then pay course amount using payment gateway api then register payment
        # the pay method can't be implemented yet as it rely on the api heavily 
        # gateway_api.pay(student.account, price, currency)
        self.register_payment(student.id, price, currency)
        return price, currency
            

    def refund(self, student):# if student eligibal for refund then refund paid amount using payment gateway api then register refund
        price, currency = self.price_paid_and_currency(student.id)
        # gateway_api.refund(student.account, price, currency)
        self.register_refund(student.id, price, currency)
        return price, currency


    def refund_all(self): # refund all student who are eligibal for refund with the paid price then register refunds for all
        students = self.students_paid
        for student in students:
            price, currency = self.refund(student)
            self.register_refund(student.id, price, currency)

    def register_payment(self, student_id, amount, currency):
        current_date = datetime.date(datetime.utcnow())
        new_obj = self.transactions_objet
        new_obj[student_id].append({"payment": {"date": current_date, "amount": amount, "currency": currency}})
        self._transactions_objet = json.dumps(new_obj)
        self.last_payment_date = current_date
        db.session.commit()
        
    def register_refund(self, student_id, amount, currency):
        new_obj = self.transactions_objet
        new_obj[student_id].append({"refund": {"date": datetime.date(datetime.utcnow()), "amount": amount, "currency": currency}})
        self._transactions_objet = json.dumps(new_obj)
        db.session.commit()

    def add_student(self, student_id):
        if not self.exists(student_id):
            new_obj = self.transactions_objet
            new_obj[student_id] = []
            self._transactions_objet = json.dumps(new_obj)
            db.session.commit()

    def remove_student(self, student_id):
        if self.exists(student_id):
            new_obj = self.transactions_objet
            new_obj.pop(student_id, None)
            self._transactions_objet = json.dumps(new_obj)
            db.session.commit()

    def exists(self, student_id):
        return True if student_id in self.transactions_objet.keys() else False

    def get_student_payments(self, student):
        get_dicts_with_key(self.transactions_objet[student.user.id], "payment")

    def get_student_refunds(self, student):
        get_dicts_with_key(self.transactions_objet[student.user.id], "refund")

    @property
    def last_payment_period(self):
        if self.last_payment_date:
            return (datetime.date(datetime.utcnow()) - self.last_payment_date).days
        else:
            return None

    def students_paid(self): # returns student_data_models whod paid for the course and not refunded
        # loop through each student transactions if last transaction was payment then put student in list
        students_list = []
        for student_id in self.transactions_objet:
            if self.is_paid_student(student_id):
                students_list.append(StudentDataModel.query.get(student_id))
        return students_list

    @property
    def number_of_students_paid(self):
        return len(self.students_paid) 

    @staticmethod
    def is_payment_dict(transaction_dict): 
        return True if list(transaction_dict.keys())[0] == "payment" else False

    @staticmethod
    def is_refund_dict(transaction_dict):
        return True if list(transaction_dict.keys())[0] == "refund" else False


    def is_paid_student(self, student_id): # return true if last transaction is payment
        if self.exists(student_id):
            last_transaction_dict = self.transactions_objet[student_id][-1] # no need for try catch bcz there always be at least 1 transaction type the first payment when the student joins
            return True if self.is_payment_dict(last_transaction_dict) else False
        return False

    def price_paid_and_currency(self, student_id):
        if self.is_paid_student(student_id):
            payment_transaction_dict = self.transactions_objet[student_id][-1]
            return payment_transaction_dict["amount"], payment_transaction_dict["currency"]
        return 0, 0
                


# ///////////////////////////// from here i stop fixing POS and billing systems ///////////////////////////
    


#///////////////////////////// from here i start fixing setting model /////////////////////////////////

class SiteSettingsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _settings = db.Column(db.String(), nullable=True) # '{"setting_name": {"setting_type": ..., "setting_value": ....}, ....}'


    @property
    def allow_tutors_to_edit_courses(self):
        return self.settings["allow_tutors_to_edit_courses"]

    @property
    def allow_tutors_to_create_courses(self):
        return self.settings["allow_tutors_to_create_courses"]

    @property
    def subjects(self):
        return self.settings["subjects"]

    @property
    def settings(self):
        return json.loads(self._settings)

    def add_setting(self, setting_key, setting_value, setting_type):
        settings_dict = self.settings
        if setting_key in settings_dict:
            return
        settings_dict[setting_key] = {"setting_type": setting_type, "setting_value" : setting_value}
        self._settings = json.dumps(settings_dict)
        db.session.commit()

    def change_setting(self, setting_key, setting_value, setting_type):
        settings_dict = self.settings
        if not setting_key in settings_dict:
            return
        settings_dict[setting_key] = {"setting_type": setting_type, "setting_value" : setting_value}
        self._settings = json.dumps(settings_dict)
        db.session.commit()

    def reverse_bool_setting(self, setting_key):
        settings_dict = self.settings
        settings_dict[setting_key]["setting_value"] = not settings_dict[setting_key]["setting_value"]
        self._settings = json.dumps(settings_dict)
        db.session.commit()

    
    def add_to_list_type_setting(self, setting_key, item):
        settings_dict = self.settings
        settings_dict[setting_key]["setting_value"].append(item)
        self._settings = json.dumps(settings_dict)
        db.session.commit() 

    def remove_from_list_type_setting(self, setting_key, item):
        settings_dict = self.settings
        settings_dict[setting_key]["setting_value"].remove(item)
        self._settings = json.dumps(settings_dict)
        db.session.commit() 

    def add_or_change_to_dict_type_setting(self, setting_key, key, value):
        setting = self.settings[setting_key]["setting_value"]
        setting[key] = value
        self._settings[setting_key]["setting_value"] = json.dumps(setting)
        db.session.commit() 

    @classmethod
    def instance(cls):
        return cls.query.get(1)


# ///////////////////////////////// from here i stop fixing settings model //////////////////////////////////////
