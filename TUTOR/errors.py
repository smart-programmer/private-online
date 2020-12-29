from flask import Flask, render_template, url_for, request, redirect, url_for
from TUTOR import app, db, bcrypt, mail


@app.errorhandler(404)
def not_found_error(error):
    error = '404'
    heading = 'Page Not Found'
    paragraph = 'The page you are looking for might have been removed had its name changed or is temporarily unavailable .'
    return render_template('errors/error.html', error=error, heading=heading, paragraph=paragraph), 404


@app.errorhandler(403)
def forbidden_error(error):
    error = '403'
    heading = 'Forbidden'
    paragraph = 'Sorry but you are not allowd for dowing this action .'
    return render_template('errors/error.html', error=error, heading=heading, paragraph=paragraph), 403


@app.errorhandler(410)
def gone_error(error):
    error = '410'
    heading = 'Gone'
    paragraph = 'The above error occurred while the Web Server was processing your request .'
    return render_template('errors/error.html', error=error, heading=heading, paragraph=paragraph), 410


@app.errorhandler(500)
def internal_error(error):
    error = '500'
    heading = 'Internal Server Error'
    paragraph = 'An unexpected error seems to have occured try to refresh the page .'
    return render_template('errors/error.html', error=error, heading=heading, paragraph=paragraph), 500
