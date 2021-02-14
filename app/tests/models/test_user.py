from app.models import User, WishListItem


def test_model_has_str_method():
    user = User(
        id=1,
        full_name="Sample",
        email="useremail.com",
        hashed_password="some-hashed-value",
        is_active=True,
        is_superuser=False,
    )

    expected_user_str = "User(id=1, full_name='Sample', email='useremail.com', is_active=True, is_superuser=False)"
    actual = str(user)

    assert expected_user_str == actual

    item = WishListItem(
        id=1, user_id=user.id, name="Boots", url="https://somenicebootwebsite.com"
    )

    expected_item_str = "WishListItem(id=1, user_id=1, name='Boots', url='https://somenicebootwebsite.com')"
    actual = str(item)

    assert expected_item_str == actual
