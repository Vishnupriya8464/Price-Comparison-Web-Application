import sqlite3
from scripts import webscrapers as wb


conn = sqlite3.connect("db.sqlite3")
conn.row_factory = lambda c, row: row
c = conn.cursor()
c.execute("""SELECT url_snapdeal, url_amazon, url_flipkart
             FROM products_product""")
database_urls = c.fetchall()


for rows in database_urls:
    for url in rows:
        if "snapdeal.com" in url:
            snapdeal_price = wb.snapdeal_scrape(url)
            # print(snapdeal_price)
            c.execute("""UPDATE products_product
                         SET price_snapdeal=?
                         WHERE url_snapdeal=?""", (snapdeal_price, url))

        elif "amazon.co.uk" in url:
            amazon_price = wb.amazon_scrape(url)
            # print(amazon_price)
            c.execute("""UPDATE products_product
                         SET price_amazon = ?
                         WHERE url_amazon=?""", (amazon_price, url))

        elif "flipkart.com" in url:
            flipkart_price = wb.flipkart_scrape(url)
            # print(flipkart_price)
            c.execute("""UPDATE products_product
                         SET price_flipkart=?
                         WHERE url_flipkart=?""", (flipkart_price, url))

        else:
            print("FLAG: Is the following url correct? {}".format(url))

conn.commit()
c.close()
conn.close()
