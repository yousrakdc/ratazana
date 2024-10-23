from django.core.management.base import BaseCommand
from core.models import Jersey, Alert


from django.core.management.base import BaseCommand
from core.models import Jersey, Alert

class Command(BaseCommand):
    help = 'Check and trigger alerts for price changes.'

    def handle(self, *args, **kwargs):
        alerts = Alert.objects.filter(status='active')
        for alert in alerts:
            jersey = alert.jersey
            current_price = jersey.price
            
            # Check for price drop
            if alert.alert_type == 'price_drop' and current_price < alert.target_price:
                alert.trigger_alert()

        self.stdout.write(self.style.SUCCESS('Alerts checked and triggered successfully.'))

def check_price_alerts(user):
    jerseys = Jersey.objects.all()
    
    for jersey in jerseys:
        if jersey.price < jersey.last_known_price:
            # Create an alert for the user
            alert = Alert(jersey=jersey, user=user)
            alert.save() 
            print(f"Alert created for Jersey ID: {jersey.id} - New Price: {jersey.price}")

        jersey.last_known_price = jersey.price
        jersey.save()

