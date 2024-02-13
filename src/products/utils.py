def get_new_product_data(current_product, product_data):
    current_product_data = {
        x.name: getattr(current_product, x.name)
        for x in current_product.__table__.columns
    }

    new_product_data = {
        **current_product_data,
        **product_data,
    }

    new_product_data.pop("id")

    return new_product_data
