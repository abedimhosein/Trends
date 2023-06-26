from django.db import transaction

from trends.accounts.models import User, Profile


def create_profile(user: User, fullname: str or None) -> Profile:
    return Profile.objects.create(user=user, fullname=fullname)


def update_profile(user: User, fullname: str or None, about: str or None) -> Profile:
    return Profile.objects.filter(user=user).update(fullname=fullname, about=about)


def create_user(email: str, password: str) -> User:
    return User.objects.create_user(email=email, password=password, usertype=User.Usertype.NORMAL)


@transaction.atomic
def register(fullname: str or None, email: str, password: str) -> User:
    user = create_user(email=email, password=password)
    create_profile(user=user, fullname=fullname)
    return user
