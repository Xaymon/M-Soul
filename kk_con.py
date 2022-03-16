import psycopg2
class gobal:
        con = psycopg2.connect(host="150.95.90.124", database="kk_exchange",user="postgres", password="sml", port="5432")