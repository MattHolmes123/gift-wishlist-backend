from app.models import WishListItem


def test_model_has_str_method():
    item = WishListItem(
        id=1, user_id=1, name="Boots", url="https://somenicebootwebsite.com"
    )

    expected_item_str = "WishListItem(id=1, user_id=1, name='Boots', url='https://somenicebootwebsite.com')"
    actual = str(item)

    assert expected_item_str == actual
