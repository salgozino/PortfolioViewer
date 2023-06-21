from flask import request, jsonify, render_template

from app.cash_positions import bp
from app.models.cash_position import CashPosition


@bp.route('/new', methods=['GET', 'POST'])
def new_cash_position():
    if request.method == 'GET':
        return render_template('cash_positions/new.html')
    else:
        value = float(request.form.get('value'))
        user = request.form.get('user')
        date = request.form.get('date')
        # Assuming the user is always "koki" for now
        user = "koki"

        cash_position = CashPosition(user=user, value=value, date=date)
        cash_position.save()

        return jsonify({'message': f'Cash position of {value} created successfully for user {user}'}), 201


@bp.route('/', methods=['GET'])
def get_last_cash_position():
    # Assuming the user is always "koki" for now
    user = "koki"
    # Query the last cash position of the user
    cash_position = CashPosition.query.filter_by(user=user).order_by(CashPosition.date.desc()).first()

    if cash_position:
        cash_position_data = {
            'user': cash_position.user,
            'value': cash_position.value,
            'date': cash_position.date.strftime('%Y-%m-%d')
        }
        return jsonify(cash_position_data), 200
    else:
        return jsonify({'message': 'No cash position found'}), 404
