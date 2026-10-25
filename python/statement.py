import math

def calculate_amount(play, performance):
    result = 0
    if play['type'] == "tragedy":
        result = 40000
        if performance['audience'] > 30:
            result += 1000 * (performance['audience'] - 30)
    elif play['type'] == "comedy":
        result = 30000
        if performance['audience'] > 20:
            result += 10000 + 500 * (performance['audience'] - 20)

        result += 300 * performance['audience']

    else:
        raise ValueError(f'unknown type: {play["type"]}')

    return result

def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    def format_as_dollars(amount):
        return f"${amount:0,.2f}"
    
    def get_play(performance):
        return plays[performance['playID']]

    for perf in invoice['performances']:
        play = get_play(perf)
        this_amount = calculate_amount(play, perf)

        # add volume credits
        volume_credits += max(perf['audience'] - 30, 0)
        # add extra credit for every ten comedy attendees
        if "comedy" == play["type"]:
            volume_credits += math.floor(perf['audience'] / 5)
        # print line for this order
        result += f' {play["name"]}: {format_as_dollars(this_amount/100)} ({perf["audience"]} seats)\n'
        total_amount += this_amount

    result += f'Amount owed is {format_as_dollars(total_amount/100)}\n'
    result += f'You earned {volume_credits} credits\n'
    return result
