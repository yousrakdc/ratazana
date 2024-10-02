from django.core.management.base import BaseCommand
from core.models import Jersey

class Command(BaseCommand):
    help = 'Clean up jersey image paths in the database'

    def handle(self, *args, **options):
        for jersey in Jersey.objects.all():
            current_image_path = str(jersey.image_path).strip()
            
            # Skip invalid entries
            if current_image_path.lower() == 'n/a':
                self.stdout.write(self.style.WARNING(f'Skipping jersey ID {jersey.id} with invalid image path: {current_image_path}'))
                continue

            # Check for multiple images and keep the first one
            if ',' in current_image_path:
                new_image_path = current_image_path.split(',')[0].strip()
                jersey.image_path = new_image_path
                jersey.save()
                self.stdout.write(self.style.SUCCESS(f'Updated jersey ID {jersey.id} to: {new_image_path}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Jersey ID {jersey.id} has a valid path: {current_image_path}'))

