import math
from create_statement_data import create_statement_data

def render_plain_text(data, plays):
    def format_as_usd(amount):
        amount = amount/100
        return f"${amount:0,.2f}"
            
    result = f'Statement for {data["customer"]}\n'
    for perf in data['performances']:
        result += f' {perf["play"]["name"]}: {format_as_usd(perf["amount"])} ({perf["audience"]} seats)\n'
    result += f'Amount owed is {format_as_usd(data["total_amount"])}\n'
    result += f'You earned {data["total_volume_credits"]} credits\n'
    return result

def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays), plays)