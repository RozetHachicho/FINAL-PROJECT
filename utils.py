# built-in imports
# standard library imports
import pickle

# external imports
import requests

# internal imports
from codeapp import db
from codeapp.models import House

# from flask import current_app


def get_data_list() -> list[House]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving it to a Redis list.
    """
    if db.exists("database_list"):
        dataset_store: list[House] = []
        raw_dataset: list[bytes] = db.lrange("database_list", 0, -1)
        for obj in raw_dataset:
            dataset_store.append(pickle.loads(obj))
        return dataset_store
    response = requests.get("https://onu1.s2.chalmers.se/datasets/houses.json")
    data_dict = response.json()
    for row in data_dict:
        new_1 = House(
            id=row["Id"],
            building_type=row["BldgType"],
            house_style=row["HouseStyle"],
            overall_quality=row["OverallQual"],
            overall_condition=row["OverallCond"],
            year_built=row["YearBuilt"],
            roof_style=row["RoofStyle"],
            number_full_bathrooms=row["FullBath"],
            number_half_bathrooms=row["HalfBath"],
            number_bedrooms=row["BedroomAbvGr"],
            number_fireplaces=row["Fireplaces"],
            sales_price=row["SalePrice"],
        )
        db.lpush("database_list", pickle.dumps(new_1))
        dataset_store.append(new_1)
    return dataset_store


def calculate_statistics(dataset: list[House]) -> dict[int, int]:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """
    # average price per number of bedrooms = ex snittkostnaden för en 3.a
    counter_1: dict[int, int] = {}
    for obj in dataset:
        bedroom = obj.number_bedrooms
        if bedroom not in counter_1:
            counter_1[bedroom] = 1
        else:
            counter_1[bedroom] += 1

    counter_2: dict[int, int] = {}
    for obj in dataset:
        # price = object.sales_price
        bedroom = obj.number_bedrooms
        if bedroom not in counter_2:
            counter_2[bedroom] = obj.sales_price
        else:
            counter_2[bedroom] += obj.sales_price

    counter_3: dict[int, int] = {}
    for bedroom in counter_1.items():
        if bedroom in counter_2:
            counter_3[bedroom] = counter_2[bedroom] // counter_1[bedroom]
    return counter_3


# def avr_purr_room(counter_1: list[int], counter_2: list[int]) ->


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
