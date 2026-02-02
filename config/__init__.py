"""
Python 3.14 compatibility: Django's BaseContext.__copy__ uses copy(super())
which fails on Python 3.14. Patch it to create a new instance and copy dicts instead.
"""
import sys

if sys.version_info >= (3, 14):
    import django.template.context

    _BaseContext = django.template.context.BaseContext

    def _base_context_copy(self):
        duplicate = _BaseContext()
        duplicate.__class__ = self.__class__
        duplicate.dicts = self.dicts[:]
        return duplicate

    _BaseContext.__copy__ = _base_context_copy
