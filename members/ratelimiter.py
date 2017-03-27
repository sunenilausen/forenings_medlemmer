from django.conf import settings
from functools import wraps
from ratelimit.utils import is_ratelimited
from ratelimit.exceptions import Ratelimited
from members.models import Family

_DEFAULT_RATE_BAD = '10/s'
_DEFAULT_RATE_GOOD = None


def create_ratelimiter(group, checker):
    """
    Creates a new ratelimit decorator
    :param group: Key to sort group ratelimits by
    :param checker: A function that returns true if the request is to be ratelimited
    :return: a configured ratelimit decorator
    """
    assert callable(checker)

    def ratelimit(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            group_limits = settings.RATELIMIT_LIMITS.get(group, {})
            if checker(request, *args, **kwargs):
                # Bad request
                rate = group_limits.get('BAD', _DEFAULT_RATE_BAD)
            else:
                # Good request
                rate = group_limits.get('GOOD', _DEFAULT_RATE_GOOD)

            print(rate)
            limited = is_ratelimited(request,
                                     group=group,
                                     key=settings.RATELIMIT_KEY,
                                     rate=rate,
                                     increment=True)

            print(limited)
            if limited:
                raise Ratelimited

            return view(request, *args, **kwargs)

        return wrapper

    return ratelimit


def _check_family(request, unique=None):
    return not Family.objects.filter(unique=unique).exists()


ratelimit_family = create_ratelimiter('family', _check_family)
