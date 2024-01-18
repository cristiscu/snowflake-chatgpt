from faker import Faker
import random

fake = Faker()

# Generate 100 fake customer records
customers = []
for i in range(100):
    customers.append({
        "CustomerKey": i,
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "Email": fake.safe_email(),
        "Phone": fake.phone_number(),
        "AddressLine1": fake.street_address(),
        "AddressLine2": fake.secondary_address(),
        "City": fake.city(),
        "State": fake.state(),
        "ZipCode": fake.zipcode(),
        "Country": fake.country()
    })

# Generate and print SQL INSERT statements
print("INSERT INTO DimCustomer (CustomerKey, FirstName, LastName, Email, Phone, AddressLine1, AddressLine2, City, State, ZipCode, Country) VALUES")

values_list = []
for customer in customers:
    values_list.append(
        f"({customer['CustomerKey']}, '{customer['FirstName']}', '{customer['LastName']}', '{customer['Email']}', '{customer['Phone']}', "
        f"'{customer['AddressLine1']}', '{customer['AddressLine2']}', '{customer['City']}', '{customer['State']}', "
        f"'{customer['ZipCode']}', '{customer['Country']}')"
    )

# Join all values and separate by commas
values_str = ",\n".join(values_list)

# Omitting the last comma for the final value
print(values_str + ";")
