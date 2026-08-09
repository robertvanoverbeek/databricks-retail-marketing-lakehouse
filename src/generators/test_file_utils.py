def create_list_data():
    cars = [
        {"make": "Toyota", "model": "Camry", "year": 2022},
        {"make": "Honda", "model": "Accord", "year": 2021},
        {"make": "Ford", "model": "Mustang", "year": 2023},
    ]
    print("List data:", cars)


def create_tuple_data():
    coordinates = (34.0522, -118.2437, "Los Angeles")
    print("Tuple data:", coordinates)


def create_dict_data():
    car = {
        "make": "Tesla",
        "model": "Model 3",
        "year": 2024,
        "color": "silver",
    }
    print("Dict data:", car)


def create_set_data():
    colors = {"white", "black", "red", "blue", "silver"}
    print("Set data:", colors)


def main():
    create_list_data()
    create_tuple_data()
    create_dict_data()
    create_set_data()


if __name__ == "__main__":
    main()


