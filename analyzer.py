#import bibliotek
import os
import pandas as pd

#wyświetlenie zawartości katalogu opinions
print(os.listdir("./opinions"))

#wczytanie id produktu, którego opinie będą analizowane
product_id = input("Podaj kod produktu: ")

opinions = pd.read_json("opinions/"+product_id+".json")
opinions = opinions.set_index("opinion_id")

print(opinions)