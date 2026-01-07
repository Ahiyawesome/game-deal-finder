import requests
import time

def get_stores(url):
    response = requests.get(url+"stores")
    data = response.json()
    stores_dict = {store["storeID"]: store["storeName"] for store in data}

    time.sleep(1)
    
    return stores_dict


def search(game_name, url):
    payload = {"title":game_name}
    response = requests.get(url+"games", params=payload)
    data = response.json()
    time.sleep(2)   
    return data[0]


def find_cheapest_deal(url, game, store_dict):
    payload = {"id":game["cheapestDealID"]}
    response = requests.get(url+"deals?id="+payload["id"])
    best_data = response.json()
    time.sleep(2)
    return {"game_name":best_data["gameInfo"]["name"], "price":best_data["gameInfo"]["salePrice"], "store":store_dict[best_data["gameInfo"]["storeID"]]}

def main():
    wishlist = ["Cyberpunk 2077", "Hades"]
    url = "https://www.cheapshark.com/api/1.0/"
    store_dict = get_stores(url)
    
    for wish in wishlist:
        data = search(wish, url)
        if not data:
            print(f"Game: {wish} not found!")
        else:
            best_deal = find_cheapest_deal(url, data, store_dict)
            if best_deal:
                print(f"Best deal for {best_deal['game_name']} is ${best_deal['price']} at Store {bgest_deal['store']}")
            else:
                print(f"Due to error, couldn't get {wish}")

if __name__ == "__main__":
    main()