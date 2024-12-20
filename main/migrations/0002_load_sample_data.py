from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

def load_sample_data(apps, schema_editor):
    Restaurant = apps.get_model('main', 'Restaurant')
    Food = apps.get_model('main', 'Food')

    # Create Restaurants
    ya_mbok = Restaurant.objects.create(name="Ya'mbok, Jatimelati", location="jakarta")
    michelle_bakery = Restaurant.objects.create(name="Michelle Bakery, Cimanggis", location="jakarta")
    kaka_udon = Restaurant.objects.create(name="Kaka Udon", location="jakarta")
    mc_donalds_panjang = Restaurant.objects.create(name="McDonald's, Panjang", location="jakarta")
    tokyo_town_cafe = Restaurant.objects.create(name="Tokyo Town Cafe", location="jakarta")
    lawson_cempaka_mas = Restaurant.objects.create(name="Lawson, Cempaka Mas", location="jakarta")
    familymart_sequis_tower = Restaurant.objects.create(name="FamilyMart, Sequis Tower", location="jakarta")
    kopi_nako_ciracas = Restaurant.objects.create(name="Kopi Nako Ciracas", location="jakarta")
    hey_kafe_cipondoh = Restaurant.objects.create(name="Hey Kafe, Cipondoh", location="jakarta")
    xiboba_ramayana_parung = Restaurant.objects.create(name="XIBOBA, Ramayana Parung", location="jakarta")
    cake_pandeglang_cake = Restaurant.objects.create(name="Cake Pandeglang Cake", location="jakarta")
    lawson_akses_ui = Restaurant.objects.create(name="Lawson, Akses UI", location="jakarta")
    ramen_giant_bogor = Restaurant.objects.create(name="Ramen Giant, Bogor", location="jakarta")
    fore_coffee_jatiwaringin = Restaurant.objects.create(name="Fore Coffee, Jatiwaringin", location="jakarta")
    mc_donalds_pekayon = Restaurant.objects.create(name="McDonald's, Pekayon", location="jakarta")
    chateraise_senayan_city = Restaurant.objects.create(name="Chateraise, Senayan City", location="jakarta")
    markobar_duren_sawit = Restaurant.objects.create(name="Markobar, Duren Sawit", location="jakarta")
    dapur_cokelat_depok = Restaurant.objects.create(name="Dapur Cokelat, Depok", location="jakarta")
    keikpop_harapan_indah = Restaurant.objects.create(name="Keikpop, Harapan Indah", location="jakarta")
    hedon_cafe_sukatani = Restaurant.objects.create(name="Hedon Cafe, Sukatani", location="jakarta")
    mc_donalds_tambak = Restaurant.objects.create(name="McDonald's, Tambak", location="jakarta")
    kemek_nyok = Restaurant.objects.create(name="Kemek Nyok", location="jakarta")
    cafe_otss = Restaurant.objects.create(name="Cafe OTSS", location="jakarta")
    mc_donalds_jatiwarna = Restaurant.objects.create(name="McDonald's, Jatiwarna", location="jakarta")
    lepas_kopi = Restaurant.objects.create(name="LEPAS KOPI", location="jakarta")
    bunga_bakery_depok = Restaurant.objects.create(name="Bunga Bakery, Depok", location="jakarta")
    menantea_pemda_cibinong = Restaurant.objects.create(name="Menantea, Pemda Cibinong", location="jakarta")
    cimory_condet_balekambang = Restaurant.objects.create(name="Cimory Condet, Balekambang", location="jakarta")
    lawson_sunter_kirana = Restaurant.objects.create(name="Lawson, Sunter Kirana", location="jakarta")
    sumoyaki_pademangan = Restaurant.objects.create(name="SUMOYAKI, PADEMANGAN", location="jakarta")
    burger_bros_bintaro = Restaurant.objects.create(name="Burger Bros, Bintaro", location="jakarta")
    faasos_blok_m = Restaurant.objects.create(name="Faasos, Blok M", location="jakarta")
    mokat_megamendung = Restaurant.objects.create(name="Mokat, Megamendung", location="jakarta")
    kebab_bosman_ciputat = Restaurant.objects.create(name="Kebab Bosman, Ciputat", location="jakarta")
    gelato_house_cafe = Restaurant.objects.create(name="Gelato House Cafe ", location="jakarta")
    keikpop_pajajaran_bogor = Restaurant.objects.create(name="Keikpop, Pajajaran Bogor", location="jakarta")
    keikpop_mangga_besar = Restaurant.objects.create(name="Keikpop, Mangga Besar", location="jakarta")
    mab_toppoki_jengki = Restaurant.objects.create(name="MAB Toppoki, Jengki", location="jakarta")
    warung_corndog_sukaraja = Restaurant.objects.create(name="Warung Corndog, Sukaraja", location="jakarta")
    martabak_acc = Restaurant.objects.create(name="Martabak Acc", location="jakarta")
    kancha_duri_kosambi = Restaurant.objects.create(name="Kancha, Duri Kosambi", location="jakarta")
    dapur_cokelat_cibubur = Restaurant.objects.create(name="Dapur Cokelat, Cibubur", location="jakarta")
    burger_naura = Restaurant.objects.create(name="Burger Naura", location="jakarta")
    geprek_bensu_karawang = Restaurant.objects.create(name="Geprek Bensu, Karawang", location="jakarta")
    mixue_harapan_indah = Restaurant.objects.create(name="Mixue, Harapan Indah", location="jakarta")
    lawson_uin_kertamukti = Restaurant.objects.create(name="Lawson, UIN Kertamukti", location="jakarta")
    takana_coffee_rawamangun = Restaurant.objects.create(name="Takana Coffee, Rawamangun", location="jakarta")
    kebab_bosman_gandul = Restaurant.objects.create(name="Kebab Bosman, Gandul", location="jakarta")
    resto_ayam_najeb = Restaurant.objects.create(name="Resto Ayam Najeb", location="jakarta")
    emados_shawarma_condet = Restaurant.objects.create(name="Emados Shawarma, Condet", location="jakarta")
    starbucks_sudirman_bogor = Restaurant.objects.create(name="Starbucks, Sudirman Bogor", location="jakarta")
    lawson_percetakan_negara = Restaurant.objects.create(name="Lawson, Percetakan Negara", location="jakarta")
    gosteak_tj_priok = Restaurant.objects.create(name="GoSteak, Tj Priok", location="jakarta")
    pancong_pijay = Restaurant.objects.create(name="Pancong Pijay", location="jakarta")
    kopinya_kimboo = Restaurant.objects.create(name="KOPINYA KIMBOO", location="jakarta")
    lawless_capsule_cibubur = Restaurant.objects.create(name="Lawless, Capsule Cibubur", location="jakarta")
    moeda_coffee = Restaurant.objects.create(name="Moeda Coffee", location="jakarta")
    bakso_titoti_parung = Restaurant.objects.create(name="Bakso Titoti, Parung", location="jakarta")
    pita_cappucino_cincau = Restaurant.objects.create(name="Pita Cappucino Cincau", location="jakarta")
    mad_bagel_bsd = Restaurant.objects.create(name="Mad Bagel, BSD", location="jakarta")
    toko_pizza_limo = Restaurant.objects.create(name="Toko Pizza, Limo", location="jakarta")
    genkaya_pabuaran = Restaurant.objects.create(name="Genkaya, Pabuaran", location="jakarta")
    traffic_bun_benhil = Restaurant.objects.create(name="Traffic Bun, Benhil", location="jakarta")
    faasos_bintaro = Restaurant.objects.create(name="Faasos, Bintaro", location="jakarta")
    emados_shawarma_depok = Restaurant.objects.create(name="Emados Shawarma, Depok", location="jakarta")
    abuba_steak_cikarang = Restaurant.objects.create(name="Abuba Steak, Cikarang", location="jakarta")
    martabak_mapingkot = Restaurant.objects.create(name="martabak mapingkot", location="jakarta")
    kopi_330_ciledug = Restaurant.objects.create(name="330 Kopi, Ciledug", location="jakarta")
    bunga_bakery_cibinong = Restaurant.objects.create(name="Bunga Bakery, Cibinong", location="jakarta")
    mixue_benhil = Restaurant.objects.create(name="Mixue, Benhil", location="jakarta")
    lawson_syahdan = Restaurant.objects.create(name="Lawson, Syahdan", location="jakarta")
    jack_donut = Restaurant.objects.create(name="JACK DONUT", location="jakarta")
    farm_girl_scbd = Restaurant.objects.create(name="farm.girl, SCBD", location="jakarta")
    kims_topokki_bintara = Restaurant.objects.create(name="Kims Topokki, Bintara", location="jakarta")
    guree_senopati = Restaurant.objects.create(name="GUREE, Senopati", location="jakarta")
    dapur_cokelat_ciracas = Restaurant.objects.create(name="Dapur Cokelat, Ciracas", location="jakarta")

    # Create Foods
    Food.objects.create(name="Punch Yambok", category="Ayam & bebek", price=26000, restaurant=ya_mbok)
    Food.objects.create(name="Choco Cheese Loaf", category="Roti", price=40000, restaurant=michelle_bakery)
    Food.objects.create(name="Chicken Katsu Curry Rice", category="Bakmie/Cepat saji/Jepang", price=30000, restaurant=kaka_udon)
    Food.objects.create(name="Double Cheese Burger", category="Sweets/Jajanan/Cepat saji", price=36000, restaurant=mc_donalds_panjang)
    Food.objects.create(name="Kabuki Taro Latte ( Ice )", category="Kopi/Minuman/Jepang", price=23000, restaurant=tokyo_town_cafe)
    Food.objects.create(name="Cheese Dumpling", category="Jepang/Jajanan/Aneka nasi/Minuman", price=9000, restaurant=lawson_cempaka_mas)
    Food.objects.create(name="Ice Grass Jelly Classic Milk Tea", category="Kopi/Jajanan/Aneka nasi/Minuman/Ayam & bebek", price=16000, restaurant=familymart_sequis_tower)
    Food.objects.create(name="Es Kopi Sayang", category="Aneka nasi/Kopi/Minuman", price=25000, restaurant=kopi_nako_ciracas)
    Food.objects.create(name="Ice Cendol", category="Minuman", price=19000, restaurant=hey_kafe_cipondoh)
    Food.objects.create(name="Brown Sugar Boba Milk Tea", category="Minuman", price=21000, restaurant=xiboba_ramayana_parung)
    Food.objects.create(name="BF Bulat Ukir Tayo Uk15cm", category="Roti", price=95000, restaurant=cake_pandeglang_cake)
    Food.objects.create(name="You C1000 Lemon Water Pet 500Ml", category="Jajanan/Aneka nasi/Minuman/Jepang", price=11000, restaurant=lawson_akses_ui)
    Food.objects.create(name="Tebasaki Ramen", category="Jepang/Cepat saji/Aneka nasi", price=25400, restaurant=ramen_giant_bogor)
    Food.objects.create(name="Americano (Iced)", category="Kopi/Minuman/Cepat saji", price=19000, restaurant=fore_coffee_jatiwaringin)
    Food.objects.create(name="PaHeBat Cheeseburger, Medium", category="Cepat saji/Sweets/Jajanan", price=39000, restaurant=mc_donalds_pekayon)
    Food.objects.create(name="Longevity Ring M", category="Jajanan/Kopi", price=600000, restaurant=chateraise_senayan_city)
    Food.objects.create(name="Lipat Pocky strawbery Full Toping", category="Martabak", price=55000, restaurant=markobar_duren_sawit)
    Food.objects.create(name="Pudding Cheese Cake", category="Sweets", price=100000, restaurant=dapur_cokelat_depok)
    Food.objects.create(name="Icakewon Class", category="Sweets/Roti", price=65000, restaurant=keikpop_harapan_indah)
    Food.objects.create(name="sate sinchan", category="Ayam & bebek/Jajanan/Minuman", price=12000, restaurant=hedon_cafe_sukatani)
    Food.objects.create(name="Oreo Sw Vanilla 137G", category="Aneka nasi/Minuman/Jepang/Jajanan", price=8000, restaurant=lawson_cempaka_mas)
    Food.objects.create(name="McSpicy", category="Cepat saji/Sweets/Jajanan", price=38000, restaurant=mc_donalds_tambak)
    Food.objects.create(name="Shrimp Roll Bento (Udang)", category="Barat/Jajanan/Ayam & bebek", price=19000, restaurant=kemek_nyok)
    Food.objects.create(name="CHOCO MEET VANILLA", category="Cepat saji/Kopi/Aneka nasi", price=45000, restaurant=cafe_otss)
    Food.objects.create(name="Fish Snack Wrap", category="Cepat saji/Sweets/Jajanan", price=16500, restaurant=mc_donalds_jatiwarna)
    Food.objects.create(name="Pisang Bakar Coklat Keju", category="Aneka nasi/Jajanan/Kopi", price=20000, restaurant=lepas_kopi)
    Food.objects.create(name="Roti Abon Sapi", category="Roti", price=11500, restaurant=bunga_bakery_depok)
    Food.objects.create(name="Smoked Beef Cheese Sandwich+Ice Java Mocha Latte", category="Aneka nasi/Minuman/Jepang/Jajanan", price=42000, restaurant=lawson_cempaka_mas)
    Food.objects.create(name="Potato and Chicken with Honey Mustard", category="Minuman", price=31000, restaurant=menantea_pemda_cibinong)
    Food.objects.create(name="Family Time Berempat Happy Meal Beef Burger", category="Cepat saji/Sweets/Jajanan", price=130000, restaurant=mc_donalds_panjang)
    Food.objects.create(name="Susu Cimory Fresh Milk 950 ML Cofee Late", category="Minuman/Jajanan/Sweets", price=25000, restaurant=cimory_condet_balekambang)
    Food.objects.create(name="SAUSAGE ROLL", category="Jajanan/Aneka nasi/Minuman/Jepang", price=9000, restaurant=lawson_sunter_kirana)
    Food.objects.create(name="COMBO 2 TISAI", category="Jajanan/Jepang/Martabak", price=32000, restaurant=sumoyaki_pademangan)
    Food.objects.create(name="Tiramisu Cheesecake", category="Ayam & bebek/Jajanan/Barat/Cepat saji", price=46000, restaurant=burger_bros_bintaro)
    Food.objects.create(name="Cheesy Beef Overload Wrap", category="Cepat saji/India/Jajanan/Timur Tengah/Aneka nasi", price=59990, restaurant=faasos_blok_m)
    Food.objects.create(name="Choco Boba Crunch", category="Minuman", price=23000, restaurant=mokat_megamendung)
    Food.objects.create(name="Special Canai Kebab + Rujak Cireng Mini", category="Jajanan", price=27000, restaurant=kebab_bosman_ciputat)
    Food.objects.create(name="6pc Frozen Martabak Telur", category="Aneka nasi/Minuman/Jepang/Jajanan", price=48000, restaurant=lawson_cempaka_mas)
    Food.objects.create(name="Mojito Lychee", category="Minuman/Sweets/Cepat saji", price=30000, restaurant=gelato_house_cafe)
    Food.objects.create(name="Pomegranate Fizz", category="Cepat saji/Sweets/Jajanan", price=17000, restaurant=mc_donalds_pekayon)
    Food.objects.create(name="White Choco Strawberry Pastry Pie", category="Sweets/Jajanan/Cepat saji", price=15500, restaurant=mc_donalds_panjang)
    Food.objects.create(name="Split Cake", category="Roti/Sweets", price=75000, restaurant=keikpop_pajajaran_bogor)
    Food.objects.create(name="Bf Ukir Doraemon Uk15cm", category="Roti", price=95000, restaurant=cake_pandeglang_cake)
    Food.objects.create(name="Twincenzo", category="Sweets/Roti", price=75000, restaurant=keikpop_mangga_besar)
    Food.objects.create(name="Rhabokki Odeng", category="Jepang/Jajanan", price=25500, restaurant=mab_toppoki_jengki)
    Food.objects.create(name="Biscuit Choco", category="Sweets", price=33000, restaurant=dapur_cokelat_depok)
    Food.objects.create(name="Corn Dog Mozarella Cappucinno", category="Cepat saji/Korea/Jajanan", price=15000, restaurant=warung_corndog_sukaraja)
    Food.objects.create(name="Beng-Beng Coklat 22G", category="Aneka nasi/Minuman/Jepang/Jajanan", price=3500, restaurant=lawson_cempaka_mas)
    Food.objects.create(name="Martabak Keju Kacang Coklat Wijen Susu", category="Martabak/Roti/Sweets", price=55000, restaurant=martabak_acc)
    Food.objects.create(name="Sparkling Tropical Fruit Regular", category="Minuman", price=19000, restaurant=kancha_duri_kosambi)
    Food.objects.create(name="Caramel Chocolate", category="Sweets", price=203000, restaurant=dapur_cokelat_cibubur)
    Food.objects.create(name="Paket Kluarga", category="Jajanan/Cepat saji/Bakso & soto", price=40000, restaurant=burger_naura)
    Food.objects.create(name="Alacarte Geprek Bensu Sambal Original", category="Ayam & bebek", price=19250, restaurant=geprek_bensu_karawang)
    Food.objects.create(name="Bf Kotak Coklat Tempel Uk15cm", category="Roti", price=100000, restaurant=cake_pandeglang_cake)
    Food.objects.create(name="Signature Dalgona Boba", category="Minuman", price=22000, restaurant=xiboba_ramayana_parung)
    Food.objects.create(name="Lemon Earl Grey Tea", category="Minuman/Jajanan", price=14000, restaurant=mixue_harapan_indah)
    Food.objects.create(name="Original Ena Chike+Ichi Ocha Teh Melati/Frestea Jasmin Pet 350ml", category="Jajanan/Aneka nasi/Minuman/Jepang", price=28500, restaurant=lawson_sunter_kirana)
    Food.objects.create(name="Siomay Rolled", category="Aneka nasi/Minuman/Jepang/Jajanan", price=8000, restaurant=lawson_uin_kertamukti)
    Food.objects.create(name="Peach Tea", category="Minuman/Roti/Kopi", price=20000, restaurant=takana_coffee_rawamangun)
    Food.objects.create(name="Black Kebab Jumbo", category="Jajanan/Barat", price=28000, restaurant=kebab_bosman_gandul)
    Food.objects.create(name="Sate Ampela", category="Ayam & bebek/Cepat saji/Sate", price=4000, restaurant=resto_ayam_najeb)
    Food.objects.create(name="Fanta Float", category="Sweets/Jajanan/Cepat saji", price=13000, restaurant=mc_donalds_panjang)
    Food.objects.create(name="Setengah Ayam Guling Nasi Mandhi", category="Ayam & bebek/Timur Tengah", price=70180, restaurant=emados_shawarma_condet)
    Food.objects.create(name="Pizza Pie", category="Cepat saji/Sweets/Jajanan", price=15000, restaurant=mc_donalds_panjang)
    Food.objects.create(name="Sinde Lrtn Pet 500Ml", category="Aneka nasi/Minuman/Jepang/Jajanan", price=10000, restaurant=lawson_uin_kertamukti)
    Food.objects.create(name="LUNCH ( Selected food + Iced Shaken Lemonade/Americano/ Latte, tall size)", category="Kopi/Roti/Minuman", price=98000, restaurant=starbucks_sudirman_bogor)
    Food.objects.create(name="Lilin Angka 2", category="Roti", price=3800, restaurant=cake_pandeglang_cake)
    Food.objects.create(name="Chic Choc 55G", category="Jepang/Jajanan/Aneka nasi/Minuman", price=9500, restaurant=lawson_percetakan_negara)
    Food.objects.create(name="Gongso Ayam", category="Aneka nasi/Bakmie/Barat", price=27500, restaurant=gosteak_tj_priok)
    Food.objects.create(name="Ropang Greentea Susu", category="Minuman/Roti/Kopi", price=13000, restaurant=pancong_pijay)
    Food.objects.create(name="Lychee Yakult", category="Minuman/Kopi", price=15500, restaurant=kopinya_kimboo)
    Food.objects.create(name="Pickels", category="Barat", price=21000, restaurant=lawless_capsule_cibubur)
    Food.objects.create(name="Vanilla Latte Ice", category="Kopi/Minuman/Sweets", price=30000, restaurant=moeda_coffee)
    Food.objects.create(name="Mie Ayam Pangsit + Urat Besar", category="Bakso & soto/Minuman", price=39000, restaurant=bakso_titoti_parung)
    Food.objects.create(name="McFlurry Choco", category="Cepat saji/Sweets/Jajanan", price=12500, restaurant=mc_donalds_tambak)
    Food.objects.create(name="Cokelat Wijen Susu", category="Martabak/Roti/Sweets", price=42000, restaurant=martabak_acc)
    Food.objects.create(name="Crunchy Signature Kakao", category="Minuman", price=21000, restaurant=xiboba_ramayana_parung)
    Food.objects.create(name="Creamy Cendol Frappe", category="Jajanan/Barat/Cepat saji/Ayam & bebek", price=36990, restaurant=burger_bros_bintaro)
    Food.objects.create(name="ES BOBA VANILLA BLUE", category="Cepat saji/Jajanan/Minuman", price=10000, restaurant=pita_cappucino_cincau)
    Food.objects.create(name="Chicken Mozarella", category="Barat/Roti", price=66000, restaurant=mad_bagel_bsd)
    Food.objects.create(name="Extra Mushroom Champignon", category="Pizza & pasta", price=13000, restaurant=toko_pizza_limo)
    Food.objects.create(name="PaMer 5 Mix Medium", category="Cepat saji/Sweets/Jajanan", price=111000, restaurant=mc_donalds_pekayon)
    Food.objects.create(name="Dumpling Mix", category="Korea/Minuman/Jajanan", price=15000, restaurant=genkaya_pabuaran)
    Food.objects.create(name="Cheese Stick", category="Roti", price=31500, restaurant=bunga_bakery_depok)
    Food.objects.create(name="Double Sei Diego Burger + Traffic French Fries + Cola", category="Barat", price=92000, restaurant=traffic_bun_benhil)
    Food.objects.create(name="2x Pizza Pie", category="Sweets/Jajanan/Cepat saji", price=26000, restaurant=mc_donalds_panjang)
    Food.objects.create(name="Mixed Kebab Meal", category="India/Jajanan/Timur Tengah", price=84970, restaurant=faasos_bintaro)
    Food.objects.create(name="Setengah Ayam Guling Nasi Mandhi", category="Ayam & bebek/Timur Tengah", price=70180, restaurant=emados_shawarma_depok)
    Food.objects.create(name="Ice Matcha Latte", category="Aneka nasi/Minuman/Jepang/Jajanan", price=18000, restaurant=lawson_uin_kertamukti)
    Food.objects.create(name="The Passion", category="Barat", price=33000, restaurant=abuba_steak_cikarang)
    Food.objects.create(name="double coklat susu", category="Martabak", price=26950, restaurant=martabak_mapingkot)
    Food.objects.create(name="Paket Beff Blackpaper", category="Kopi/Minuman/Roti", price=37000, restaurant=kopi_330_ciledug)
    Food.objects.create(name="Red Velvet 11", category="Roti", price=56500, restaurant=bunga_bakery_cibinong)
    Food.objects.create(name="Milk Tea with 2 Topping (Medium)", category="Minuman/Sweets", price=21000, restaurant=mixue_benhil)
    Food.objects.create(name="Hot Kopi Susu Arabica Gayo", category="Minuman/Jepang/Jajanan/Aneka nasi", price=18000, restaurant=lawson_syahdan)
    Food.objects.create(name="Oreo", category="Roti/Jajanan", price=4000, restaurant=jack_donut)
    Food.objects.create(name="Extra Kalamata Olives", category="Sweets/Kopi/Barat", price=36000, restaurant=farm_girl_scbd)
    Food.objects.create(name="Rabokki Original", category="Korea", price=20000, restaurant=kims_topokki_bintara)
    Food.objects.create(name="Sambal Matah", category="Aneka nasi/Ayam & bebek/Barat", price=7000, restaurant=guree_senopati)
    Food.objects.create(name="Grape Pebbles", category="Minuman/Sweets/Roti", price=30000, restaurant=dapur_cokelat_ciracas)

    # Create Admin User
    User = apps.get_model('auth', 'User')
    Admin = apps.get_model('main', 'Admin')
    
    admin_username = "admin"
    admin_password = make_password("admin123")
    admin_email = "admin@gmail.com"
    
    admin_user = User.objects.create(
        username=admin_username,
        email=admin_email,
        password=admin_password
    )
    
    Admin.objects.create(user=admin_user)

    # Create Client User
    Client = apps.get_model('main', 'Client')
    
    client_username = "client"
    client_password = make_password("client123")
    client_email = "client@gmail.com"
    
    client_user = User.objects.create(
        username=client_username,
        email=client_email,
        password=client_password
    )
    
    Client.objects.create(user=client_user)

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_sample_data),
    ]