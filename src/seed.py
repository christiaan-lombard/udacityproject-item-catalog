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
        title = 'Fancy Cat'
        # description = 'Dresscode = Fancy'
    )

    cat_artsy = Category.create(
        slug = 'artsy',
        title = 'Artsy Cat'
        # description = 'Leave your box at home. Think outside the scratchpost.'
    )

    cat_brainy = Category.create(
        slug = 'brainy',
        title = 'Brainy Cat'
        # description = 'Leave your box at home. Think outside the scratchpost.'
    )

    cat_brauny = Category.create(
        slug = 'brauny',
        title = 'Brauny Cat'
        # description = 'Leave your box at home. Think outside the scratchpost.'
    )

    Item.create(
        name='Starry Eyed Tie',
        picture='LINK:http://78.media.tumblr.com/tumblr_llz72e9zcQ1qjahcpo1_400.jpg',
        description='''
            Be interview ready with a fancy tie.
            Lorem ipsum dolor amet snackwave craft beer echo park pitchfork, YOLO microdosing health goth iPhone.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_fancy.slug,
    )

    Item.create(
        name='Blue Striped Tie',
        picture='LINK:http://78.media.tumblr.com/tumblr_m3pm42TBuR1qjahcpo1_500.jpg',
        description='''
            Take a break, throw out the picnic cloth, you are always ready wearing this blue striped tie.
            Blue bottle copper mug cloud bread, lyft synth sriracha 90's art party semiotics enamel pin slow-carb before they sold out cronut kale chips.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_fancy.slug,
    )

    Item.create(
        name='Light',
        picture='LINK:http://78.media.tumblr.com/tumblr_li3wtcrERj1qgnva2o1_500.jpg',
        description='''
            Beard ethical succulents, man braid cardigan schlitz air plant jianbing kitsch sustainable mlkshk pork belly.
            Fanny pack unicorn portland, live-edge before they sold out af flannel art party pour-over bicycle rights helvetica squid air plant taxidermy pok pok.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_artsy.slug,
    )

    Item.create(
        name='Whisker Cream',
        picture='LINK:http://78.media.tumblr.com/tumblr_m4i88dyXJE1rweruno1_1280.jpg',
        description='''
            Treat yourcatself.
            Intelligentsia salvia paleo wayfarers. Live-edge cliche occupy, iPhone umami flexitarian irony activated charcoal pork belly listicle pug man bun cloud bread affogato. Yuccie trust fund squid adaptogen yr.
        ''',
        user_id=user_snowball.id,
        category_slug=cat_fancy.slug,
    )

    Item.create(
        name='Golden Christmas Crown',
        picture='LINK:http://78.media.tumblr.com/tumblr_lwqd4rbkhg1r48fhjo1_500.jpg',
        description='''
            Santa Clausse of old.
        ''',
        user_id=user_snowball.id,
        category_slug=cat_artsy.slug,
    )

    Item.create(
        name='Piano Lessons',
        picture='LINK:http://25.media.tumblr.com/tumblr_l9be3aypTu1qcn249o1_500.gif',
        description='''
            Ramps mumblecore tacos viral. Pour-over actually brunch irony.
            Meggings biodiesel af copper mug vexillologist sartorial cardigan.
            Gentrify succulents snackwave pitchfork pork belly. Pop-up hell of
            raw denim trust fund keytar humblebrag echo park twee salvia yuccie
            ugh hot chicken.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_artsy.slug,
    )

    Item.create(
        name='Kittens for Dummies',
        picture='LINK:http://78.media.tumblr.com/tumblr_m1hn70ZQQx1qze0hyo1_1280.jpg',
        description='',
        user_id=user_snowball.id,
        category_slug=cat_brainy.slug,
    )

    Item.create(
        name='meh tumeric taiyaki',
        picture='LINK:http://25.media.tumblr.com/tumblr_latjtqu8wm1qbrje6o1_400.gif',
        description='',
        user_id=user_snowball.id,
        category_slug=cat_brauny.slug,
    )
    Item.create(
        name='Viral heirloom affogato',
        picture='LINK:http://25.media.tumblr.com/Jjkybd3nSdctvezhaYnbJk3h_500.jpg',
        description='',
        user_id=user_snowball.id,
        category_slug=cat_brauny.slug,
    )
    Item.create(
        name='Next level direct',
        picture='LINK:http://25.media.tumblr.com/tumblr_lvj7yiEMUO1qzpwi0o1_400.gif',
        description='''
            Letterpress williamsburg man bun pitchfork poutine taiyaki 
            chartreuse man braid activated charcoal humblebrag gastropub 
            hot chicken narwhal yuccie. Next level plaid shoreditch, chia 
            trust fund keffiyeh glossier skateboard irony chicharrones 
            pinterest sustainable craft beer pitchfork
        ''',
        user_id=user_snowball.id,
        category_slug=cat_brainy.slug,
    )

    Item.create(
        name='Selvage Affogato Stumptown',
        picture='LINK:http://24.media.tumblr.com/tumblr_lkurxzEBeG1qga5cqo1_500.jpg',
        description='''
            Brunch sriracha hot chicken, asymmetrical vaporware thundercats 
            enamel pin woke YOLO celiac. Hammock disrupt cronut swag PBR&B 
            master cleanse schlitz kitsch affogato tousled mixtape. 
            Seitan meditation disrupt retro jianbing.
        ''',
        user_id=user_snowball.id,
        category_slug=cat_brainy.slug,
    )

if __name__ == '__main__':
    init_db()
    seed()
