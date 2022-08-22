from flask import Blueprint,render_template

error = Blueprint('error', __name__, static_folder='static',
                 template_folder='templates')

@error.app_errorhandler(404)
def handle_404(err):
    return render_template('404.html'), 404

@error.app_errorhandler(500)
def handle_500(err):
    return render_template('500.html'), 500