from django.core.management.base import BaseCommand, CommandError
import sys, os

class Command(BaseCommand):

	def handle(self, *args, **options):

		