import math

def render_plain_text(invoice, plays):
    def format_as_usd(amount):
        amount = amount/100
        return f"${amount:0,.2f}"
        
    def calculate_amount(performance):
        result = 0
        if get_play(performance)['type'] == "tragedy":
            result = 40000
            if performance['audience'] > 30:
                result += 1000 * (performance['audience'] - 30)
        elif get_play(performance)['type'] == "comedy":
            result = 30000
            if performance['audience'] > 20:
                result += 10000 + 500 * (performance['audience'] - 20)
        
            result += 300 * performance['audience']
        
        else:
            raise ValueError(f'unknown type: {get_play(performance)["type"]}')
        
        return result
            
    def get_play(performance):
        return plays[performance['playID']]
        
    def calculate_volume_credits(performance):
        result = 0
        result += max(performance['audience'] - 30, 0)
        if "comedy" == get_play(performance)["type"]:
            result += math.floor(performance['audience'] / 5)
        return result
            
    def calculate_total_volume_credits():
        result = 0
        for perf in invoice['performances']:
            result += calculate_volume_credits(perf)
        return result
            
    def calculate_total_amount():
        result = 0
        for perf in invoice['performances']:
            result += calculate_amount(perf)
        return result
        
    result = f'Statement for {invoice["customer"]}\n'
    for perf in invoice['performances']:
        result += f' {get_play(perf)["name"]}: {format_as_usd(calculate_amount(perf))} ({perf["audience"]} seats)\n'
    result += f'Amount owed is {format_as_usd(calculate_total_amount())}\n'
    result += f'You earned {calculate_total_volume_credits()} credits\n'
    return result

def statement(invoice, plays):
    return render_plain_text(invoice, plays)
