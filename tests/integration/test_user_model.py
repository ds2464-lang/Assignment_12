def test_login_existing_user(test_user):
    from app.auth.jwt import verify_password

    # test_user is already inserted in the DB
    assert verify_password("wrongpassword", test_user.hashed_password) is False
    assert verify_password(test_user.password, test_user.hashed_password) is True
