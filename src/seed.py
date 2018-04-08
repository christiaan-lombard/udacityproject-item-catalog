from models import User, Item, Category, init_db

def seed():
    user_jerry = User.make(email='jerry@yahoo.com', name='Jerry Smith')
    user_jerry.set_password('secret')
    user_jerry.save()
    print('Added user %s' % user_jerry)

if __name__ == '__main__':
    init_db()
    seed()
