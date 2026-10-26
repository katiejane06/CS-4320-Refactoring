import math

class PerformanceCalculator:
    def __init__(self, performance, play):
        self.performance = performance
        self.play = play
    @property
    def amount(self):
        raise NotImplementedError("Subclasses should calculate the amount")
    @property
    def volume_credits(self):
        return max(self.performance["audience"] - 30, 0)

class TragedyCalculator(PerformanceCalculator):
    @property
    def amount(self):
        result = 40000
        if self.performance['audience'] > 30:
            result += 1000 * (self.performance['audience'] - 30)
        return result

class ComedyCalculator(PerformanceCalculator):
    @property
    def amount(self):
        result = 30000
        if self.performance['audience'] > 20:
            result += 10000 + 500 * (self.performance['audience'] - 20)
        result += 300 * self.performance['audience']
        return result
    @property
    def volume_credits(self):
        return (super().volume_credits + self.performance["audience"] // 5)

class HistoricalCalculator(PerformanceCalculator):
    @property
    def amount(self):
        result = 50000
        if self.performance['audience'] > 20:
            result += 1500 * (self.performance['audience'] - 20)
        return result
    @property
    def volume_credits(self):
        return self.performance["audience"] // 5


def create_performance_calculator(performance, play):
    if play["type"] == "tragedy":
        return TragedyCalculator(performance, play)

    if play["type"] == "comedy":
        return ComedyCalculator(performance, play)

    if play["type"] == "historical":
        return HistoricalCalculator(performance, play)

    raise ValueError(f'unknown type: {play["type"]}')

def create_statement_data(invoice, plays):
    def get_play(performance):
        return plays[performance['playID']]

    def calculate_total_volume_credits(data):
        return sum(p["volume_credits"] for p in data["performances"])

    def calculate_total_amount(data):
        return sum(perf["amount"] for perf in data["performances"])
    
    def enrich_performance(performance):
        calculator = create_performance_calculator(performance, get_play(performance))
        result = performance.copy()
        result["play"] = calculator.play
        result["amount"] = calculator.amount
        result["volume_credits"] = calculator.volume_credits
        return result

    result = {}
    result['customer'] = invoice['customer']
    result["performances"] = [enrich_performance(performance) for performance in invoice["performances"]]
    result["total_amount"] = calculate_total_amount(result)
    result["total_volume_credits"] = calculate_total_volume_credits(result)
    return result