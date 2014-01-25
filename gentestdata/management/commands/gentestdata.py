from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

def import_by_name(name):
    m = __import__(name)
    for n in name.split(".")[1:]:
        m = getattr(m, n)
    return m

class Command(BaseCommand):
    # TODO add args with app name?
    #args = '<poll_id poll_id ...>'
    #help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # get the list of installed apps
        apps = settings.INSTALLED_APPS

        for app_name in apps:
            self.generate_app(app_name)

    def generate_app(self, app_name):
        # import the app gentestdata module
        try:
            gentestdata = import_by_name(app_name+'.gentestdata')
            if hasattr(gentestdata, 'generate') and callable(gentestdata.generate):
                self.stdout.write('Generating test data for app "%s"' % app_name)
                gentestdata.generate()
        except ImportError:
            pass
