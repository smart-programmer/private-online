from flask import url_for, current_app, request
import datetime
from flask_mail import Message as MailMessage
from TUTOR import mail



def send_user_confirmation_email(email, confirmation_code):
	#send mail
	string = """TUTOR email verification"""
	msg = MailMessage(string, sender=current_app.config.get("MAIL_USERNAME"), 
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

