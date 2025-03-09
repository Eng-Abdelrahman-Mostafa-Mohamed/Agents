import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

data = pd.read_csv('Agents/WorldPopulation2023.csv')

def generate_plots(data):
    pdf = FPDF()
    for i in range(10):
        plt.figure(figsize=(10,6))
        if i == 0:
            sns.barplot(x='Country', y='Population', data=data)
            plt.title('Barplot of Country vs Population')
        elif i == 1:
            sns.boxplot(x='Region', y='Population', data=data)
            plt.title('Boxplot of Region vs Population')
        elif i == 2:
            sns.scatterplot(x='Population', y='GDP', data=data)
            plt.title('Scatterplot of Population vs GDP')
        # Add more plots as needed
        plt.savefig(f'plot_{i}.png')
        pdf.add_page()
        pdf.image(f'plot_{i}.png', x=10, y=10, w=170)
    pdf.output('population_plots.pdf', 'F')

generate_plots(data)