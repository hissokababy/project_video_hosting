from django.core.management.base import BaseCommand

from broker.handlers import rabbit

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        print('listening...')
        rabbit.run()
