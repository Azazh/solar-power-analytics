import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib.cm as cm

class WindAnalysis:
    """
    A class for performing wind analysis using wind roses and radial plots.
    """

    def __init__(self, data):
        """
        Initializes the WindAnalysis class with a DataFrame.

        Parameters:
        - data (pd.DataFrame): The DataFrame containing wind speed ('WS') and wind direction ('WD') columns.
        """
        self.data = data

    def plot_wind_rose(self, wind_speed_col='WS', wind_dir_col='WD', bins=None, cmap='coolwarm'):
        """
        Plots a wind rose to show the distribution of wind speed and direction.

        Parameters:
        - wind_speed_col (str): The column name for wind speed.
        - wind_dir_col (str): The column name for wind direction.
        - bins (list): Custom bins for wind speed intervals (optional).
        - cmap (str): Colormap for the plot (default: 'coolwarm').
        """
        # Default bins if not provided
        if bins is None:
            bins = [0, 1, 2, 3, 5, 10, 15, 20]

        # Drop NaN values
        wind_data = self.data[[wind_speed_col, wind_dir_col]].dropna()

        # Ensure cmap is a colormap object
        if isinstance(cmap, str):
            cmap = cm.get_cmap(cmap)

        # Create a wind rose plot
        ax = WindroseAxes.from_ax()
        ax.bar(
            wind_data[wind_dir_col], 
            wind_data[wind_speed_col],
            normed=True, 
            bins=bins, 
            cmap=cmap
        )
        ax.set_legend()
        plt.title("Wind Rose", fontsize=16)
        plt.show()

    def plot_radial_bar(self, wind_speed_col='WS', wind_dir_col='WD', num_bins=8):
        """
        Plots a radial bar chart showing the average wind speed per direction sector.

        Parameters:
        - wind_speed_col (str): The column name for wind speed.
        - wind_dir_col (str): The column name for wind direction.
        - num_bins (int): The number of bins (sectors) to divide wind directions into.
        """
        # Drop NaN values
        wind_data = self.data[[wind_speed_col, wind_dir_col]].dropna()

        # Bin wind direction into sectors
        bin_edges = np.linspace(0, 360, num_bins + 1)
        wind_data['sector'] = pd.cut(
            wind_data[wind_dir_col], 
            bins=bin_edges, 
            labels=[f"{int(bin_edges[i])}-{int(bin_edges[i + 1])}" for i in range(num_bins)],
            right=False
        )

        # Calculate average wind speed for each sector
        sector_avg = wind_data.groupby('sector')[wind_speed_col].mean()

        # Plot radial bar chart
        angles = np.linspace(0, 2 * np.pi, num_bins, endpoint=False)
        values = sector_avg.values

        # Close the plot
        angles = np.concatenate((angles, [angles[0]]))
        values = np.concatenate((values, [values[0]]))

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
        ax.fill(angles, values, color='blue', alpha=0.5)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(sector_avg.index, fontsize=10)
        ax.set_title("Radial Bar Plot of Wind Speed by Direction", fontsize=16)
        plt.show()