from flask import url_for, current_app, request
import datetime
from flask_mail import Message as MailMessage
from TUTOR import mail



def send_user_confirmation_email(email, confirmation_code):
	#send mail
	string = """TUTOR email verification"""
	msg = MailMessage(string, sender="Horizon Light Training Centre", 
	recipients=[email])
	msg.body = f'''your confirmation code is {confirmation_code},
	{request.host_url}{url_for('users_blueprint.email_confirmation')}
	'''
	mail.send(msg)

def send_user_reset_password_email(email, user_serialized_id):
	#send mail
	string = """TUTOR reset password"""
	msg = MailMessage(string, sender=current_app.config.get("MAIL_USERNAME"), 
	recipients=[email])
	msg.body = f'''go to the following link to reset password,
	{request.host_url}{url_for('users_blueprint.reset_password', user_serialized_id=user_serialized_id)}
	'''
	mail.send(msg)

def send_user_change_password_email(email, user_serialized_id):
	#send mail
	string = """TUTOR reset password"""
	msg = MailMessage(string, sender=current_app.config.get("MAIL_USERNAME"), 
	recipients=[email])
	msg.body = f'''This is a confirmation that the password for your TUTOR account has just been changed.
If you didn't change your password, you can secure your account here

	{request.host_url}{url_for('users_blueprint.reset_password', user_serialized_id=user_serialized_id)}
	'''
	mail.send(msg)

def send_email_change_request_email(email, serialized_id_and_email):
	#send mail
	string = """TUTOR change email"""
	msg = MailMessage(string, sender=current_app.config.get("MAIL_USERNAME"), 
	recipients=[email])
	msg.body = f'''you requested to change your TUTOR account email to this email, please click the following link to 
	finish the change: 

	{request.host_url}{url_for('users_blueprint.change_email', user_serialized_id_and_email=serialized_id_and_email)}
	'''
	mail.send(msg)

def send_deny_email_change_email(email, user_serialized_id_and_email):
	#send mail
	string = """TUTOR deny email change"""
	msg = MailMessage(string, sender=current_app.config.get("MAIL_USERNAME"), 
	recipients=[email])
	msg.body = f'''someone requetsed to change your TUTOR account email, if that wasn't you please click the following link to 
	revert the change

	{request.host_url}{url_for('users_blueprint.deny_email_change', user_serialized_id_and_email=user_serialized_id_and_email)}
	'''
	mail.send(msg)

def send_student_course_join_email(user, course):
	#send mail

	string = """HLTC course"""
	msg = MailMessage(string, sender=current_app.config.get("MAIL_USERNAME"), 
	recipients=[user.email])
	msg.body = f'''Congratulations {user.full_name} you have joined the course {course.name}. 
	we will notify you for payment when the course reaches the requested number of students to start which is {course.min_students}
	it's currently at {len(course.students)}

	please pay using this LINK if you dont pay you will not be included in the course
	'''
	mail.send(msg)

def send_student_leave_course_email(user, course):
	#send mail

	string = """HLTC course"""
	msg = MailMessage(string, sender=current_app.config.get("MAIL_USERNAME"), 
	recipients=[user.email])
	msg.body = f'''dear {user.full_name} you have left the que for the course {course.name}. 
	you no longer will be notified when the course is started

	'''
	mail.send(msg)

def send_student_pay_for_course_email(user, course):
	#send mail

	string = """HLTC course"""
	msg = MailMessage(string, sender=current_app.config.get("MAIL_USERNAME"), 
	recipients=[user.email])
	msg.body = f'''Hello {user.full_name} the course {course.name} has reached the requested
	number of students to start. please click this link to pay (LINK)
	and wait for the course tutor to email you the course arrangements

	'''
	mail.send(msg)

def send_student_course_start_email(user, course):
	#send mail

	string = """HLTC course"""
	msg = MailMessage(string, sender="Horizon Light Training Centre", 
	recipients=[user.email])
	msg.body = f'''Hello {user.full_name} we're glad to tell you
	the course you joined {course.name} has started be ready for the tutor to contact you

	'''
	mail.send(msg)

def send_tutor_course_start_email(user, course):
	#send mail

	string = """HLTC course"""
	msg = MailMessage(string, sender="Horizon Light Training Centre", 
	recipients=[user.email])
	msg.body = f'''Hello {user.full_name} the course {course.name} has reached the requested
	number of students to start. please contact the students to set up the course arrangements

	'''
	mail.send(msg)

def send_student_course_ended_email(user, course):
	string = """HLTC course"""
	msg = MailMessage(string, sender="Horizon Light Training Centre", 
	recipients=[user.email])
	msg.body = f'''Hello {user.full_name} the course {course.name} has ended thank you for
	using our website

	'''
	mail.send(msg)

def send_tutor_course_ended_email(user, course):
	string = """HLTC course"""
	msg = MailMessage(string, sender="Horizon Light Training Centre", 
	recipients=[user.email])
	msg.body = f'''Hello {user.full_name} the course {course.name} has ended thank you for
	using our website

	'''
	mail.send(msg)

def send_student_course_canceled_email(user, course):
	string = """HLTC course"""
	msg = MailMessage(string, sender="Horizon Light Training Centre", 
	recipients=[user.email])
	msg.body = f'''Hello {user.full_name} the course {course.name} has been canceled thank you for
	using our website

	'''
	mail.send(msg)

def send_tutor_course_canceled_email(user, course):
	string = """HLTC course"""
	msg = MailMessage(string, sender="Horizon Light Training Centre", 
	recipients=[user.email])
	msg.body = f'''Hello {user.full_name} the course {course.name} has been canceled thank you for
	using our website

	'''
	mail.send(msg)



def send_tutor_accepted_email(tutor):
	string = """HLTC course"""
	msg = MailMessage(string, sender="Horizon Light Training Centre", 
	recipients=[tutor.user.email])
	msg.body = f'''Hello {tutor.user.full_name} congratulations for being accepted 
	into our oraganisation as a tutor 

	'''
	mail.send(msg)