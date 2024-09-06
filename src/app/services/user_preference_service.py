from ..models import db, UserPreferences, UserEvent

def update_user_preferences(user_id):
    """
    Update the user's preference vector based on logged events.
    
    :param user_id: The ID of the user to update preferences for.
    """
    # Fetch all events for the user
    events = UserEvent.query.filter_by(user_id=user_id).all()
    
    # Example logic: count occurrences of each event type
    preferences = {}
    for event in events:
        if event.event_type not in preferences:
            preferences[event.event_type] = 0
        preferences[event.event_type] += 1
    
    # Update or create the user preferences in the database
    for event_type, count in preferences.items():
        preference = UserPreferences.query.filter_by(user_id=user_id, preference=event_type).first()
        if preference:
            preference.value = str(count)
        else:
            new_preference = UserPreferences(user_id=user_id, preference=event_type, value=str(count))
            db.session.add(new_preference)
    
    db.session.commit()