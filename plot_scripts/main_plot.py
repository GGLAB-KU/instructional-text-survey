import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import networkx as nx
import numpy as np

# Load the data from the TSV file
df = pd.read_csv('data.tsv', sep='\t')

# Extracting all tag columns dynamically
tag_columns = [col for col in df.columns if col.startswith('tag')]

# Initialize lists to hold extracted data types and tasks
data_types = []
tasks = []

# Extract year and city for additional analyses
years = df['year'].tolist()
cities = df[tag_columns[0]].apply(lambda x: x.split(':')[1] if 'CITY' in x else None).dropna().tolist()

# Create a dictionary to map cities to countries (assuming a simplified mapping)
city_to_country = {
    'Stanford': 'USA',
    'Seattle': 'USA',
    'New York City': 'USA',
    'Beijing': 'China',
    'Stuttgart': 'Germany',
    'Melbourne': 'Australia',
    'Santa Barbara': 'USA',
    'Princeton': 'USA',
    'San Francisco': 'USA',
    'Pittsburgh': 'USA',
    'Austin': 'USA',
    'Philadelphia': 'USA',
    'Canberra': 'Australia',
    'New Delhi': 'India',
    'Menlo Park': 'USA',
    'Ann Arbor': 'USA',
    'Amherst': 'USA',
    'Waltham': 'USA',
    'Ithaca': 'USA',
    'Sunnyvale': 'USA',
    'Liverpool': 'UK',
    'Edinburgh': 'UK',
    'Hong Kong': 'Hong Kong',
    'Kyoto': 'Japan',
    'Champaign': 'USA',
    'Sydney': 'Australia',
    'Kanpur': 'India',
    'Adelaide': 'Australia',
    'Brescia': 'Italy',
    'Porto Alegre': 'Brazil',
    'Menlo Park': 'USA',
    'Tempe': 'USA',
    'Mountain View': 'USA',
    'Delft': 'Netherlands',
    'Saarbrucken': 'Germany',
    'Verona': 'Italy',
    'Irvine': 'USA',
    'Ikoma': 'Japan',
    'Tel Aviv': 'Israel',
    'West Lafayette': 'USA',
    'Ghent': 'Belgium',
    'Yorktown Heights': 'USA',
    'Singapore': 'Singapore',
    'Shanghai': 'China',
    'Columbus': 'USA',
    'Kyoto': 'Japan',
    'Cambridge Massachusetts': 'USA',
    'Providence': 'USA',
    'London': 'UK',
    'Maryland': 'USA',
    'Boston': 'USA',
    'Vienna': 'Austria',
    'Paris': 'France',
    'Tokyo': 'Japan',
    'Chicago': 'USA',
    'Porto': 'Portugal',
    'Abu Dhabi': 'UAE',
    'San Diego': 'USA',
    'Freiburg im Breisgau': 'Germany',
    'Chapel Hill': 'USA',
    'Guangzhou': 'China',
    'Potsdam': 'Germany',
    'Yokohama': 'Japan'
}

# Update the cities list with countries
countries = [city_to_country.get(city, 'Unknown') for city in cities]

# Iterate over the tag columns to extract data types and tasks
for col in tag_columns:
    for item in df[col].dropna().unique():
        if 'DATA' in item:
            data_types.append(item.split(':')[1])
        if 'TASK' in item:
            tasks.append(item.split(':')[1])

# Removing duplicates
data_types = list(set(data_types))
tasks = list(set(tasks))

# Creating a crosstab for the heatmap
crosstab = pd.DataFrame(0, index=data_types, columns=tasks)

# Populate the crosstab with counts
for _, row in df.iterrows():
    row_data_types = [item.split(':')[1] for item in row[tag_columns].dropna() if 'DATA' in item]
    row_tasks = [item.split(':')[1] for item in row[tag_columns].dropna() if 'TASK' in item]
    for data_type in row_data_types:
        for task in row_tasks:
            crosstab.loc[data_type, task] += 1

# Plot the heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(crosstab, annot=True, fmt='d', cmap='YlGnBu')
plt.ylabel('Data Representation')
plt.xlabel('Tasks')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.savefig('heatmap_data_tasks.png')
plt.close()

# Yearly Trends of Specific Tasks
task_yearly_trends = pd.DataFrame(0, index=sorted(set(years)), columns=tasks)

# Populate the task_yearly_trends DataFrame
for _, row in df.iterrows():
    row_year = round(row['year'])  # Round the year to integer
    row_tasks = [item.split(':')[1] for item in row[tag_columns].dropna() if 'TASK' in item]
    for task in row_tasks:
        task_yearly_trends.loc[row_year, task] += 1

# Plot yearly trends for all tasks in a single plot
plt.figure(figsize=(14, 10))
for task in tasks:
    sns.lineplot(data=task_yearly_trends[task], label=task)

plt.ylabel('Number of Papers')
plt.xlabel('Year')
plt.legend(title='Task', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.xticks(np.arange(min(task_yearly_trends.index), max(task_yearly_trends.index)+1, 1))
plt.savefig('yearly_trends_all_tasks.png')
plt.close()

# Task Combination Frequency (Network Graph)
task_combinations = []

# Extract task combinations from each row
for _, row in df.iterrows():
    row_tasks = [item.split(':')[1] for item in row[tag_columns].dropna() if 'TASK' in item]
    task_combinations.extend(list(itertools.combinations(row_tasks, 2)))

# Create a DataFrame for task combinations
task_comb_df = pd.DataFrame(task_combinations, columns=['Task1', 'Task2'])

# Create a graph from task combinations
G = nx.Graph()
for _, row in task_comb_df.iterrows():
    G.add_edge(row['Task1'], row['Task2'])

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.3)  # Adjust k to avoid overlap
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold")
plt.tight_layout()  # Adjust layout to prevent overlap
plt.savefig('task_combination_frequency.png')
plt.close()

# Task vs. Year and Country (Bubble Chart)
task_country_year = pd.DataFrame(columns=['Year', 'Country', 'Task', 'Count'])

# Populate the task_country_year DataFrame using pd.concat instead of append
rows = []
for _, row in df.iterrows():
    row_year = round(row['year'])  # Round the year to integer
    row_country = city_to_country.get(row[tag_columns[0]].split(':')[1], 'Unknown')
    row_tasks = [item.split(':')[1] for item in row[tag_columns].dropna() if 'TASK' in item]
    for task in row_tasks:
        rows.append({'Year': row_year, 'Country': row_country, 'Task': task, 'Count': 1})

task_country_year = pd.concat([task_country_year, pd.DataFrame(rows)], ignore_index=True)

task_country_year_grouped = task_country_year.groupby(['Year', 'Country', 'Task']).count().reset_index()

plt.figure(figsize=(14, 10))
sns.scatterplot(data=task_country_year_grouped, x='Year', y='Country', size='Count', hue='Task', sizes=(20, 200))
plt.xlabel('Year')
plt.legend(title='Task', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.xticks(np.arange(min(task_country_year_grouped['Year']), max(task_country_year_grouped['Year'])+1, 1))
plt.savefig('task_year_country.png')
plt.close()

# Number of Papers per Year for Each Task (Multiple Lines Chart)
plt.figure(figsize=(14, 10))
for task in tasks:
    sns.lineplot(data=task_yearly_trends[task], label=task)

plt.ylabel('Number of Papers')
plt.xlabel('Year')
plt.legend(title='Task', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.xticks(np.arange(min(task_yearly_trends.index), max(task_yearly_trends.index)+1, 1))
plt.savefig('papers_per_year_per_task_line.png')
plt.close()


plt.figure(figsize=(14, 10))

# Creating a bar chart for each task
for task in tasks:
    plt.bar(task_yearly_trends[task].index, task_yearly_trends[task].values.flatten(), label=task, alpha=0.7)

plt.ylabel('Number of Papers')
plt.xlabel('Year')
plt.legend(title='Task', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.xticks(np.arange(min(task_yearly_trends[task].index), max(task_yearly_trends[task].index)+1, 1))
plt.savefig('papers_per_year_per_task_bar.png')
plt.close()

plt.figure(figsize=(14, 10))

# Creating a dot plot for each task
for task in tasks:
    plt.plot(task_yearly_trends[task].index, task_yearly_trends[task].values.flatten(), 'o', label=task)

plt.ylabel('Number of Papers')
plt.xlabel('Year')
plt.legend(title='Task', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()  # Adjust layout to prevent overlap
plt.xticks(np.arange(min(task_yearly_trends[task].index), max(task_yearly_trends[task].index)+1, 1))
plt.savefig('papers_per_year_per_task_dot.png')
plt.close()


tasks = task_yearly_trends.columns
years = task_yearly_trends.index

# Determine the grid size for subplots
num_tasks = len(tasks)
grid_size = int(np.ceil(np.sqrt(num_tasks)))

fig, axes = plt.subplots(grid_size, grid_size, figsize=(20, 20), sharex=True, sharey=True)
axes = axes.flatten()

# Plot each task in its own subplot
for i, task in enumerate(tasks):
    axes[i].plot(years, task_yearly_trends[task].values.flatten(), marker='o', linestyle='-')
    axes[i].set_title(task)
    axes[i].set_xticks(np.arange(min(years), max(years) + 1, 1))
    axes[i].set_xlabel('Year')
    axes[i].set_ylabel('Number of Papers')

# Hide any unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.savefig('papers_per_year_per_task_faceted.png')
plt.close()

