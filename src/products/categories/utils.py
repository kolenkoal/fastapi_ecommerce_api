from sqlalchemy import event
from sqlalchemy.orm import Session

from src.variations.models import Variation


def add_variation_to_children(session, variation):
    category = variation.category
    if category.children_categories:
        for child_category in category.children_categories:
            child_variation = Variation(
                name=variation.name, category_id=child_category.id
            )
            session.add(child_variation)
            add_variation_to_children(session, child_variation)


@event.listens_for(Variation, "after_insert")
def receive_after_insert(mapper, connection, target):
    session = Session.object_session(target)
    add_variation_to_children(session, target)
    session.commit()
