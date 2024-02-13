def get_new_variation_option_data(
    current_variation_option, variation_option_data
):
    current_variation_option_data = {
        x.name: getattr(current_variation_option, x.name)
        for x in current_variation_option.__table__.columns
    }

    new_variation_data = {
        **current_variation_option_data,
        **variation_option_data,
    }

    new_variation_data.pop("id")

    return new_variation_data
