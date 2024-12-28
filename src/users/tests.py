import pytest


@pytest.mark.django_db
def test_create_user(django_user_model):
    user = django_user_model.objects.create_user(
        email="foo@bar.com", password="apabepa"
    )

    assert user.email == "foo@bar.com"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.username is None

    with pytest.raises(TypeError):
        django_user_model.objects.create_user()
    with pytest.raises(TypeError):
        django_user_model.objects.create_user(email="")
    with pytest.raises(ValueError):
        django_user_model.objects.create_user(email="", password="apabepa")


def test_create_superuser(django_user_model):
    user = django_user_model.objects.create_superuser(
        email="root@bar.com", password="apabepa"
    )

    assert user.email == "root@bar.com"
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.username is None

    with pytest.raises(ValueError):
        django_user_model.objects.create_superuser(
            email="root@bar.com", password="apabepa", is_superuser=False
        )
