from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
def get_price(price_of_product):
    temp = ''
    found = False
    for c in price_of_product:
        try:
            int(c)
            temp += c
            found = True
        except:
            if c != ',' and found:
                break
    return temp



def scrape_olizstore(search_query):
    results = []

    try:
        print("olizstore called")

        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        url = "https://www.olizstore.com/catalogsearch/result/?q=" + search_query
        driver.get(url)
        time.sleep(2)

        page_html = driver.page_source
        driver.quit()
        time.sleep(5)

        page_soup = soup(page_html, "html.parser")
        matching_li_elements = page_soup.select('div#layer-product-list div.search.results div.products.wrapper.grid.columns4.products-grid li.item')

        time.sleep(5)
        # print(matching_li_elements)


        for container in matching_li_elements:
            # print(container)
            title_of_product = container.find("a", class_="product-item-link").text
            price_of_product = container.find("span", class_="price")
            if price_of_product:
                # print("price", price_of_product.text)
                price_of_product = get_price(price_of_product)

            else:
                price_of_product=0
                # print("no price")

            image_of_product = container.find("div", {"class": "product-item-photo"}).a.img['src']
            link_of_product = container.find("div", {"class": "product-item-photo"}).a['href']

            if price_of_product != '0':
                results.append({
                    "title": title_of_product,
                    "price": price_of_product,
                    "image": image_of_product,
                    "link": link_of_product,
                    "site": "https://www.olizstore.com/pub/media/porto/sticky_logo/default/olizLogo.png"
                })
    except Exception as e:
        print(f"Error at Olizstore: {e}")

    return results

def scrape_sastodeal(search_query):
    results = []

    try:
        print("sastodeal called")

        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://www.sastodeal.com/catalogsearch/result/?q={search_query}")

        content = driver.page_source
        soup_bs=soup(content, 'html.parser')
        product_divs = soup_bs.select('div.products ol.filterproducts li.item')

        for div in product_divs:
            title_of_product = div.select_one('a.product-item-link').text
            link_of_product = div.select_one('.product-item-name a').attrs.get('href')
            price_of_product = div.select_one('span.price').text
            image_of_product = div.select_one('span.product-image-wrapper img').attrs.get('src')

            results.append({
                'title': title_of_product,
                'price': price_of_product,
                'image': image_of_product,
                'link': link_of_product,
                'site': 'Sastodeal'
            })

        driver.quit()
    except Exception as e:
        print(f"Error at Sastodeal: {e}")

    return results

def scrape_daraz(search_query):
    results = []

    try:
        print("daraz called")
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.daraz.com.np/')

        search_box = driver.find_element(By.CSS_SELECTOR, 'input#q')
        search_box.send_keys(search_query)
        search_box.submit()

        driver.implicitly_wait(10)

        content = driver.page_source
        soup_bs4 = soup(content, 'html.parser')
        product_divs = soup_bs4.select('div.box--ujueT div[data-qa-locator="product-item"]')

        for div in product_divs:
            title_of_product = div.select_one('.title-wrapper--IaQ0m').text.split('|')[0].strip()
            # link_of_product = 'https:' + div.select_one('a.product-card--vHfY9').attrs.get('href').split('?')[0]
            price_of_product = div.select_one('span.currency--GVKjl').text
            

            image_of_product = div.select_one('img#id-img').attrs.get('src')

            results.append({
                'title': title_of_product,
                'price': price_of_product,
                'image': image_of_product,
                # 'link': link_of_product,
                'site': 'Daraz'
            })

        driver.quit()
    except Exception as e:
        print(f"Error at Daraz: {e}")

    return results

def scrape_dealayo(search_query):
    results = []

    try:
        print("dealayoo called")

        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(f'https://www.dealayo.com/catalogsearch/result/?q={search_query}')

        content = driver.page_source
        soup_bs4 = soup(content, 'html.parser')
        product_divs = soup_bs4.select('.item.product-item')

        for div in product_divs:
            title_of_product = div.select_one('.product-name a').text
            link_of_product = div.select_one('.product-name a').attrs.get('href')
            price_of_product = div.select_one('.price').text
            image_of_product = div.select_one('.amda-product-top a.product-image img').attrs.get('src')

            results.append({
                'title': title_of_product,
                'price': price_of_product,
                'image': image_of_product,
                'link': link_of_product,
                'site': 'Dealayo'
            })

        driver.quit()
    except Exception as e:
        print(f"Error at Dealayo: {e}")

    return results

def main(search_query: str):
    results = [
        # scrape_olizstore(search_query),
        # scrape_sastodeal(search_query),
        # scrape_daraz(search_query),
        scrape_dealayo(search_query),

    ]

    
    return results

# def main(search_query: str):
#     all_results = []

#     olizstore_results = scrape_olizstore(search_query)
#     for result in olizstore_results:
#         all_results.append({
#             'title': result['title'],
#             'price': result['price'],
#             'site': 'Olizstore'
#         })

#     sastodeal_results = scrape_sastodeal(search_query)
#     for result in sastodeal_results:
#         all_results.append({
#             'title': result['title'],
#             'price': result['price'],
#             'site': 'Sastodeal'
#         })

#     daraz_results = scrape_daraz(search_query)
#     for result in daraz_results:
#         all_results.append({
#             'title': result['title'],
#             'price': result['price'],
#             'site': 'Daraz'
#         })

#     dealayo_results = scrape_dealayo(search_query)
#     for result in dealayo_results:
#         all_results.append({
#             'title': result['title'],
#             'price': result['price'],
#             'site': 'Dealayo'
#         })

#     # Sort the results based on price in ascending order
#     all_results.sort(key=lambda x: float(x['price']) if x['price'].replace('.', '', 1).isdigit() else float('inf'))

#     return all_results

if __name__ == '__main__':
    search_query = ("iphone 12").replace(" ", "%20")
    results = main(search_query)
    print(results)
