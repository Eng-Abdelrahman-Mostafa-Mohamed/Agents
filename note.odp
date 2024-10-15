import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('WorldPopulation2023.csv')
afghanistan_population = data[data['Country'] == 'Afghanistan']['Population2023'].values[0]
albania_population = data[data['Country'] == 'Albania']['Population2023'].values[0]
western_sahara_population = data[data['Country'] == 'Western Sahara']['Population2023'].values[0]
plt.bar(['Afghanistan', 'Albania', 'Western Sahara'], [afghanistan_population, albania_population, western_sahara_population])
plt.xlabel('Country')
plt.ylabel('Population2023')
plt.title('Population2023 of Afghanistan, Albania and Western Sahara')
plt.show()