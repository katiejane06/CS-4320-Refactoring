import math

class PerformanceCalculator:
    def __init__(self, performance, play):
        self.performance = performance
        self.play = play
    @property
    def amount(self):
        result = 0
        if self.play["type"] == "tragedy":
            result = 40000
            if self.performance['audience'] > 30:
                result += 1000 * (self.performance['audience'] - 30)
        elif self.play["type"] == "comedy":
            result = 30000
            if self.performance['audience'] > 20:
                result += 10000 + 500 * (self.performance['audience'] - 20)
            
            result += 300 * self.performance['audience']
            
        else:
            raise ValueError(f'unknown type: {self.play["type"]}')
            
        return result

def create_statement_data(invoice, plays):
    def get_play(performance):
        return plays[performance['playID']]

    def calculate_amount(performance):
        calculator = PerformanceCalculator(performance, get_play(performance))
        return calculator.calculate_amount(performance)

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
        calculator = PerformanceCalculator(performance, get_play(performance))
        result = performance.copy()
        result["play"] = calculator.play
        result["amount"] = calculator.amount
        result["volume_credits"] = calculate_volume_credits(result)
        return result

    result = {}
    result['customer'] = invoice['customer']
    result["performances"] = [enrich_performance(performance) for performance in invoice["performances"]]
    result["total_amount"] = calculate_total_amount(result)
    result["total_volume_credits"] = calculate_total_volume_credits(result)
    return result