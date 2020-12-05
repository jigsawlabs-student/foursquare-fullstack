import psycopg2
from src.orm import *
from src.db import *
from src import Category, Venue

conn = psycopg2.connect(database = 'foursquare_development', user = 'postgres', password = 'postgres')
cursor = conn.cursor()

drop_records(cursor, conn, 'venues')
drop_records(cursor, conn, 'categories')

famiglia = Venue(foursquare_id = '1234', name = 'La Famiglia', price = 1,
        rating = 2, likes = 3, menu_url = 'lafamig.com')
mogador = Venue(foursquare_id = '5678', name = 'Cafe Mogador', 
        price = 3, rating = 4, likes = 15, menu_url = 'cafemogador.com')
save(famiglia, conn, cursor)
save(mogador, conn, cursor)

pizza = Category(name = 'Pizza')
italian = Category(name = 'Italian')

save(pizza, conn, cursor)
save(italian, conn, cursor)
