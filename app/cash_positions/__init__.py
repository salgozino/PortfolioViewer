from flask import Blueprint

bp = Blueprint('cash_positions', __name__)

from app.cash_positions import routes
