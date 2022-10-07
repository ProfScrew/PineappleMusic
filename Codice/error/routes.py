from flask import Blueprint,render_template
from flask_login import current_user

error = Blueprint('error', __name__, static_folder='static',
                 template_folder='templates')

@error.app_errorhandler(404)
def not_found(err):
    return render_template('404.html'), 404

@error.app_errorhandler(500)
def server_error(err):
    return render_template('500.html'), 500
@error.app_errorhandler(405)
def method_not_allowed(err):
    return render_template('405.html'), 405
@error.app_errorhandler(403)
def unauthorized(err):
    return render_template('403.html',user = current_user), 403
@error.app_errorhandler(412)
def precondition_failed(err):
    return render_template('412.html'), 412