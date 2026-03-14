import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CommodityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Commodity Export Dashboard")
        self.root.geometry("1000x800")

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.TOP, pady=10)
        
        tk.Button(btn_frame, text="Generate October Charts", command=lambda: self.update_dashboard('Coding Test.xlsx - Oct.csv', 'Oct')).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Generate November Charts", command=lambda: self.update_dashboard('Coding Test.xlsx - Nov.csv', 'Nov')).pack(side=tk.LEFT, padx=5)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def clean_data(self, file_path):
        # Read file, skip the first row header
        df = pd.read_csv(file_path, skiprows=1)
        # Select rows for Soybeans(3-12), Corn(17-26), Wheat(29-38) 
        # Note: Indexing starts at 0 in Python
        soy = df.iloc[3:13].copy()
        corn = df.iloc[17:27].copy()
        wheat = df.iloc[29:39].copy()
        
        # Convert values to numbers (removing commas)
        for d in [soy, corn, wheat]:
            d.iloc[:, 1] = pd.to_numeric(d.iloc[:, 1].astype(str).str.replace(',', ''), errors='coerce')
            if len(d.columns) > 2:
                d.iloc[:, 2] = pd.to_numeric(d.iloc[:, 2].astype(str).str.replace(',', ''), errors='coerce')
        
        return soy, corn, wheat

    def update_dashboard(self, file, month):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        soy, corn, wheat = self.clean_data(file)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10))
        fig.tight_layout(pad=4.0)

        if month == 'Oct':
            # October Styles: Stacked, Bar, Line
            ax1.barh(soy.iloc[:, 0], soy.iloc[:, 1], label='2024')
            ax1.barh(soy.iloc[:, 0], soy.iloc[:, 2], left=soy.iloc[:, 1], label='2025')
            ax1.set_title("Soybeans (Stacked Bar)")
            
            ax2.bar(corn.iloc[:, 0], corn.iloc[:, 1], width=0.4, label='2024', align='center')
            ax2.bar(corn.iloc[:, 0], corn.iloc[:, 2], width=0.4, label='2025', align='edge')
            ax2.set_title("Corn (Grouped Bar)")
            
            ax3.plot(wheat.iloc[:, 0], wheat.iloc[:, 1], marker='o', label='2024')
            ax3.plot(wheat.iloc[:, 0], wheat.iloc[:, 2], marker='s', label='2025')
            ax3.set_title("Wheat (Line Chart)")
        else:
            # November Styles: Pie, Horizontal Bar, Area
            ax1.pie(soy.iloc[:, 1], labels=soy.iloc[:, 0], autopct='%1.1f%%')
            ax1.set_title("Soybeans (Pie Chart)")
            
            ax2.barh(corn.iloc[:, 0], corn.iloc[:, 1], color='green')
            ax2.set_title("Corn (Horizontal Bar)")
            
            ax3.fill_between(range(len(wheat)), wheat.iloc[:, 1], color="skyblue", alpha=0.4)
            ax3.set_xticks(range(len(wheat)))
            ax3.set_xticklabels(wheat.iloc[:, 0], rotation=45)
            ax3.set_title("Wheat (Area Chart)")

        for ax in [ax1, ax2, ax3]: ax.legend(fontsize='x-small')
        
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = CommodityApp(root)
    root.mainloop()