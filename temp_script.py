import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('WorldPopulation2023.csv')
print(data.columns)
# assuming the population column is the second column
afghanistan_population = data[data['Country'] == 'Afghanistan'].iloc[:, 1]
albania_population = data[data['Country'] == 'Albania'].iloc[:, 1]
western_sahara_population = data[data['Country'] == 'Western Sahara'].iloc[:, 1]
plt.bar(['Afghanistan', 'Albania', 'Western Sahara'], [afghanistan_population.values[0], albania_population.values[0], western_sahara_population.values[0]])
plt.xlabel('Country')
plt.ylabel('Population')
plt.title('Population of Afghanistan, Albania and Western Sahara')
plt.show()