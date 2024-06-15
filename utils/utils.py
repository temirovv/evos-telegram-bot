from geopy.geocoders import Nominatim
from loader import db


def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="location_finder")
    location = geolocator.reverse((latitude, longitude))
    address = location.raw['address']
    # Depending on what exactly you want, you can extract different parts of the address.
    # For example, you might want 'city', 'country', etc.
    city = address.get('city', '')
    country = address.get('country', '')
    street = address.get('street', '')
    return address


def sort_user_products(tg_id: int):
    data = db.get_order(tg_id)
    for user_id, product_id, quantity in data:
        print(
            f"{user_id=}"
        )
        print(
            f"product name: {db.get_product_name(product_id)[-1]}"
        )
        print(
            f"{quantity=}"
        )



# # Example usage:
# latitude, longitude =  -0.05160534897156116, 11.614744303363235

# street = get_location_name(latitude, longitude)

# print("street:", street)
# # , 