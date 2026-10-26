from create_statement_data import create_statement_data

def format_as_usd(amount):
    # Charges are stored in cents; convert to dollars for display.
    amount = amount/100
    return f"${amount:0,.2f}"

### STATEMENT RENDERERS
# Both renderers use prepared statement data so charging rules stay separate from output formatting.

def render_html(data):
    result = f'<h1>Statement for {data["customer"]}</h1>\n'
    result += "<table>\n"
    result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>\n"
    for perf in data["performances"]:
        result += (
            f'<tr><td>{perf["play"]["name"]}</td>'
            f'<td>{perf["audience"]}</td>'
            f'<td>{format_as_usd(perf["amount"])}</td></tr>\n'
        )
    result += "</table>\n"
    result += (
        f'<p>Amount owed is <em>{format_as_usd(data["total_amount"])}</em></p>\n'
    )
    result += (
        f'<p>You earned <em>{data["total_volume_credits"]}</em> credits</p>\n'
    )
    return result

def html_statement(invoice, plays):
    return render_html(create_statement_data(invoice, plays))

def render_plain_text(data):     
    result = f'Statement for {data["customer"]}\n'
    for perf in data['performances']:
        result += f' {perf["play"]["name"]}: {format_as_usd(perf["amount"])} ({perf["audience"]} seats)\n'
    result += f'Amount owed is {format_as_usd(data["total_amount"])}\n'
    result += f'You earned {data["total_volume_credits"]} credits\n'
    return result

def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays))