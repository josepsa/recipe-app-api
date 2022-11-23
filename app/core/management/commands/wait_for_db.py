"""
Django custom command to check whether db is available. directory structure should be same,
so django will recognise it as custom management command

"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
       pass

