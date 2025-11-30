def test_register_user(db_session):
    # Use db_session directly to manipulate users
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "username": "alice",
        "password": "StrongPass123!"
    }
    from app.models.user import User
    from app.auth.jwt import get_password_hash

    user = User(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"],
        username=user_data["username"],
        hashed_password=get_password_hash(user_data["password"])
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.username == "alice"
