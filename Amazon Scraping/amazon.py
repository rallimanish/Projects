
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

MAX_PAGES = 3


def search_page(search):
    search = search.split(' ')
    search = '%20'.join(search)

    try:
        url_search = 'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={0}&sprefix=thi%2Caps%2C505&crid=6O845RNLNMIR&rh=i%3Aaps%2Ck%3A{0}'.format(search)
        req = urllib.request.Request(url_search, headers=headers)
        resp = urllib.request.urlopen(req)

        respData = resp.read()
        soup = BeautifulSoup(respData, 'html.parser')
        product_link = soup.find('div', class_="a-row a-spacing-small")
        product_link = product_link.a['href']

        return product_link

    except Exception as e:
        print(str(e))


def product_page(search):

    try:
        url_product = search_page(search)
        req = urllib.request.Request(url_product, headers=headers)
        resp = urllib.request.urlopen(req)

        respData = resp.read()
        soup = BeautifulSoup(respData, 'html.parser')
        review_link = soup.find('div', class_="a-row a-spacing-large")
        review_link = "https://www.amazon.in{}".format(review_link.a['href'])

        return review_link

    except Exception as e:
        print(str(e))


def get_response(search, pageNumber):

    try:
        url = product_page(search)
        url = '{0}&pageNumber={1}'.format(url, pageNumber)
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        return resp.read()

    except Exception as e:
        print(str(e))


def get_reviews(search):

    # Writing it to a file
    with open('reviews.txt', 'w') as f:

        try:
            for i in range(1, MAX_PAGES + 1):
                respData = get_response(search, i)
                soup = BeautifulSoup(respData, 'html.parser')
                reviews = soup.find_all('div', attrs={'class': "a-section review"})

                for review in reviews:

                    # Getting the review title and star ratings
                    rev_title = str(review.div.div)
                    soup = BeautifulSoup(rev_title, 'html.parser')
                    rev_title = soup.find_all('a', class_="a-link-normal")
                    print("\nStar Ratings: {}".format(rev_title[0].text))
                    print("Review Title: {}".format(rev_title[1].text))

                    # Getting the actual review
                    rev_text = str(review.div)
                    soup = BeautifulSoup(rev_text, 'html.parser')
                    rev_text = soup.find('div', class_="a-row review-data")
                    print("Review Text:-\n{}".format(rev_text.text))
                    print('\n\n')

                    f.write("Star Ratings: {}".format(rev_title[0].text))
                    f.write('\n')
                    f.write("Review Title: {}".format(rev_title[1].text))
                    f.write('\n')
                    f.write("Review Text:-\n{}".format(rev_text.text))
                    f.write('\n\n\n')

        except Exception as e:
            print(str(e))


def main():

    search = input("\nEnter a Book Name to get customer reviews: ")

    get_reviews(search)


if __name__ == '__main__':
    main()
