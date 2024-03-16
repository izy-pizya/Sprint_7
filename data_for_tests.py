from faker import Faker

fake = Faker()

order_data = {
    "firstName": fake.name(),
    "lastName": f"{fake.last_name()} s",
    "address": f"Moscow, {fake.building_number()} qwe.",
    "metroStation": 1,
    "phone": "+7 999 606 00 11",
    "rentTime": 1,
    "deliveryDate": "2026-01-01",
    "comment": "test comment",
    "color": []
}