import pandas as pd

# Step 1: Read the data from data.tsv into a DataFrame
file_path = 'data.tsv'
df = pd.read_csv(file_path, sep='\t')

# Step 2: Initialize a dictionary to store data and associated tasks
data_tasks = {}

# Step 3: Iterate over each row to extract data and tasks
for index, row in df.iterrows():
    # Initialize variables to store data and tasks
    data = None
    tasks = set()  # Use a set to ensure unique tasks
    
    # Iterate over each column to find DATA: and TASK: tags
    for col_name, value in row.items():
        if not isinstance(value, str):
            continue
        if value.startswith('DATA:'):
            data = value.replace('DATA:', '').strip()
        elif value.startswith('TASK:'):
            tasks.add(value.replace('TASK:', '').strip())
    
    # If data and tasks are found, store them in data_tasks dictionary
    if data and tasks:
        if data in data_tasks:
            data_tasks[data].update(tasks)  # Use update() to add all elements of tasks to the set
        else:
            data_tasks[data] = tasks

# Step 4: Print the results
for data, tasks in data_tasks.items():
    print(f"DATA: {data} -> UNIQUE TASKS: {tasks}")
