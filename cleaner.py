from typing import Any
import pandas as pd
import numpy as np

df = pd.read_csv("../challenge-collecting-data/data/Property_structured_data.csv")

columns = ['postal_code', 'type_of_property', 'subtype_of_property', 'type_of_sale', 'price',
       'number_of_bedrooms', 'surface', 'kitchen_type',
       'fully_equipped_kitchen', 'furnished', 'open_fire', 'terrace',
       'terrace_surface', 'garden', 'garden_surface', 'land_surface',
       'number_of_facades', 'swimming_pool', 'state_of_the_building']

def replace_to_nan(data: pd.DataFrame, column_name:str, value: Any):
    data.loc[data[column_name] == value, column_name] = np.nan

replace_to_nan(df, "price", -1)
replace_to_nan(df, "surface", -1)
replace_to_nan(df, "number_of_bedrooms", -1)

df.loc[df["number_of_facades"] > 8, "number_of_facades"] = np.nan

df["number_of_facades"] = np.where((df["number_of_facades"] == -1) & (df["type_of_property"] == "APARTMENT"), 1, df["number_of_facades"])
df["number_of_facades"] = np.where((df["number_of_facades"] == -1) & (df["type_of_property"] == "HOUSE"), 2, df["number_of_facades"])

df["fully_equipped_kitchen"] = df["fully_equipped_kitchen"].map({"-1": -1, "1": 1, "INSTALLED": 0, "SEMI_EQUIPPED": 0, "NOT_INSTALLED": 0, "USA_INSTALLED": 0, "USA_SEMI_EQUIPPED": 0, "USA_UNINSTALLED": 0})
df["state_of_the_building"] = df["state_of_the_building"].map({"NO_INFO": -1, "TO_BE_DONE_UP": 0, "TO_RENOVATE": 0, "TO_RESTORE": 0, "JUST_RENOVATED": 1, "GOOD": 1, "AS_NEW": 1})

df.dropna(subset=["price"], inplace=True)
df.dropna(subset=["surface"], inplace=True)
df.dropna(subset=["number_of_bedrooms"], inplace=True)
df.dropna(subset=["number_of_facades"], inplace=True)

df[df["type_of_property"].str.contains("APARTMENT_GROUP")==False]
df[df["type_of_property"].str.contains("HOUSE_GROUP")==False]
df[df["type_of_sale"].str.contains("first_session_with_reserve_price")==True]
df[df["type_of_sale"].str.contains("residential_sale")==True]
df.drop_duplicates()

print(df["type_of_sale"].value_counts())


