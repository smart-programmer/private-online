import os
import secrets
from PIL import Image
import boto3
from flask import url_for, current_app, request
import datetime
from random import randint
from flask.globals import _app_ctx_stack, _request_ctx_stack
from werkzeug.urls import url_parse
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS
from functools import wraps
# from TUTOR.models import Visitors, db

def save_image_locally(image_file, path):
	
	# create a random name
	random_hex = secrets.token_hex(20)

	# get file extention via os module
	_, extention = os.path.splitext(image_file.filename)

	# create image name
	image_filename = random_hex + extention

	# specify image path
	image_path = os.path.join(current_app.root_path, path, image_filename)

	# resize image with pillow and save it 
	new_size = (600, 600)
	image = Image.open(image_file)
	image.thumbnail(new_size)
	image.save(image_path)

	## image_file.save(image_path)

	if os.environ.get("online"):
		return image_filename, image_path
	else:
		return image_filename, url_for("static", filename="profiles/images/"+ image_filename) # a new url for the local image is returned here because the images_path variable has a url relative to the whole os which is ok when we save the image but when displaying the image on the server we need a path relative to the server not the os which is what url_for returns

def delete_image(image_path):
	os.remove(current_app.root_path + image_path)



def save_image(image_file, path):
	if os.environ.get("online"):	
		# connect to s3
		# s3_client = boto3.client('s3')
		s3_resource = boto3.resource('s3')
		my_bucket = s3_resource.Bucket("cam-media-static-files")

		# save image locally
		image_filename, local_path = save_image_locally(image_file, path)

		# upload image to s3 
		my_bucket.upload_file(Filename=local_path, Key=image_filename)

		# remove image from local machine
		os.remove(local_path)

		s3_path = "https://s3-us-west-2.amazonaws.com/cam-media-static-files/" + image_filename # or: https://cam-media-static-files.s3.amazonaws.com/
		
		return image_filename, s3_path


	else:
		return save_image_locally(image_file, path)


def delete_s3_object(object_name, object_path):
	if os.environ.get("online"):
		s3_resource = boto3.resource('s3')
		s3_resource.Object('cam-media-static-files', object_name).delete()
	else:
		local_image_path = current_app.root_path + object_path # the function os.path.join didn't work here, NOTE: see the comment in the "save_image_locally" function to know why we need a new image path relative to the os to delete the image
		os.remove(local_image_path)



def generate_random_digits(n):
	range_start = 10**(n-1)
	range_end = (10**n) - 1
	return randint(range_start, range_end)


def reverse_url_for(url, method = None):
    appctx = _app_ctx_stack.top
    reqctx = _request_ctx_stack.top
    if appctx is None:
        raise RuntimeError('Attempted to match a URL without the '
                           'application context being pushed. This has to be '
                           'executed when application context is available.')

    if reqctx is not None:
        url_adapter = reqctx.url_adapter
    else:
        url_adapter = appctx.url_adapter
        if url_adapter is None:
            raise RuntimeError('Application was not able to create a URL '
                               'adapter for request independent URL matching. '
                               'You might be able to fix this by setting '
                               'the SERVER_NAME config variable.')
    parsed_url = url_parse(url)
    if parsed_url.netloc is not "" and parsed_url.netloc != url_adapter.server_name:
        raise NotFound()
    return url_adapter.match(parsed_url.path, method) # return value is a tuple with the endpoint name and a dict with the arguments.

def parse_view_name(view_name):
	view_name_list = view_name.split(".")
	blueprint_name = view_name_list[0]
	page_name = view_name_list[1]
	return {"blueprint_name": blueprint_name, "page_name": page_name}

def login_required(roles=[]):
	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):
			if request.method in EXEMPT_METHODS:
				return fn(*args, **kwargs)
			elif current_app.login_manager._login_disabled:
				return fn(*args, **kwargs)
			elif not current_user.is_authenticated:
				return current_app.login_manager.unauthorized()
			role = current_user.user_type
			if ( (role not in roles) and (roles != []) ):
				return current_app.login_manager.unauthorized()      
			return fn(*args, **kwargs)
		return decorated_view
	return wrapper

def list_to_select_compatable_tuple(ls, identifier, front):
	base_list = []
	for obj in ls:
		base_list.append(tuple([str(getattr(obj, identifier)), str(getattr(obj, front))]))
	return tuple(base_list)

def dict_to_select_compatable_tuple(info_dict):
	base_list = []
	for key, value in info_dict.items():
		base_list.append((str(key), str(value)))
	return tuple(base_list)



# def handle_new_visitor(response):
# 	expire_date = datetime.datetime.now()
# 	expire_date = expire_date + datetime.timedelta(days=100000)
# 	response.set_cookie("did_visit", "True", expires=expire_date)
# 	increase_visitors_counter()

# # def get_visitors_file():
# # 	return os.getcwd()+"/WEBSITE/static/visitors.txt" #url_for("static", filename="visitors.txt")



# def increase_visitors_counter():

# 	visitors = Visitors.query.get(1)
# 	visitors.count += 1
# 	db.session.commit()

# 	# with open(get_visitors_file(), "r+") as visitors_file:
# 	# 	number = int(visitors_file.read())
# 	# 	number += 1
# 	# 	visitors_file.truncate(0)
# 	# 	visitors_file.seek(0)
# 	# 	visitors_file.write(str(number))