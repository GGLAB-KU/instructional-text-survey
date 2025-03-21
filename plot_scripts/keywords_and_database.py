# This produces Fig. 3. Publications Per Keyword Per Database
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

keywords = [
    "'instruction manual' parsing",
    "action sequence annotation",
    "action sequence(s) natural language",
    "BPMN generation",
    "entity tracking",
    "instruction parsing",
    "instructional text",
    "natural language instruction(s)",
    "procedural text",
    "recipe parsing",
    "script knowledge",
    "wikihow",
    "entity state tracking"
]

database_counts = {
    "IEEE": np.array([1, 19, 74, 50, 14, 106, 5, 39, 6, 3, 4, 10, 0]),
    "DBLP": np.array([0, 0, 0, 17, 44, 4, 5, 125, 52, 0, 44, 11, 9]),
    "Google Scholar": np.array([98, 100, 99, 99, 100, 100, 93, 200, 97, 99, 99, 89, 33]),
}


df = pd.DataFrame(database_counts, index=keywords)

df.plot(kind='bar', stacked=True, colormap='viridis', figsize=(10, 6))

plt.xlabel('Keywords')
plt.ylabel('Number of Papers')


#plt.title('Number of Papers for Each Keyword by Database')

plt.xticks(rotation=20, ha='right', fontsize = 8)

plt.tight_layout()
plt.show()