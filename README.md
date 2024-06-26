# Manual Coding Helper GUI for Text Classification
This project is a simple Python GUI tool designed to assist with manual classification of segmented text data stored in Excel or CSV files. The motivation behind this project was to provide a user-friendly alternative for creating training data for machine learning tasks, avoiding the complexities of Doccano (https://github.com/doccano/doccano) or tedious manual spreadsheet work.

![image](https://github.com/harrytyp/manual-coding-helper/assets/125975248/b5522b82-cc19-42ea-ae20-15823effa74c)


# Features
- User-Friendly Interface: A straightforward GUI designed to streamline the process of annotating and classifying text data in csv and xlsx format.
- Customizable: Easily adaptable to different datasets by configuring JSON files with specific codes and descriptions. Select your columns to display.
- Navigation Controls: Navigate through rows of data, update annotations, and manage classification status with buttons and keyboard shortcuts.
- Font Size Adjustment: Ability to customize the font size for better readability.
- Dark Mode Support: Toggle between light and dark modes for optimal viewing experience.

# Planned Features (in that order)
- Improve label editor
- Setting persistence between sessions
- Re-Implement a Correct/Incorrect Toggle
- Color Customization
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

### JSON File
The JSON file (labels.json) is used for configuring codes, descriptions, and category mappings. Update these files according to your dataset's classification needs or use the rudimentary editor in the GUI under settings.

### Display to be coded
Change the column to be displayed/to be coded under Settings -> Select columns to display.

# Contributing
Contributions to enhance this tool are welcome! Feel free to open issues, submit pull requests, or suggest improvements.

# License
tbd
