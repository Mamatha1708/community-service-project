from models import db, User, Product, Order, OrderItem

def seed_database():
    """Seed initial demo users, realistic Kalamkari products, and orders."""
    # Check if admin already exists
    if User.query.filter_by(username='admin').first():
        return

    print("Seeding database with realistic Kalamkari artisan data...")

    # 1. Create Users
    admin = User(
        username='admin',
        email='admin@kalamkari.org',
        full_name='CSP Project Coordinator (Admin)',
        role='admin',
        phone='+91 98765 43210',
        bio='Community Service Project Administrator supervising artisan welfare and portal management.'
    )
    admin.set_password('admin123')

    artisan1 = User(
        username='ramana_artisan',
        email='artisan@kalamkari.org',
        full_name='Master S. Ramanaiah',
        role='artisan',
        phone='+91 94401 23456',
        artisan_cluster='Srikalahasti, Tirupati District',
        experience_years=28,
        bio='3rd-generation Kalamkari master craftsperson. Specializes in bamboo kalam freehand drawings of Tree of Life and sacred temple epics using pure vegetable dyes.'
    )
    artisan1.set_password('artisan123')

    artisan2 = User(
        username='lakshmi_crafts',
        email='lakshmi@kalamkari.org',
        full_name='Smt. Lakshmi Devi',
        role='artisan',
        phone='+91 98480 87654',
        artisan_cluster='Pedana, Machilipatnam',
        experience_years=16,
        bio='Preserving Machilipatnam GI block-printing heritage. Expert in hand-carved teakwood relief impressions and natural indigo vat fermentation.'
    )
    artisan2.set_password('lakshmi123')

    customer1 = User(
        username='ananya_buyer',
        email='customer@kalamkari.org',
        full_name='Ananya Sharma',
        role='customer',
        phone='+91 99887 76655',
        bio='Handloom revival supporter, architecture enthusiast, and conscious art collector.'
    )
    customer1.set_password('customer123')

    db.session.add_all([admin, artisan1, artisan2, customer1])
    db.session.commit()

    # 2. Create Realistic Kalamkari Products
    products = [
        Product(
            artisan_id=artisan1.id,
            title='Hand-Painted Tree of Life Sacred Wall Tapestry',
            kalamkari_style='Srikalahasti Pen Kalamkari',
            category='Wall Hangings & Scrolls',
            motif_type='Tree of Life',
            natural_dyes='Kasinam (fermented iron rust), Myrobalan milk, Madder root boiling, Natural Indigo',
            description=(
                'An exquisite masterwork hand-drawn with bamboo pens (toda kalam) on milk-scoured organic cotton. '
                'The sprawling branches symbolize the universal cosmic connection, sheltering singing peacocks and deer. '
                'Drawn over 22 days and cured in the holy Swarnamukhi river waters.'
            ),
            price=4850.0,
            stock=4,
            image_url='/static/images/samples/tree_of_life.svg'
        ),
        Product(
            artisan_id=artisan1.id,
            title='Dancing Peacock Pure Tussar Silk Saree',
            kalamkari_style='Srikalahasti Pen Kalamkari',
            category='Sarees',
            motif_type='Peacock & Swan',
            natural_dyes='Pomegranate rind yellow, Indigo leaf vat extract, Alum mordant, Kasinam black',
            description=(
                'Pure handloom Tussar silk saree featuring regal dancing peacock pallu motifs. '
                'Each feather is meticulously outlined with charcoal tamarind pens and filled with plant-derived jewel tones. '
                'Includes unstitched designer blouse piece with ornate border work.'
            ),
            price=8200.0,
            stock=3,
            image_url='/static/images/samples/peacock_saree.svg'
        ),
        Product(
            artisan_id=artisan2.id,
            title='Machilipatnam Botanical Paisley Block-Printed Dupatta',
            kalamkari_style='Machilipatnam Block Kalamkari',
            category='Dupattas & Shawls',
            motif_type='Floral & Paisley',
            natural_dyes='Pure fermented Indigo, Madder root, Myrobalan flower tannin',
            description=(
                'Feather-light Chanderi cotton-silk dupatta stamped with antique teakwood blocks dating back over 80 years. '
                'Flowing Mankolam (paisley) and leafy vine borders washed in Krishna river delta currents for sublime softness.'
            ),
            price=1650.0,
            stock=8,
            image_url='/static/images/samples/paisley_dupatta.svg'
        ),
        Product(
            artisan_id=artisan1.id,
            title='Ramayana Epic Sita Swayamvar Hand-Drawn Scroll',
            kalamkari_style='Srikalahasti Pen Kalamkari',
            category='Wall Hangings & Scrolls',
            motif_type='Mythological & Epics',
            natural_dyes='Fermented Kasinam, Madder red, Turmeric yellow, Buffalo milk resist',
            description=(
                'Museum-quality narrative wall scroll capturing the celestial moment of Lord Rama stringing the Shiva Dhanush. '
                'Created strictly following traditional temple mural proportions with descriptive Telugu calligraphy inscriptions.'
            ),
            price=9500.0,
            stock=2,
            image_url='/static/images/samples/ramayana_scroll.svg'
        ),
        Product(
            artisan_id=artisan2.id,
            title='Royal Lotus & Elephant Organic Cotton Table Runner',
            kalamkari_style='Machilipatnam Block Kalamkari',
            category='Home Decor',
            motif_type='Lotus & Elephants',
            natural_dyes='Natural Indigo, Chayroot madder, Alum paste, Kasim iron slag',
            description=(
                'Heavyweight handspun organic cotton table runner featuring ceremonial royal elephants walking beside blooming lotuses. '
                'Adds rustic warmth and authentic Indian craft character to your dining table or console.'
            ),
            price=1250.0,
            stock=12,
            image_url='/static/images/samples/elephant_runner.svg'
        ),
        Product(
            artisan_id=artisan2.id,
            title='Pedana Heritage Floral Indigo Dress Fabric (3 Meters)',
            kalamkari_style='Machilipatnam Block Kalamkari',
            category='Fabrics',
            motif_type='Floral & Paisley',
            natural_dyes='Cold-vat fermented Natural Indigo, Myrobalan yellow',
            description=(
                'Pure 60s count breathable cotton yardage adorned with miniature Mughal floral jaal block prints. '
                'Skin-friendly, completely free of chemical azo dyes, ideal for custom kurtas, tops, or ceremonial shirts.'
            ),
            price=1890.0,
            stock=6,
            image_url='/static/images/samples/indigo_fabric.svg'
        )
    ]

    db.session.add_all(products)
    db.session.commit()

    # 3. Create Sample Demo Order for demonstration
    sample_order = Order(
        order_number='KC-2026-1001',
        user_id=customer1.id,
        full_name='Ananya Sharma',
        email='customer@kalamkari.org',
        phone='+91 99887 76655',
        shipping_address='Flat 402, Kaveri Heritage Apartments, MG Road',
        city='Vijayawada',
        pincode='520010',
        payment_method='Cash on Delivery (Demo)',
        total_amount=4850.0,
        status='Processing'
    )
    db.session.add(sample_order)
    db.session.commit()

    order_item = OrderItem(
        order_id=sample_order.id,
        product_id=products[0].id,
        artisan_id=artisan1.id,
        product_title=products[0].title,
        price_at_purchase=4850.0,
        quantity=1
    )
    db.session.add(order_item)
    db.session.commit()

    print("Database successfully seeded with realistic sample data!")
