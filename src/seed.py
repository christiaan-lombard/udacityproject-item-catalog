from models import User, Item, Category, init_db

def seed():
    user_jerry = User.make(email='jerry@mawhoo.com', name='Jerry Smith')
    user_jerry.set_password('secret')
    user_jerry.save()

    user_snowball = User.make(email='snowball@cmail.com', name='Snowball')
    user_snowball.set_password('secret')
    user_snowball.save()

    cat_fancy = Category.create(
        slug = 'fancy',
        title = 'Fancy Cat',
        description = 'Dresscode = Fancy'
    )

    cat_artsy = Category.create(
        slug = 'artsy',
        title = 'Artsy Cat',
        description = 'Leave your box at home. Think outside the scratchpost.'
    )

    cat_brainy = Category.create(
        slug = 'books',
        title = 'Brainy Cat',
        description = 'Leave your box at home. Think outside the scratchpost.'
    )

    Item.create(
        name='Starry Eyed Tie',
        picture='http://78.media.tumblr.com/tumblr_llz72e9zcQ1qjahcpo1_400.jpg',
        description='''
            Be interview ready with a fancy tie.
            Lorem ipsum dolor amet snackwave craft beer echo park pitchfork, YOLO microdosing health goth iPhone.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_fancy.slug,
    )

    Item.create(
        name='Blue Striped Tie',
        picture='http://78.media.tumblr.com/tumblr_m3pm42TBuR1qjahcpo1_500.jpg',
        description='''
            Take a break, throw out the picnic cloth, you are always ready wearing this blue striped tie.
            Blue bottle copper mug cloud bread, lyft synth sriracha 90's art party semiotics enamel pin slow-carb before they sold out cronut kale chips.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_fancy.slug,
    )

    Item.create(
        name='UV Light',
        picture='http://78.media.tumblr.com/tumblr_li3wtcrERj1qgnva2o1_500.jpg',
        description='''
            Beard ethical succulents, man braid cardigan schlitz air plant jianbing kitsch sustainable mlkshk pork belly.
            Fanny pack unicorn portland, live-edge before they sold out af flannel art party pour-over bicycle rights helvetica squid air plant taxidermy pok pok.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_artsy.slug,
    )

    Item.create(
        name='Whisker Cream',
        picture='http://78.media.tumblr.com/tumblr_m4i88dyXJE1rweruno1_1280.jpg',
        description='''
            Treat yourcatself.
            Intelligentsia salvia paleo wayfarers. Live-edge cliche occupy, iPhone umami flexitarian irony activated charcoal pork belly listicle pug man bun cloud bread affogato. Yuccie trust fund squid adaptogen yr.
        ''',
        user_id=user_snowball.id,
        category_slug=cat_artsy.slug,
    )

    Item.create(
        name='Golden Christmas Crown',
        picture='http://78.media.tumblr.com/tumblr_lwqd4rbkhg1r48fhjo1_500.jpg',
        description='''
            Santa Clausse of old.
        ''',
        user_id=user_snowball.id,
        category_slug=cat_artsy.slug,
    )

    Item.create(
        name='Kittens for Dummies',
        picture='http://78.media.tumblr.com/tumblr_m1hn70ZQQx1qze0hyo1_1280.jpg',
        description='',
        user_id=user_snowball.id,
        category_slug=cat_brainy.slug,
    )

if __name__ == '__main__':
    init_db()
    seed()
