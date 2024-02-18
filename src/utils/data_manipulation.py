def get_new_data(current_item, data):
    current_data = {
        x.name: getattr(current_item, x.name)
        for x in current_item.__table__.columns
    }

    new_data = {
        **current_data,
        **data,
    }

    new_data.pop("id")

    return new_data
