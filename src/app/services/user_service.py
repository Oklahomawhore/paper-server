from ..models import db, User, UserPreferences
from werkzeug.security import generate_password_hash

def register_user(data):
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'], method='sha256')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return {'message': 'User already exists'}, 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User registered successfully'}, 201

def update_user_preferences(data):
    username = data['username']
    preferences = data['preferences']

    user = User.query.filter_by(username=username).first()
    if not user:
        return {'message': 'User not found'}, 404

    for preference, value in preferences.items():
        existing_preference = UserPreferences.query.filter_by(user_id=user.id, preference=preference).first()
        if existing_preference:
            existing_preference.value = value
        else:
            new_preference = UserPreferences(user_id=user.id, preference=preference, value=value)
            db.session.add(new_preference)

    db.session.commit()

    return {'message': 'Preferences updated successfully'}, 200
