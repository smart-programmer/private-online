from flask import Blueprint, render_template, make_response, current_app, request, url_for, redirect
from SPORT.utils.utils import reverse_url_for, parse_view_name
from SPORT.utils.languages import LngObj
from SPORT.settings import LANGUAGES
import logging
import os


main_blueprint = Blueprint("main_blueprint", __name__)

@main_blueprint.context_processor
def utility_processor():
    return dict(get_language_text=LngObj.get_language_text, get_current_page_language_list=LngObj.get_current_page_language_list)


@main_blueprint.route('/')
def home():
    page_language_list = LngObj.get_validated_page_language_list("home", request.cookies.get("language"))

    return render_template("index2.html", language_list=page_language_list, languages=LANGUAGES)


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




