from app.security import hash_password, verify_password, create_access_token, decode_token

def test_password_hash_round_trip():
    hashed = hash_password("Demo@12345")
    assert hashed != "Demo@12345"
    assert verify_password("Demo@12345", hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_contains_identity():
    token = create_access_token(7, "official")
    payload = decode_token(token)
    assert payload["sub"] == "7"
    assert payload["role"] == "official"
    assert "exp" in payload
