import random
import string


def generate_reference(prefix="TXN"):

    random_part = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=10
        )
    )

    return f"{prefix}-{random_part}"