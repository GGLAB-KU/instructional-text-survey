#This file procdues Fig.5 a: Papers Per Task Distribution over Time
import pandas as pd
import matplotlib.pyplot as plt

# Load data from TSV file
df = pd.read_csv('data.tsv', sep='\t')

# Combine tag columns into a single column with multiple tags per paper
tags = df.melt(id_vars='year', value_vars=['tag0','tag1','tag2','tag3','tag4','tag5','tag6','tag7','tag8','tag9',
                                            'tag10','tag11','tag12','tag13','tag14','tag15','tag16','tag17','tag18',
                                            'tag19','tag20','tag21','tag22'], 
                var_name='tag_type', value_name='task').dropna()

# Remove 'TASK:' prefix from the task labels
tags = tags[tags['task'].str.startswith('TASK:')]
tags['task'] = tags['task'].str.replace('TASK:', '', regex=False)

# Function to format task names and merge Grounded tasks
def format_task_name(name, word_limit=3):
    if name.startswith("Grounded"):
        return "Grounded Tasks"  # Merge all "Grounded" tasks into "Grounded Tasks"
    words = name.split()
    if len(words) > word_limit:
        first_line = ' '.join(words[:word_limit])
        second_line = ' '.join(words[word_limit:])
        return f'{first_line}\n{second_line}'
    return name

# Apply formatting function
tags['task'] = tags['task'].apply(format_task_name)

# Count occurrences of each task per year
task_counts = tags.groupby(['year', 'task']).size().unstack(fill_value=0)

# Transpose the data for plotting
task_counts = task_counts.T

# Create a scatter plot
plt.figure(figsize=(12, 8))

# Determine a scaling factor for circle sizes
scaling_factor = 1000 / task_counts.max().max()

for task in task_counts.index:
    sizes = task_counts.loc[task] * scaling_factor  
    non_zero_indices = sizes > 0
    years = task_counts.columns[non_zero_indices]
    sizes = sizes[non_zero_indices]
    
    if not years.empty:
        plt.scatter(years, [task] * len(years), s=sizes, alpha=0.6, edgecolor='w', c='#008080')

        # Add labels inside the circles
        for year, size in zip(years, sizes):
            plt.text(year, task, str(int(size / scaling_factor)), 
                     ha='center', va='center', fontsize=12, color='black')

# Add grid and format axes
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(ticks=range(int(task_counts.columns.min()), int(task_counts.columns.max()) + 1, 1), 
           fontsize=18, rotation=45)
plt.yticks(fontsize=18)
plt.tight_layout()

# Save and show plot
plt.savefig('task_year_avg.png')
plt.show()
