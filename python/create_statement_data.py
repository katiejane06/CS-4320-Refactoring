import math

def create_statement_data(invoice, plays):
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
        return sum(p["volume_credits"] for p in data["performances"])

    def calculate_total_amount(data):
        return sum(perf["amount"] for perf in data["performances"])
    
    def enrich_performance(performance):
        result = performance.copy()
        result["play"] = get_play(result)
        result["amount"] = calculate_amount(result)
        result["volume_credits"] = calculate_volume_credits(result)
        return result

    result = {}
    result['customer'] = invoice['customer']
    result["performances"] = [enrich_performance(performance) for performance in invoice["performances"]]
    result["total_amount"] = calculate_total_amount(result)
    result["total_volume_credits"] = calculate_total_volume_credits(result)
    return result