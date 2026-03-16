import pandas as pd
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CommodityDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("USDA Commodity Dashboard")
        self.root.geometry("1000x850")
        self.excel_file = 'Coding Test.xlsx'

        tk.Label(root, text="Export Market Analysis", font=("Arial", 18, "bold")).pack(pady=10)
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Analyze October", command=lambda: self.update_dashboard('Oct'),
                  width=25, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Analyze November", command=lambda: self.update_dashboard('Nov'),
                  width=25, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def clean_data(self, sheet_name):
        try:
            df = pd.read_excel(self.excel_file, sheet_name=sheet_name, header=None)

            def extract(start_row):
                block = df.iloc[start_row:start_row + 10].copy()
                countries = block.iloc[:, 0].astype(str)
                val_2024  = pd.to_numeric(block.iloc[:, 1], errors='coerce')
                val_2025  = pd.to_numeric(block.iloc[:, 2], errors='coerce') \
                            if block.shape[1] > 2 else pd.Series([None] * 10)
                return pd.DataFrame({'Market': countries,
                                     '2024': val_2024,
                                     '2025': val_2025}).dropna(subset=['Market'])

            soy   = extract(5)
            corn  = extract(17)
            wheat = extract(29)

            return soy, corn, wheat

        except Exception as e:
            messagebox.showerror("Error", f"Data Error: {e}")
            return None, None, None

    def update_dashboard(self, sheet_name):
        soy, corn, wheat = self.clean_data(sheet_name)
        if soy is None or soy.empty:
            messagebox.showwarning("Warning", "No data found.")
            return

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        has_2025 = soy['2025'].notna().any()
        period   = "Jan–Oct" if sheet_name == "Oct" else "Jan–Nov"

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 11))
        fig.suptitle(f'Top 10 U.S. Export Markets — {period} 2024'
                     + (' vs 2025' if has_2025 else ''),
                     fontsize=14, fontweight='bold')

        combos = [
            (ax1, soy,   "Soybeans",       "#2d6a4f", "#74c69d"),
            (ax2, corn,  "Corn",            "#e9c46a", "#f4a261"),
            (ax3, wheat, "Wheat",           "#264653", "#457b9d"),
        ]

        for ax, data, title, color_24, color_25 in combos:
            markets = data['Market']
            x = range(len(markets))
            width = 0.4

            if has_2025:
                ax.bar([i - width/2 for i in x], data['2024'], width,
                       label='2024', color=color_24)
                ax.bar([i + width/2 for i in x], data['2025'], width,
                       label='2025', color=color_25)
                ax.legend(fontsize=8)
            else:
                ax.bar(x, data['2024'], color=color_24)

            ax.set_title(f"{title} (Metric Tons)", fontsize=11, fontweight='bold')
            ax.set_xticks(list(x))
            ax.set_xticklabels(markets, rotation=20, ha='right', fontsize=8)
            ax.set_ylabel("Volume (Metric Tons)")
            ax.yaxis.set_major_formatter(
                plt.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M"))
            ax.grid(axis='y', linestyle='--', alpha=0.4)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CommodityDashboard(root)
    root.mainloop()
