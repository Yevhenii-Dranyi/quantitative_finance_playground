from typing import List
from matplotlib import pyplot as plt


def plot_order_flow(book_state_sequence: List[List], price_sequence: List =None, volumes_sequence: List =None, buy_sequence: List =None, sell_sequence: List =None):
    """ Plot the sequence of snapshots of the order book, that is the order flow.
        Moreover, you can plot the executed trades, volumes and prices.

        inputs:
        - book_state_sequence (List[List]): list of lists that contains the sequence of book states. Every state is an order book snapshot.
                        Every snapshot is made like this: [[time,price_ask,volume,'ask']],[[time,price_bid,volume,'bid']].
                        If you have more than one ask or bid, list the asks ascending and bids descending.
                        Example of a book_state_sequence for 2 timesteps:
                        [
                        [[1,101,2,'ask'],[1,102,7,'ask'],[1,103,2,'ask']],[[1,99,5,'bid'],[1,98,7,'bid'],[1,97,2,'bid']],
                        [[2,101,4,'ask'],[2,102,7,'ask'],[2,103,2,'ask']],[[2,99,5,'bid'],[2,98,7,'bid'],[2,97,2,'bid']],
                        ]

        - price_sequence (List): sequence of (executed) prices for the security, i.e. [100,98,98,102]
        - volumes_sequence (List): sequence of executed volumes. i.e [8,7,0,3]. This requires a price_sequence. 
        - buy_sequence (List): sequence with 1 if the executed price is a buy and 0 if it is not. i.e [1,0,0,1]. This requires a price_sequence.
        - sell_sequence (List): sequence with 1 if the executed price is a sell and 0 if it is not. i.e [0,1,0,0]. This requires a price_sequence.
                            Notice that a single entry isn't necessary a buy or a sell. Set it to 0 in both vectors (i.e. the number at the
                            3rd place in the example) if the price didn't move (notice that its volume is 0 and the price didn't change)

    """
    # Step 1: plot the order book in each timestep

    # Get Bid and Ask data in two different lists
    ask_data = [item for sublist in book_state_sequence for item in sublist if item[3] == 'ask']
    bid_data = [item for sublist in book_state_sequence for item in sublist if item[3] == 'bid']

    # get volumes and prices
    ask_times, ask_prices, ask_volumes = zip(*[(d[0], d[1], d[2]) for d in ask_data])
    bid_times, bid_prices, bid_volumes = zip(*[(d[0], d[1], d[2]) for d in bid_data])

    # Normalise the volumes
    max_volume = max(max(ask_volumes), max(bid_volumes))
    norm_ask_volumes = [v / max_volume for v in ask_volumes]
    norm_bid_volumes = [v / max_volume for v in bid_volumes]

    fig, ax = plt.subplots()

    # Plot the asks
    for t, p, v in zip(ask_times, ask_prices, norm_ask_volumes):
        ax.bar(t, v, width=1, bottom=p, color='blue', alpha=0.6)

    # plot the bids
    for t, p, v in zip(bid_times, bid_prices, norm_bid_volumes):
        ax.bar(t, -v, width=1, bottom=p, color='red', alpha=0.6)

    # add some gridlines
    prices = sorted(set(ask_prices + bid_prices))
    for price in prices:
        ax.axhline(y=price, color='grey', linestyle='--', linewidth=0.5)

    # Fill the area between the highest bid and the lowest ask for each time
    # this is the bid ask spread
    unique_times = sorted(set(ask_times + bid_times))
    for t in unique_times:
        ask_prices_at_t = [p for time, p in zip(ask_times, ask_prices) if time == t]
        bid_prices_at_t = [p for time, p in zip(bid_times, bid_prices) if time == t]
        
        if ask_prices_at_t and bid_prices_at_t:
            min_ask_price = min(ask_prices_at_t)
            max_bid_price = max(bid_prices_at_t)
            ax.fill_between([t - 1/2, t + 1/2], max_bid_price, min_ask_price, color='yellow', alpha=0.3, edgecolor='none')


    # axes labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Order Flow')

    # set axes limits
    ax.set_xlim(min(ask_times + bid_times), max(ask_times + bid_times))

    # Step 2: plot the prices
    
    if price_sequence:
        x, y = zip(*[[i + 1, v] for (i, v) in enumerate(price_sequence)])
        ax.plot(x, y, color='orange', label='price')


        if volumes_sequence and buy_sequence and sell_sequence:
            ax.scatter(x, y, s=[val * 20 for val in [v * b for v,b in zip(volumes_sequence, buy_sequence)]], alpha=1, edgecolors='black', color='green')
            ax.scatter(x, y, s=[val * 20 for val in [v * s for v,s in zip(volumes_sequence, sell_sequence)]], alpha=1, edgecolors='black', color='red')

        #ax.legend(loc='upper right')

    plt.show()