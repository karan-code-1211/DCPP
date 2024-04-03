# import necessary libraries
import requests
from bs4 import BeautifulSoup

# Create a class to extract the data from each product url for Question 2
class EbayDataMiner:
    # define all the required variables
    class EbayData:
        name = None
        returns = None
        ships_to = None
        shipping_price = None
        estimate_delivery = None
        location = None
        payment_modes = None
        price = None
        ebay_item_number = None
        condition = None
        brand = None
        color = None
        type = None
        material = None
        starting_bid = None

    # function to extract the product name
    def get_name(self, soup):
        # use try except to return 'NA value if None value is received while scraping
        try:
            name_element = soup.find("div", class_="vim x-item-title")

            if name_element:
                name = name_element.text.strip()
                return name
            return None
        except Exception as e:
            return 'NA'

    # function to get the return policy of the product
    def get_returns(self, soup):
        # locate the path of the detail to be scraped in html and return the value
        try:
            returns_parent = soup.find("div", {"data-testid": "x-returns-minview"})
            returns_parent_lables = returns_parent.find("div", class_="ux-labels-values__values")
            all_text_spans = returns_parent_lables.find("div").find("div").find_all("span", class_="ux-textspans",
                                                                                          recursive=False)
            returns_value = ""
            for text_span in all_text_spans:
                returns_value = returns_value + text_span.text
            return returns_value
        except Exception as e:
            return 'NA'

    # function to get the shipping to details of the product
    def get_ships_to(self, soup):
        try:
            ships_to_parent = soup.find("div", {"data-testid": "d-shipping-minview"})
            ships_to_parent_labels = ships_to_parent.find("div", class_="ux-layout-section__row")
            ships_to_parent_labels_content = ships_to_parent_labels.find("div",
                                                                               class_="ux-labels-values__values-content")
            all_text_span = ships_to_parent_labels_content.find("div").find_all("span", class_="ux-textspans",
                                                                           recursive=False)
            ships_to_value = ""
            # as there are multiple text fields we need to extract in this hence extracting all and combining into a single value.
            for text_span in all_text_span:
                ships_to_value = ships_to_value + text_span.text
            return ships_to_value
        except Exception as e:
            return 'NA'


    # function to get the estimate delivery time of the product
    def get_estimate_delivery(self, soup):
        try:
            ships_to_parent = soup.find("div", {"data-testid": "d-shipping-minview"})  # d-shipping-minview
            ships_to_parent_labels = ships_to_parent.find_all("div", class_="ux-layout-section__row")
            key_val = {}
            for i in ships_to_parent_labels:
                j = i.find("div", class_="ux-labels-values__labels")
                k = i.find("div", class_="ux-labels-values__values")
                key = j.find("span", class_="ux-textspans").text.strip()
                k_ = k.find("div", class_='ux-labels-values__values-content')
                k__ = k_.find("div", recursive=False)
                ts = k_.find_all("span", class_="ux-textspans")
                value = ' '.join([ii.text.strip() for ii in ts])
                key_val[key] = value

            return key_val["Delivery:"]
        except Exception as e:
            return 'NA'


    # function to get the shipping price of the product
    def get_shipping_price(self, soup):
        try:
            shipping_price_parent = soup.find("div", {"data-testid": "d-shipping-minview"})
            shipping_price_parent_labels = shipping_price_parent.find("div", class_="ux-layout-section__row")
            shipping_price_parent_labels_content = shipping_price_parent_labels.find("div",
                                                                               class_="ux-labels-values__values-content")
            text_span = shipping_price_parent_labels_content.find("div").find("span", class_="ux-textspans",
                                                                           recursive=True)
            shipping_price_value = ""

            shipping_price_value = shipping_price_value + text_span.text
            return shipping_price_value.split(".")[0]
        except Exception as e:
            return 'NA'

    # function to get the starting bid of the product from Auction section.
    def get_starting_bid(self, soup):
        try:
            starting_bid_parent = soup.find("div", {"data-testid": "app-main-container-upgrade__history_content"})
            starting_bid_parent_labels = starting_bid_parent.find("div", class_= "app-container-view-upgrade__content_table")
            starting_bid_parent_labels_context = starting_bid_parent_labels.find("table", class_= "app-bid-history__table")

            text_span = starting_bid_parent_labels_context.find("div", class_= "textual-display-item")

            starting_bid_value = ""

            starting_bid_value = starting_bid_value + text_span.text
            return starting_bid_value.split(".")[0]


        except Exception as e:
            return 'NA'


    # function to get the location of the product
    def get_location(self, soup):
        try:
            location_parent = soup.find("div", {"data-testid": "d-shipping-minview"})
            location_parent_labels = location_parent.find("div", class_="ux-layout-section__row")
            location_parent_labels_content = location_parent_labels.find("div",
                                                                             class_="ux-labels-values__values-content")
            text_span = location_parent_labels_content.find("span", class_="ux-textspans ux-textspans--SECONDARY",
                                                              recursive=True)
            location_value = ""

            location_value = location_value + text_span.text
            return location_value.split("Located in:")[1].strip()
        except Exception as e:
            return 'NA'

    # function to get the payment modes available for buying the product
    def get_payment_modes(self, soup):
        try:
            payment_mode_parent = soup.find("div", {"data-testid": "d-payments-minview"})
            payment_mode_parent_labels = payment_mode_parent.find("div", class_="ux-labels-values__values")
            # payment_mode_parent_labels_content = payment_mode_parent_labels.find("span", class_= "ux-labels-values__values col-9")
            title_spans = payment_mode_parent_labels.find("div", class_="ux-labels-values__values-content")
            title_spans_all = title_spans.find_all("span", class_="ux-textspans")
            all_titles = []
            for title_span in title_spans_all:
                if title_span.get("title"):
                    all_titles.append(title_span.get("title"))
            return ','.join(all_titles)
        except Exception as e:
            return 'NA'


    # function to get the price of the product
    def get_price(self, soup):
        try:
            price_parent = soup.find("div", {"data-testid": "x-bin-price"})
            if price_parent is None:
                return None
            price_parent_labels = price_parent.find("div", class_="x-price-primary")
            text_span = price_parent_labels.find("span", class_="ux-textspans",
                                                 recursive=True)

            price_value = ""

            price_value = price_value + text_span.text
            return price_value
        except Exception as e:
            return 'NA'


    # function to extract the ebay item number of the product
    def get_ebay_item_number(self, soup):
        try:
            item_number = soup.find("div", class_="tabs__content")
            item_number_labels = item_number.find("div", {'data-testid': 'd-vi-region'})
            text_span = item_number_labels.find("span", class_="ux-textspans ux-textspans--BOLD", recursive=True)

            ebay_item_number = ""

            ebay_item_number = ebay_item_number + text_span.text
            return ebay_item_number
        except Exception as e:
            return 'NA'



    # as there are multiple rows and they difer for each product, hence creating a function to pick the value on the Values section of the page when it reads the corresponding Labels value.
    def get_about_me_details_of_product(self, soup):

        def get_key_value_from_row_item(row_item_):
            try:
                key = value = None
                key_soup = row_item_.find("div", class_ = "ux-labels-values__labels")
                value_soup = row_item_.find("div", class_ = "ux-labels-values__values")
                key = key_soup.find("span", class_="ux-textspans").text.strip()
                value = value_soup.find("span", class_="ux-textspans").text.strip()
                return key, value
            except Exception as e:
                print(e)
                return None, None

        # function to get that key value from each row
        def get_key_value_from_row(about_me_detail_row_):
            about_me_detail_row_key_values = {

            }
            if not about_me_detail_row_:
                return about_me_detail_row_key_values
            row_items = about_me_detail_row_.find_all("div", class_="ux-layout-section-evo__col", recursive=False)
            for row_item in row_items:
                (key, value) = get_key_value_from_row_item(row_item)
                if key and value:
                    about_me_detail_row_key_values[key] = value
            return about_me_detail_row_key_values

        about_me_details = {
        }
        soup.find("div", {"data-testid": "x-about-this-item"}).find("div",
                                                                    class_="ux-layout-section-evo__item ux-layout-section-evo__item--table-view").find_all(
            "div", class_="ux-layout-section-evo__row", recursive=False)
        about_me_soup = soup.find("div", {"data-testid": "x-about-this-item"})
        about_me_detail_rows = about_me_soup.find("div", class_="ux-layout-section-evo__item"
                                                                " ux-layout-section-evo__item--table-view").find_all(
            "div", class_="ux-layout-section-evo__row", recursive=False)
        for about_me_detail_row in about_me_detail_rows:
            about_me_detail_row_res = get_key_value_from_row(about_me_detail_row)
            if about_me_detail_row_res:
                about_me_details.update(**about_me_detail_row_res)

        return about_me_details


    # saving and calling all the above functions for part 2 and getting the respective values in their columns
    def get_product_data_from_soup(self, soup):
        data = EbayDataMiner.EbayData()

        data.name = self.get_name(soup)
        data.returns = self.get_returns(soup)
        data.ships_to = self.get_ships_to(soup)
        data.shipping_price = self.get_shipping_price(soup)
        data.location = self.get_location(soup)
        data.payment_modes = self.get_payment_modes(soup)
        data.price = self.get_price(soup)
        data.ebay_item_number = self.get_ebay_item_number(soup)
        data.estimate_delivery = self.get_estimate_delivery(soup)
        data.starting_bid = self.get_starting_bid(soup)
        about_me_details = self.get_about_me_details_of_product(soup)
        data.brand = about_me_details.get("Brand", "NA")
        data.condition = about_me_details.get("Condition", "NA")
        data.color = about_me_details.get("Color", "NA")
        data.type = about_me_details.get("Type", "NA")
        data.material = about_me_details.get("Material", "NA")
        # self.get_key_value_for_shipping(soup)

        return data

    # function which is called after part 1 and here we create the soup
    def get_product_details_for_urls(self, urls: list):
        product_details = []
        for url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                product_details.append(self.get_product_data_from_soup(soup))

        return product_details


print("\nPart 1 begins here:-")
# Define the URL of the eBay search page
url = "https://www.ebay.com/sch/i.html?_nkw=table"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Initialize lists to store data
    names = []
    prices = []
    shipping_costs = []
    image_urls = []
    watchers = []
    conditions = []

    # Define the list to store product URLs
    product_urls = []

    # Find and loop through the product listings on the page
    for product in soup.find_all("div", class_="s-item__info")[:8]:
        name_element = product.find("a").find("div").find("span")
        if name_element:
            name = name_element.text.strip()
        else:
            name = "N/A"
        price_element = product.find("span", class_="s-item__price")
        if price_element:
            price = price_element.text.strip()
        else:
            price = "N/A"
        shipping_cost_element = product.find("span", class_="s-item__shipping")
        if shipping_cost_element:
            shipping_cost = shipping_cost_element.text.strip()
        else:
            shipping_cost = "N/A"
        image_element = product.find("img")
        if image_element:
            image_url = image_element.get("src")
        else:
            image_url = "N/A"
        watcher_element_parent = product.find("span", class_="s-item__watchCountTotal")
        if watcher_element_parent and watcher_element_parent.find("span"):
            watcher_element = watcher_element_parent.find("span")
            watcher_count = watcher_element.text.strip()
        else:
            watcher_count = "N/A"
        condition_element = product.find("span", class_="SECONDARY_INFO")
        if condition_element:
            condition = condition_element.text.strip()
        else:
            condition = "N/A"

        # Append the extracted data to the lists
        names.append(name)
        prices.append(price)
        shipping_costs.append(shipping_cost)
        image_urls.append(image_url)
        watchers.append(watcher_count)
        conditions.append(condition)

        # Extract product details using the function
        product_link_element = product.find("a", class_="s-item__link")
        if product_link_element:
            product_link = product_link_element.get("href")
            if product_link.startswith("http"):
                product_url = product_link
            else:
                product_url = f"https://www.ebay.com{product_link}"

            # Send a new request to the product page URL
            product_response = requests.get(product_url)

            # Check if the request was successful
            if product_response.status_code == 200:
                product_soup = BeautifulSoup(product_response.text, "html.parser")
            else:
                print(f"Failed to retrieve product details for URL: {product_url}")
        else:
            continue

        # Print the extracted data for each product
        print(f"Product Name: {name}")
        print(f"Price: {price}")
        print(f"Shipping Cost: {shipping_cost}")
        print(f"URL: {product_url}")
        print(f"Image URL: {image_url}")
        print(f"Number of Watchers: {watcher_count}")
        print(f"Condition: {condition}")
        print("------")
        product_urls.append(product_url)

    # Write the data to a TSV file for Part 1
    with open("tableList.tsv", "w", encoding="utf-8") as file:
        header = "Product Name\tPrice\tShipping Cost\tImage URL\tNumber of Watchers\tCondition\n"
        file.write(header)

        for i in range(len(names)):
            line = f"{names[i]}\t{prices[i]}\t{shipping_costs[i]}\t{image_urls[i]}\t{watchers[i]}\t{conditions[i]}\n"
            file.write(line)
        file.close()

    print("Data scraped and saved to tableList.tsv.")
    product_details = EbayDataMiner().get_product_details_for_urls(product_urls)
    print(product_details)

    # write the data to a TSV file for Part 2
    with open("tableDetails.tsv", "w", encoding="utf-8") as file:
        header = ("Product Name\tReturn Policy\tShipping to\tShipping Price\tEstimated Delivery\tStarting Bid\tLocated In\tPayment Modes\tPrice\tEbay Item Number\t"
                  "Condition\tBrand\tColor\tType\tMaterial\n")
        file.write(header)
        print("\nPart 2 begins below:-")
        for product_detail in product_details:
            line = (f"{product_detail.name}\t{product_detail.returns}\t{product_detail.ships_to}\t"
                    f"{product_detail.shipping_price}\t{product_detail.estimate_delivery}\t{product_detail.starting_bid}\t{product_detail.location}\t{product_detail.payment_modes}\t"
                    f"{product_detail.price}\t{product_detail.ebay_item_number}\t"
                    f"{product_detail.condition}\t{product_detail.brand}\t{product_detail.color}\t{product_detail.type}\t"
                    f"{product_detail.material}\n")
            file.write(line)
            print(f"\nProduct Name: {product_detail.name}")
            print(f"Return Policy: {product_detail.returns}")
            print(f"Shipping To: {product_detail.ships_to}")
            print(f"Item Location: {product_detail.location}")
            print(f"SHipping Cost: {product_detail.shipping_price}")
            print(f"Estimated Delivery: {product_detail.estimate_delivery}")
            print(f"Payment Modes: {product_detail.payment_modes}")
            print(f"Price: {product_detail.price}")
            print(f"Starting Bid: {product_detail.starting_bid}")
            print(f"eBay Item Number: {product_detail.ebay_item_number}")
            print(f"Condition: {product_detail.condition}")
            print(f"Brand: {product_detail.brand}")
            print(f"Color: {product_detail.color}")
            print(f"Type: {product_detail.type}")
            print(f"Material: {product_detail.material}")
            print("------")
        file.close()

    print("\nData scraped and saved to tableDetails.tsv")