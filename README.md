# Manual Coding Helper GUI for Text Classification
This project is a simple Python GUI tool designed to assist with manual classification of segmented text data stored in Excel or CSV files. The motivation behind this project was to provide a user-friendly alternative for creating training data for machine learning tasks, avoiding the complexities of Doccano (https://github.com/doccano/doccano) or tedious manual spreadsheet work.

![image](https://github.com/harrytyp/manual-coding-helper/assets/125975248/049f7dee-4268-486e-b0e0-d1d2eb29ba2d)


# Features
- User-Friendly Interface: A straightforward GUI designed to streamline the process of annotating and classifying text data.
- Customizable: Easily adaptable to different datasets by configuring JSON files with specific codes and descriptions.
- Navigation Controls: Navigate through rows of data, update annotations, and manage classification status with buttons and keyboard shortcuts.
- Font Size Adjustment: Ability to customize the font size for better readability.
- Dark Mode Support: Toggle between light and dark modes for optimal viewing experience.

# Known Bugs
- No focus on the main page after loading the dataset: Tab out and in after loading it
- Correct toggle does is bugged

# Planned Features
- Merging the json files into one
- Being able to see and set the categories, category values and category descriptions within the GUI
- selection screen for the column that is to be coded
- Multi-Label classification support

# Not Planned Features
- Span annotations. This is only for table-based manual classification

# Getting Started

Prerequisites
- Python 3.x installed on your system.
- Required Python packages can be installed using pip:
```pip install pandas ttkbootstrap```

# Installation and Usage

Clone the repository:

```git clone https://github.com/your-username/manual-coding-helper.git```

```cd manual-coding-helper```

Run the application:

```python manual_coding_gui.py```

Select your dataset file (in Excel or CSV format) when prompted.
Use the GUI to navigate through your data and annotate classifications. Your process is automatically saved. For best performance, use csv.

# Configuration

### JSON Files
Two JSON files (descriptive_sentences.json and category_mapping.json) are used for configuring codes, descriptions, and category mappings. Update these files according to your dataset's classification needs.

### Display Customization
Modify the display_row function in the code to specify the column you want to display within the GUI interface. (Replace 'sentence_text')

# Contributing
Contributions to enhance this tool are welcome! Feel free to open issues, submit pull requests, or suggest improvements.

# License
tbd
