def get_new_variation_data(current_variation, variation_data):
    current_variation_data = {
        x.name: getattr(current_variation, x.name)
        for x in current_variation.__table__.columns
    }

    new_variation_data = {
        **current_variation_data,
        **variation_data,
    }

    new_variation_data.pop("id")

    return new_variation_data
