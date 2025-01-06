import json
import io
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Dump data with specified encoding'

    def add_arguments(self, parser):
        parser.add_argument('output_file', type=str, help='The file to write the JSON data to')

    def handle(self, *args, **options):
        output_file = options['output_file']
        buffer = io.StringIO()
        
        # Dump the data to the in-memory buffer
        call_command('dumpdata', exclude=['contenttypes'], stdout=buffer)
        buffer.seek(0)
        
        # Load the data into a Python object
        data = json.load(buffer)

        # Write the data to a file with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
