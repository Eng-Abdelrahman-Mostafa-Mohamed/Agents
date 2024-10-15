import matplotlib.pyplot as plt
import pandas as pd

data = {'Country': ['United States', 'Brazil', 'China', 'Japan', 'India'],
         'Total Dentists': [200000, 150000, 500000, 100000, 250000],
         'Mean Dentists per 100,000 people': [40, 30, 20, 80, 15],
         'Standard Deviation': [10, 15, 20, 5, 25]}

df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))
plt.bar(df['Country'], df['Mean Dentists per 100,000 people'])
plt.xlabel('Country')
plt.ylabel('Mean Dentists per 100,000 people')
plt.title('Distribution of Dentists in 5 Countries')
plt.show()