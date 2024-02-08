def get_new_payment_method_data(current_payment_method, payment_method_data):
    current_payment_method_data = {
        x.name: getattr(current_payment_method, x.name)
        for x in current_payment_method.__table__.columns
    }

    new_payment_method = {**current_payment_method_data, **payment_method_data}

    new_payment_method.pop("id")

    return new_payment_method
