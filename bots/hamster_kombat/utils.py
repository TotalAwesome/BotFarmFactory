def sorted_by_profit(prepared):
    return sorted(prepared, key=lambda x: x["profitPerHourDelta"], reverse=True)


def sorted_by_profitness(prepared):
    return sorted(
        prepared, key=lambda x: x["profitPerHourDelta"] / x["price"], reverse=True
    )


def sorted_by_price(prepared):
    return sorted(prepared, key=lambda x: x["price"], reverse=False)


def sorted_by_payback(prepared):
    return sorted(
        prepared, key=lambda x: x["price"] / x["profitPerHourDelta"], reverse=False
    )

def get_keys_count_per_game(states):
    result = {}
    for state in states:
        result[state['promoId']] =  state["receiveKeysToday"]
    return result
    