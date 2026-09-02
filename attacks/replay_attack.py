
from collections import deque
import copy
import random


history = deque(
    maxlen=20
)


def inject(row):

    history.append(
        copy.deepcopy(row)
    )

    if len(history) < 10:

        return row


    old = copy.deepcopy(

        random.choice(
            list(history)[:-5]
        )

    )


    # replay old measurements
    old["timestamp"] = row["timestamp"]


    # slight drift
    old["voltage_v"] *= 0.95

    old["current_a"] *= 1.10


    return old


