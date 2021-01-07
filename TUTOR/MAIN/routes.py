from flask import Blueprint, render_template, make_response, current_app, request, url_for, redirect
from flask_login import current_user
from TUTOR.utils.utils import reverse_url_for, parse_view_name
from TUTOR.utils.languages import LngObj
from TUTOR.settings import LANGUAGES, ADMIN_TYPES
from TUTOR.models import SiteSettingsModel
import logging
import os

# a blueprint for unauthorised users or views for all types of users

main_blueprint = Blueprint("main_blueprint", __name__)

@main_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list, languages=LANGUAGES, admin_types=ADMIN_TYPES, settings=SiteSettingsModel.get_settings_dict())


@main_blueprint.route('/')
def home():
    return render_template("index2.html", admin_types=ADMIN_TYPES)


@main_blueprint.route('/register')
def register():
    return render_template("register.html")







@main_blueprint.route("/change_language")
def change_language():
    language = request.args.get("language")
    next_page = request.args.get("next")
    if not language:
        return redirect(url_for("main_blueprint.home"))

    if not next_page:
        response = make_response(redirect(url_for('index')))
    else:
        response = make_response(redirect(next_page))

    LngObj.set_user_language(response, language)
    
    return response



@main_blueprint.route('/how_to_download_zoom')
def how_to_download_zoom():
    return render_template("how_to_download_zoom.html")