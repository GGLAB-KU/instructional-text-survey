#This file generates fig5.b: Papers from each country Per Task Distribution over Time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the TSV file
df = pd.read_csv('data.tsv', sep='\t')

# Filter rows to include only years from 2010 onwards
df = df[df['year'] >= 2010]

# Extracting all tag columns dynamically
tag_columns = [col for col in df.columns if col.startswith('tag')]

# Update city-to-country mapping with the newly identified cities
city_to_country = {
    'Seattle': 'USA',
    'Philadelphia': 'USA',
    'Saarbrucken': 'Germany',
    'Beijing': 'China',
    'Cambridge Massachusetts': 'USA',
    'Stanford': 'USA',
    'Champaign': 'USA',
    'Baltimore': 'USA',
    'Pittsburgh': 'USA',
    'Tokyo': 'Japan',
    'New Delhi': 'India',
    'New York City': 'USA',
    'Mountain View': 'USA',
    'Yorktown Heights': 'USA',
    'Shanghai': 'China',
    'Santa Barbara': 'USA',
    'Singapore': 'Singapore',
    'Kyoto': 'Japan',
    'Menlo Park': 'USA',
    'San Francisco': 'USA',
    'Ghent': 'Belgium',
    'Los Angeles': 'USA',
    'Kharagpur': 'India',
    'Chicago': 'USA',
    'Stuttgart': 'Germany',
    'London': 'UK',
    'Boston': 'USA',
    'Edinburgh': 'UK',
    'Austin': 'USA',
    'Princeton': 'USA',
    'Amherst': 'USA',
    'Ithaca': 'USA',
    'Guangzhou': 'China',
    'Atlanta': 'USA',
    'Hong Kong': 'Hong Kong',
    'Tempe': 'USA',
    'Melbourne': 'Australia',
    'Pennsylvania': 'USA',
    'Hanoi': 'Vietnam',
    'Toronto': 'Canada',
    'Bandung': 'Indonesia',
    'Harbin': 'China',
    'Brescia': 'Italy',
    'Waltham': 'USA',
    'Sankt Augustin': 'Germany',
    'Raleigh': 'USA',
    'Columbus': 'USA',
    'California': 'USA',
    'Boulder': 'USA',
    'Verona': 'Italy',
    'Irvine': 'USA',
    'Liverpool': 'UK',
    'Munich': 'Germany',
    'Kanpur': 'India',
    'San Diego': 'USA',
    'Ramat Gan': 'Israel',
    'Chapel Hill': 'USA',
    'Daejeon': 'South Korea',
    'Providence': 'USA',
    'Abu Dhabi': 'UAE',
    'Istanbul': 'Turkey',
    'Sydney': 'Australia',
    'Porto': 'Portugal',
    'West Lafayette': 'USA',
    'Canberra': 'Australia',
    'Ankara': 'Turkey',
    'New York': 'USA',
    'Adelaide': 'Australia',
    'Valencia': 'Spain',
    'Delft': 'Netherlands',
    'Porto Alegre': 'Brazil',
    'Yokohama': 'Japan',
    'Potsdam': 'Germany',
    'Palo Alto': 'USA',
    'Bochum': 'Germany',
    'Sunnyvale': 'USA',
    'Ann Arbor': 'USA',
    'Freiburg im Breisgau': 'Germany',
    'Montreal': 'Canada'
}

# Task vs. Year and Country (Bubble Chart)
task_country_year = pd.DataFrame(columns=['Year', 'Country', 'Task', 'Count'])

# Populate the task_country_year DataFrame
rows = []
for _, row in df.iterrows():
    row_year = round(row['year'])  # Round the year to integer
    row_country = city_to_country.get(row[tag_columns[0]].split(':')[1], 'Unknown')
    row_tasks = [item.split(':')[1] for item in row[tag_columns].dropna() if 'TASK' in item]
    
    # Merge tasks that start with 'Grounded'
    merged_tasks = []
    for task in row_tasks:
        if task.startswith('Grounded'):
            merged_tasks.append('Grounded Tasks')
        else:
            merged_tasks.append(task)
    
    for task in set(merged_tasks):  # Ensure no duplicate task entries per row
        rows.append({'Year': row_year, 'Country': row_country, 'Task': task, 'Count': 1})

task_country_year = pd.concat([task_country_year, pd.DataFrame(rows)], ignore_index=True)

# Count overall publications per country
country_counts = task_country_year.groupby('Country')['Count'].sum().reset_index()

# Filter out countries with less than 3 publications
filtered_countries = country_counts[country_counts['Count'] >= 3]['Country']
task_country_year['Country'] = task_country_year['Country'].apply(lambda x: x if x in filtered_countries.values else 'Other')

# Recalculate the counts after filtering
task_country_year_grouped = task_country_year.groupby(['Year', 'Country', 'Task']).count().reset_index()

# Reorder the 'Country' category with 'USA' at the top and 'Other' at the bottom
ordered_countries = ['USA'] + [c for c in filtered_countries.values if c != 'USA'] + ['Other']
task_country_year_grouped['Country'] = pd.Categorical(
    task_country_year_grouped['Country'],
    categories=ordered_countries,
    ordered=True
)

plt.figure(figsize=(14, 10))

sns.scatterplot(data=task_country_year_grouped, x='Year', y='Country', size='Count', hue='Task', sizes=(100, 1000), legend='full', palette='tab10')

# Adjust legend
plt.legend(title=None, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='xx-large', frameon=False)

plt.xlabel('')
plt.ylabel('')
plt.xticks(fontsize=18, rotation=45)
plt.yticks(fontsize=18)
plt.tight_layout()
plt.savefig('task_year_country.png')
plt.show()
