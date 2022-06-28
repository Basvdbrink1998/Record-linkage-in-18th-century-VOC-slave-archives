# Record linkage in 18th century VOC slave archives

## General info
This repository contains code used during my masters thesis: Entry linking in 18th century VOC slave archives.

## Technologies used
All code is written in Python 3.6

Most code is written iside Python notebooks using Jupyter notebook

All requirements can be found in requirements.txt

## Top-level directory layout

    .
    ├── Annotation                            # Contains most code to annotate matches.
    │   ├── Annotation_helper.py              # Contains helper functions used by the other notebooks.
    │   ├── Automated_annotation.ipynb        # Contains the automatic record linkage methods using string similarities.
    │   ├── Blocking.ipynb                    # Contains tests for blocking parameters.
    │   ├── Calculate distances.ipynb         # Calculates string similarities between two datasets.
    │   ├── EDA.ipynb                         # Performs Exploratory data analysis of the data and distances and generates figures.
    │   ├── Embedding.ipynb                   # Contains the automatic record linkage methods using word embeddings.
    ├── Figures                               # Contains all figures generated by the code.
    ├── Models                                # Contains Models generated by the code.
    ├── requirements.txt                      # Contains all used python packages.
    ├── LICENSE
    └── README.md

