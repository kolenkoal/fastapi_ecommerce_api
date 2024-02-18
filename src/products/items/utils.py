import random
import string


def pick(num):
    for j in range(num):
        return (
            "".join([random.choice(string.digits) for _ in range(3)])
            + "_"
            + "".join(
                [random.choice(string.ascii_uppercase) for _ in range(3)]
            )
            + "_"
            + "".join([random.choice(string.digits) for _ in range(3)])
        )
