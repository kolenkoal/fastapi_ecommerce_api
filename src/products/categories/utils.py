def get_new_product_category_data(
    current_product_category, product_category_data
):
    current_address_data = {
        x.name: getattr(current_product_category, x.name)
        for x in current_product_category.__table__.columns
    }

    new_product_category_data = {
        **current_address_data,
        **product_category_data,
    }

    new_product_category_data.pop("id")

    return new_product_category_data
