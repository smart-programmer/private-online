import os
from flask import current_app, url_for, request
import json
import datetime
from SPORT.settings import DEFAULT_LANGUAGE, LANGUAGES
from SPORT.utils.utils import parse_view_name, reverse_url_for


class LngObj():
    def __init__(self):
        self.tag = None
        self.text = None


    @staticmethod
    def translate(page_name, language=DEFAULT_LANGUAGE): # returns specific language page
        return LngObj.read_language_file(page_name, language)

    @staticmethod
    def set_user_language(response, language=DEFAULT_LANGUAGE):
        current_time = datetime.datetime.now()
        expire_date = current_time + datetime.timedelta(days=100000)
        response.set_cookie("language", language, expires=expire_date, path="/")

    @staticmethod
    def read_language_file(page_name, language):
        path = os.path.join(current_app.root_path,"static", "languages", language + ".json")

        with open(path, "r", encoding='utf-8') as f:
            language_dict = json.loads(f.read())
            page_list = language_dict.get(page_name)
            return page_list if page_list else []
    
    @staticmethod
    def get_validated_page_language_list(view, language_cookie): # returns specific language page with extra validation
        if not language_cookie or language_cookie not in list(LANGUAGES.values()):
            page_language_list = LngObj.translate(view)
        else:
            page_language_list = LngObj.translate(view, language_cookie)
        return page_language_list

    @staticmethod
    def get_current_page_language_list(): # returns current page language list
        current_page, _args_dict = reverse_url_for(request.path)
        page_language_list = LngObj.get_validated_page_language_list(parse_view_name(current_page)["page_name"], request.cookies.get("language"))
        return page_language_list

    @staticmethod
    def get_language_text(tag, language_list): # returns single text using it's tag
        return next(x.get("description") for x in language_list if x.get("tag") == tag)