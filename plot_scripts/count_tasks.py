import pandas as pd
import matplotlib.pyplot as plt

# Replace 'data.tsv' with your actual file path
file_path = 'data.tsv'

# Load data from file into pandas DataFrame
df = pd.read_csv(file_path, sep='\t', header=None)

# Extract values starting with TASK: and count occurrences
task_counts = {}
for index, row in df.iterrows():
    for value in row:
        if isinstance(value, str) and value.startswith('TASK:'):
            task = value.split('TASK:')[1].strip()
            # Remove [TO REVIEW] from task label
            if task in task_counts:
                task_counts[task] += 1
            else:
                task_counts[task] = 1

# Convert dictionary to a DataFrame for plotting
task_counts_df = pd.DataFrame(list(task_counts.items()), columns=['TASK', 'Count'])

# Plotting a donut chart with legend and without percentages
labels = task_counts_df['TASK']
sizes = task_counts_df['Count']
colors = plt.cm.Dark2.colors  # Using Dark2 colormap for variety of colors

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(sizes, labels=None, colors=colors, startangle=90, pctdistance=0.85, autopct='')
centre_circle = plt.Circle((0,0),0.70,fc='white')  # Draw a white circle at the center to make it a donut chart
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')  

# Create legend with task labels and colors, smaller size
ax.legend(wedges, labels, title='TASK Types', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize='xx-small')

plt.title('Distribution of TASK Types')
plt.tight_layout()

# Save the chart to a file (change 'donut_chart.png' to your desired filename and format)
plt.savefig('donut_chart.png', dpi=300)  # Save as PNG with 300 DPI resolution
plt.show()
