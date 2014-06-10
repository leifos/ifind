import os

def populate():
    janedoe = User.objects.create_user('janedoe', 'janedoe@test.com', '1234')
    johndoe = User.objects.create_user('johndoe', 'johndoe@test.com', '1234')

if __name__ == '__main__':
    print "Starting badsearch population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'badsearch_project.settings')
    from badsearch.models import User
    populate()
