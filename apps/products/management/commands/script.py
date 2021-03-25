from django.core.management import BaseCommand



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """
        Write your logic here
        """
        print("Hello PILOT PTN")

