import tkinter as tk

import matplotlib.pyplot as plt
import pandas as pd


class SHOW_RESULTS():

    def __init__(self, account):
        self.root = tk.Tk()
        self.root.geometry("350x100")
        self.list = []
        self.accout = account

        button = tk.Button(self.root, background="red", text="Good")
        button.place(x=130, y=50)

    def read_csv_data(self):
        """Read csvfile
        Args:
        Returns:
            list: csv data
        """
        data = pd.read_csv(f'{self.account}_instagram_api_result.csv',
                           encoding='UTF-8')


gui = SHOW_RESULTS()
gui.root.mainloop()
