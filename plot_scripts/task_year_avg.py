import pandas as pd
import matplotlib.pyplot as plt

# Load data from TSV file
df = pd.read_csv('data.tsv', sep='\t')

# Combine tag columns into a single column with multiple tags per paper
tags = df.melt(id_vars='year', value_vars=['tag 1', 'tag 2', 'tag 3'], var_name='tag_type', value_name='task').dropna()

# Remove 'TASK:' prefix from the task labels
tags['task'] = tags['task'].str.replace('TASK:', '', regex=False)

# Create a function to format task names with line breaks after the third word
def format_task_name(name, word_limit=3):
    words = name.split()
    if len(words) > word_limit:
        # Split into two lines: the first line with up to `word_limit` words, and the rest on the second line
        first_line = ' '.join(words[:word_limit])
        second_line = ' '.join(words[word_limit:])
        return f'{first_line}\n{second_line}'
    return name

# Apply the function to format task names
tags['task'] = tags['task'].apply(format_task_name)

# Count occurrences of each task per year
task_counts = tags.groupby(['year', 'task']).size().unstack(fill_value=0)

# Transpose the data for the desired axis arrangement
task_counts = task_counts.T

# Create a scatter plot
plt.figure(figsize=(12, 8))

# Determine a scaling factor to fit the circle sizes within the plot
scaling_factor = 1000 / task_counts.max().max()  # Adjust this factor as needed

for task in task_counts.index:
    sizes = task_counts.loc[task] * scaling_factor  # Scale the circle size by a factor
    
    # Filter out zero sizes
    non_zero_indices = sizes > 0
    years = task_counts.columns[non_zero_indices]
    sizes = sizes[non_zero_indices]
    
    if not years.empty:
        plt.scatter(years, [task] * len(years), s=sizes, alpha=0.6, edgecolor='w', c='#008080')  # Teal color

        # Add labels inside the circles with increased font size
        for year, size in zip(years, sizes):
            plt.text(year, task, str(int(size / scaling_factor)), 
                     ha='center', va='center', fontsize=12, color='black')  # Increased fontsize

# Add grid with dotted lines
plt.grid(True, linestyle='--', alpha=0.7)

# Format x-axis to show integer years with increased font size and rotation
plt.xticks(ticks=range(int(task_counts.columns.min()), int(task_counts.columns.max()) + 1, 1), 
           fontsize=12, rotation=45)

# Increase font size of y-axis labels (task names) and axis labels
plt.yticks(fontsize=14)
plt.xlabel('Year', fontsize=16)  # Increased font size for x-axis label
plt.ylabel('Task', fontsize=16)   # Increased font size for y-axis label

# plt.title('Task Frequency by Year', fontsize=18)  # Increased font size for title
plt.tight_layout()

# Save the figure before showing it
plt.savefig('task_year_avg.png')

# Show the plot
plt.show()
