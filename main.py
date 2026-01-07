import requests
import time


def get_response_data(url, addition="", param=None, id=None):
    if id:
        ls = id.split()
        id = "%20".join(ls)
    response = requests.get(url + addition + ("?"+param+"="+id if param else ""))
    time.sleep(2)
    data = response.json()

    return data


def get_stores(url):
    data = get_response_data(url, "stores")
    stores_dict = {store["storeID"]: store["storeName"] for store in data}

    return stores_dict


def search(game_name, url):
    data = get_response_data(url, "games", "title", game_name)

    if not data:
        return None

    return data[0]


def find_cheapest_deal(url, game, store_dict):
    best_data = get_response_data(url, "deals", "id", game["cheapestDealID"])

    return {"game_name":best_data["gameInfo"]["name"], "price":best_data["gameInfo"]["salePrice"], "store":store_dict[best_data["gameInfo"]["storeID"]]}


def find_top_n_deals(url, game, store_dict, k):
    data = get_response_data(url, "games", "id", game["gameID"])
    deals = data["deals"]
    n = k if len(deals) >= k else len(deals)
    top_three = [{"price": deals[i]["price"], "store": store_dict[deals[i]["storeID"]]} for i in range(n)]

    return (top_three, n)


def main():
    wishlist = []
    cur_game = "p"
    url = "https://www.cheapshark.com/api/1.0/"
    store_dict = get_stores(url)

    while cur_game and cur_game != "f":
        if cur_game != "p":
            wishlist.append(cur_game)
        cur_game = input("What game do you want on your wishlist? Type f if finished: ")

    n = int(input("How many top deals do you want to see? "))
    if not n:
        n = 1

    for wish in wishlist:
        data = search(wish, url)
        if not data:
            print(f"Game: {wish} not found!")
        else:
            top_n_deals, n = find_top_n_deals(url, data, store_dict, n)
            if top_n_deals:
                print(f"Top {n} deals for {wish}")
                for deal in top_n_deals:
                    print(f"${deal['price']} at store: {deal['store']}")
                print()
            else:
                print(f"Due to error, couldn't get {wish}")

if __name__ == "__main__":
    main()