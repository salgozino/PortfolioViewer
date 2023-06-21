from flask import render_template, request, redirect, url_for
import json

import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

from app.operations import bp
from app.models.operations import Operation
from app.models.cash_position import CashPosition


@bp.route('/', methods=['GET', 'POST'])
def portfolio():
    # Assuming the user is always "koki" for now
    user = "koki"

    # Fetch all open trades
    open_trades = Operation.query.filter(
        Operation.close_date.is_(None), Operation.user == user).all()

    # Retrieve the cash position of the user
    cash_position = (
        CashPosition.query
        .filter_by(user=user)
        .order_by(CashPosition.date.desc())
        .first()
    )

    # Calculate the total size of open trades for each ticker
    ticker_sizes = {}
    for trade in open_trades:
        ticker = trade.ticker
        size = trade.size
        price = trade.entry_price
        if ticker in ticker_sizes:
            ticker_sizes[ticker] += size * price
        else:
            ticker_sizes[ticker] = size * price

    # Prepare data for the pie chart
    labels = list(ticker_sizes.keys())
    values = list(ticker_sizes.values())

    # Create the pie chart figure
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Convert the figure to JSON for rendering in the template
    chart_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('operations/open_trades.html',
                           operations=open_trades,
                           chart_json=chart_json,
                           cash_position=cash_position)


@bp.route('/history')
def history():
    # Assuming the user is always "koki" for now
    user = "koki"
    all_op = Operation.query.all()
    operations = Operation.query.filter(
        Operation.close_date.is_not(None), Operation.user == user).all()
    print(operations)
    print(all_op)
    return render_template('operations/all_trades.html', operations=operations)


@bp.route('/new', methods=['GET', 'POST'])
def new_trade():
    if request.method == 'POST':
        user = request.form.get('user')
        ticker = request.form.get('ticker')
        entry_date = request.form.get('entry_date')
        entry_price = float(request.form.get('entry_price'))
        size = float(request.form.get('size'))
        broker = request.form.get('broker')
        trade_type = request.form.get('type')

        operation = Operation(ticker=ticker, entry_date=entry_date, entry_price=entry_price, size=size,
                              broker=broker, type=trade_type, user=user)
        operation.save()

        return redirect(url_for('operations.new_trade'))
    else:
        return render_template('operations/open_trade.html')


@bp.route('/close_trade', methods=['POST'])
def close_trade():
    operation_id = request.form.get('operation_id')
    close_date = request.form.get('close_date')
    close_price = float(request.form.get('close_price'))
    portfolio_value = float(request.form.get('portfolio_value'))

    operation = Operation.query.get(operation_id)
    if operation:
        operation.close_trade(close_date, close_price, portfolio_value)
        return 'Trade closed successfully'
    else:
        return 'Operation not found'


@bp.route('/delete_trade/<int:operation_id>', methods=['GET'])
def delete_trade(operation_id):
    operation = Operation.query.get(operation_id)
    if operation:
        operation.delete()
        return 'Trade deleted successfully'
    else:
        return 'Operation not found'


@bp.route('/close_trade_page/<int:operation_id>')
def close_trade_page(operation_id):
    operation = Operation.query.get(operation_id)
    return render_template('operations/close_trade.html', operation=operation)
