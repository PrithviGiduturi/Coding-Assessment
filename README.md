This is the README for the Coding Assessment for USDA Commodities

This USDA Market Analysis is for the commodities soybeans, corn, and wheat. 

I have built an interactive tool where you can select multiple buttons to display trends on the Jan-Oct months of 2024 and 2025, for the Oct dataset, and Jan-Nov for the Nov dataset. Based on the instructions, the features of this interactive design utilize a tkinter dashboard for the Oct and Nov buttons, while having side-by-side charts for each commodity. 

The requirements for this task are as follows:
- Python 3.8+
- Panda library
- Matplotlib
- Openpyxl


Set up and Run Process:
1. Either clone the repository or download the files onto your computer. 
2. Then, install the dependencies, which are the bash command:  pip install pandas matplotlib openpyxl
3. Then, create a folder on your file explorer to contain all three files (main.py, readme.md, and Coding Test.xlsx)
4. Next, utilize either the command prompt or VSCode to run the main.py file by changing the command cd to the specific folder. 
5. Finally, run the command: python main.py to run the file and click the buttons to display the output for both datasets.

Assumptions & Notes
- Cotton wasn't noted. As the source file was referencing cotton, there wasn’t any data present in the Excel file. Thus, I only visualized soybeans, corn, and wheat. 
- There wasn’t any November 2025 data available for the November dataset. The November dataset only contained the November 2024 timeline, so that data was explicitly used. 
- Minor nuances such as wheat (unmilled) were also considered as wheat in the chart since there weren’t 2 types of wheat, removing it for brevity. 
- All values are in metric tonnes as provided in the source data, which are labeled as M. 
