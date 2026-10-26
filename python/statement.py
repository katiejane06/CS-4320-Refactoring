import math

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
    def get_play(performance):
            return plays[performance['playID']]

    def calculate_amount(performance):
            result = 0
            if performance["play"]["type"] == "tragedy":
                result = 40000
                if performance['audience'] > 30:
                    result += 1000 * (performance['audience'] - 30)
            elif performance["play"]["type"] == "comedy":
                result = 30000
                if performance['audience'] > 20:
                    result += 10000 + 500 * (performance['audience'] - 20)
            
                result += 300 * performance['audience']
            
            else:
                raise ValueError(f'unknown type: {performance["play"]["type"]}')
            
            return result

    def calculate_volume_credits(performance):
            result = 0
            result += max(performance['audience'] - 30, 0)
            if "comedy" == performance["play"]["type"]:
                result += math.floor(performance['audience'] / 5)
            return result

    def calculate_total_volume_credits(data):
            result = 0
            for perf in data['performances']:
                result += perf["volume_credits"]
            return result

    def calculate_total_amount(data):
        result = 0
        for perf in data['performances']:
            result += perf["amount"]
        return result
    
    def enrich_performance(performance):
        result = performance.copy()
        result["play"] = get_play(result)
        result["amount"] = calculate_amount(result)
        result["volume_credits"] = calculate_volume_credits(result)
        return result
    
    statement_data = {}
    statement_data['customer'] = invoice['customer']
    statement_data["performances"] = [enrich_performance(performance)for performance in invoice["performances"]]
    statement_data["total_amount"] = calculate_total_amount(statement_data)
    statement_data["total_volume_credits"] = calculate_total_volume_credits(statement_data)

    return render_plain_text(statement_data, plays)
