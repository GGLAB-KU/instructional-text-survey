This repository contains the code, plots, and data associated with the paper:

**A Systematic Survey on Instructional Text: From Representation Formats to Downstream NLP Tasks**  
[https://arxiv.org/pdf/2410.18529](https://arxiv.org/pdf/2410.18529)

---

## Overview

This project accompanies our survey paper which provides a comprehensive review of the current landscape in instructional text understanding. With the recent progress in large language models (LLMs) and instruction tuning, our paper investigates the challenges of processing complex, multi-step instructions that go beyond simple command following. It offers:

- A detailed taxonomy of data representation formats used for instructional texts.
- An analysis of various downstream tasks such as summarization, event alignment, implicit instruction correction, and more.
- A discussion on the trends, challenges, and future opportunities in the field.

---

## Paper Summary

**Background:**  
While recent advances in NLP have allowed models to follow simple instructions, real-world tasks are often more complex, involving multiple interdependent steps. Understanding such multi-step instructions requires models to reason about events, actions, and their relationships in depth.

**Contributions:**  
- **Systematic Review:** We surveyed 177 papers across related domains including NLP, robotics, and business intelligence.
- **Taxonomy:** The survey categorizes instructional texts by their representation formats (e.g., unstructured, event-centric, entity-centric, symbolic) and links these formats to a variety of downstream tasks.
- **Future Directions:** The paper identifies gaps and proposes directions for future research in complex instruction understanding and processing.

For a detailed read, please refer to the paper on [arXiv](https://arxiv.org/abs/2410.18529).

---

## Repository Structure

```
instructional-text-survey/
├── data/                 # Metadata
├── plot_scripts/                # Visualizations and figures from the paper
├── README.md             # This file
```
---

## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/GGLAB-KU/instructional-text-survey.git
   cd instructional-text-survey
   ```

2. **Environment Setup:**

   We recommend using [conda](https://docs.conda.io/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/latest/) for managing dependencies. Install the required packages with:

   ```bash
   pip install -r requirements.txt
   ```

3. **Running the Code:**

   Navigate to the `plot_scripts/` directory and run the scripts as described in the accompanying documentation. For example, to generate plots:

   ```bash
   python pub_per_city.py
   ```

4. **Reproducing Experiments:**

   Detailed instructions for reproducing the experiments and analyses are provided in the `code/README.md` file within the code directory.

---

## Citation

If you find our work useful, please cite the paper as follows:

```
@misc{safa2024systematicsurveyinstructionaltext,
      title={A Systematic Survey on Instructional Text: From Representation Formats to Downstream NLP Tasks}, 
      author={Abdulfattah Safa and Tamta Kapanadze and Arda Uzunoğlu and Gözde Gül Şahin},
      year={2024},
      eprint={2410.18529},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2410.18529}, 
}
```

---

## Contributing

Contributions to the repository are welcome! If you have suggestions or improvements, please open an issue or submit a pull request. For major changes, please discuss them first via issue to ensure alignment with the project goals.

---

This README.md provides an introduction to the repository, a summary of the paper, and practical guidance on how to use and contribute to the project. Feel free to adjust the content to better match your project’s specifics or additional instructions.