from sqlalchemy.exc import SQLAlchemyError
from ..models import db, UserEvent

def log_user_event(user_id, paper_id, event_type):
    """
    Log a user interaction event.

    :param user_id: The ID of the user who performed the action.
    :param paper_id: The ID of the paper the user interacted with.
    :param event_type: The type of event (e.g., 'viewed', 'liked', 'shared').
    :return: The created UserEvent object.
    """
    event = UserEvent(user_id=user_id, paper_id=paper_id, event_type=event_type)

    try:
        db.session.add(event)
        db.session.commit()
        return event
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
