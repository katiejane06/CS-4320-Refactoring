import math


def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    def format_as_dollars(amount):
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

    for perf in invoice['performances']:

        # add volume credits
        volume_credits += max(perf['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == get_play(perf)["type"]:
            volume_credits += math.floor(perf['audience'] / 5)
        # print line for this order
        result += f' {get_play(perf)["name"]}: {format_as_dollars(calculate_amount(perf)/100)} ({perf["audience"]} seats)\n'
        total_amount += calculate_amount(perf)

    result += f'Amount owed is {format_as_dollars(total_amount/100)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result
