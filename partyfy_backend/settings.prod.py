try:
    from .base import *  # noqa
except ImportError:
    pass

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

sentry_sdk.init(
    dsn=config('SENTRY_DNS'),
    integrations=[DjangoIntegration()]
)
