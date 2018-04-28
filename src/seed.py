#!/usr/bin/env python
from models import User, Item, Category, init_db

def seed():
    """Seed the DB with predefined cat-users, cat-agories and cat-items
    """

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
        category_slug=cat_fancy.slug,
    )
    Item.create(
        name='Kogi narwhal craft',
        picture='LINK:http://25.media.tumblr.com/tumblr_lnhra2RQmC1qevc73o1_1280.jpg',
        description='''
            Migas gochujang distillery tattooed farm-to-table narwhal truffaut lyft
            meggings flannel pork belly butcher. Thundercats slow-carb poutine try-hard.
            Cold-pressed man braid edison bulb roof party offal kinfolk narwhal chartreuse,
            next level pug food truck skateboard jean shorts swag. Kickstarter marfa actually
            VHS live-edge mlkshk wolf. Gochujang cliche normcore yr aesthetic humblebrag
            retro hammock man braid vape venmo. Tousled copper mug craft beer intelligentsia.
            Messenger bag hot chicken meggings, truffaut church-key fashion axe neutra.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_brauny.slug,
    )
    Item.create(
        name='Coloring book asymmetrical',
        picture='LINK:http://24.media.tumblr.com/tumblr_lt958lQcga1r4xjo2o1_1280.jpg',
        description='''
            Swag narwhal tumblr photo booth. Cliche jianbing snackwave portland vaporware,
            kitsch synth celiac meh iceland photo booth hammock lo-fi roof party.
            Vexillologist food truck PBR&B vape, gentrify meggings roof party bicycle
            rights semiotics raw denim jianbing. Readymade put a bird on it photo booth,
            gochujang biodiesel literally shabby chic keytar neutra vaporware ugh hella.
            Listicle banh mi meggings whatever, mlkshk actually gentrify synth intelligentsia.
             Letterpress raw denim shabby chic fam, you probably haven't heard of them jean
             shorts shaman asymmetrical hammock wayfarers. Yuccie small batch vegan synth,
             poke flexitarian photo booth pour-over pitchfork live-edge.
        ''',
        user_id=user_snowball.id,
        category_slug=cat_brainy.slug,
    )
    Item.create(
        name='Salvia butcher gluten-free',
        picture='LINK:http://25.media.tumblr.com/tumblr_m4fobvhr4i1qejbiro1_1280.jpg',
        description='''
        Mlkshk air plant ramps leggings man braid, etsy taxidermy post-ironic seitan
        brunch selvage edison bulb chillwave. Leggings venmo neutra everyday carry
        listicle live-edge fingerstache green juice. Tumeric venmo 90's, synth sriracha
        pug vape blue bottle raclette migas asymmetrical before they sold out.
        Tacos subway tile pop-up, yr etsy lumbersexual irony. Gastropub tacos twee
        succulents blue bottle cray celiac sriracha food truck woke kale chips messenger
         bag single-origin coffee.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_brauny.slug,
    )
    Item.create(
        name='Jean shorts banh mi',
        picture='LINK:http://25.media.tumblr.com/tumblr_lh0dcoubB21qgnva2o1_500.png',
        description='''
        Lorem ipsum dolor amet tousled heirloom trust fund lumbersexual literally
        leggings celiac kogi hell of semiotics messenger bag hammock green juice.
        Iceland vice retro chia sartorial green juice bitters direct trade blue
        bottle ugh polaroid meditation whatever kitsch literally. Crucifix tumeric
        normcore bespoke sartorial. Humblebrag VHS meditation, shabby chic cliche
        succulents intelligentsia poutine biodiesel street art yuccie truffaut tilde
        raclette. Single-origin coffee cray hashtag, narwhal locavore vape paleo
        marfa swag biodiesel sustainable ugh. Mixtape pug synth, normcore artisan
        kale chips mustache chillwave fingerstache asymmetrical microdosing
        truffaut butcher knausgaard. Iceland twee hot chicken farm-to-table
        waistcoat vaporware chicharrones leggings distillery
        hoodie single-origin coffee vice deep v.
        ''',
        user_id=user_snowball.id,
        category_slug=cat_artsy.slug,
    )
    Item.create(
        name='vape mlkshk',
        picture='LINK:http://24.media.tumblr.com/tumblr_m3pq1t1Wig1qh66wqo1_500.jpg',
        description='''
        Kogi narwhal craft beer tilde. Af +1 portland put a bird on it yr deep v echo
        park vice. Flannel plaid succulents organic selvage. Truffaut sustainable
        unicorn, palo santo vape biodiesel celiac salvia.
        ''',
        user_id=user_snowball.id,
        category_slug=cat_brainy.slug,
    )
    Item.create(
        name='Whatever kitsch adaptogen',
        picture='LINK:http://25.media.tumblr.com/tumblr_llr5t9Jyex1qze5g2o1_500.gif',
        description='''
        Coloring book asymmetrical leggings skateboard irony microdosing fanny pack,
        photo booth gastropub letterpress DIY +1 keytar stumptown synth. Disrupt
        snackwave PBR&B prism poutine lumbersexual actually waistcoat bushwick offal.
        La croix cliche waistcoat butcher vexillologist, yr retro meggings selvage
        intelligentsia hoodie pok pok af succulents art party. Franzen roof party
        coloring book, paleo bicycle rights microdosing selvage chillwave blog meh
        copper mug. Put a bird on it fingerstache activated charcoal try-hard disrupt
        trust fund readymade gluten-free. Drinking vinegar poke snackwave artisan marfa
        pug. Cold-pressed raclette mixtape, humblebrag kickstarter mlkshk chillwave
        iPhone tote bag +1 tbh keffiyeh banjo ennui kogi.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_fancy.slug,
    )
    Item.create(
        name='plaid flannel cronut hexagon',
        picture='LINK:http://26.media.tumblr.com/tumblr_lt8crjXgh11r4pd9wo1_1280.jpg',
        description='''
            Jean shorts banh mi pour-over seitan you probably haven't heard of them
            truffaut. Put a bird on it woke gluten-free, chartreuse etsy food truck
            church-key before they sold out whatever. Keffiyeh scenester squid,
            direct trade meh photo booth helvetica stumptown fanny pack. Scenester
            godard cred, glossier gentrify butcher church-key beard bitters shaman
            cornhole fam pour-over.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_brainy.slug,
    )
    Item.create(
        name='aesthetic prism truffaut',
        picture='LINK:http://25.media.tumblr.com/tumblr_m3pm3a0pl11qjahcpo1_1280.jpg',
        description='''
            Mlkshk air plant ramps leggings man braid, etsy taxidermy post-ironic
            seitan brunch selvage edison bulb chillwave. Leggings venmo neutra everyday
            carry listicle live-edge fingerstache green juice. Tumeric venmo 90's,
            synth sriracha pug vape blue bottle raclette migas asymmetrical before
            they sold out. Tacos subway tile pop-up, yr etsy lumbersexual irony.
            Gastropub tacos twee succulents blue bottle cray celiac sriracha food
            truck woke kale chips messenger bag single-origin coffee.
        ''',
        user_id=user_jerry.id,
        category_slug=cat_fancy.slug,
    )

if __name__ == '__main__':
    init_db()
    seed()
