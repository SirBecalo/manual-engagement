import os
import numpy as np
import pandas as pd
import pathlib
import glob
import kaleido
import matplotlib
import matplotlib.pyplot as plt

def generate_read_frequency(week_folder_path):
    """
    Generate the read_frequency table for a given week's folder.
    
    Parameters:
    - week_folder_path (str): Path to the folder containing the week's CSV files.
    
    Returns:
    - DataFrame: read_frequency table for the week.
    """
    # Step 1: Load CSVs from a Folder
    user_ids = [] # to eventually contain a list for each day's unique opens. (list of lists)
    for filename in os.listdir(week_folder_path): # loop over each csv from the week's folder
        if filename.endswith(".csv"): # ommit non-csvs
            file_path = os.path.join(week_folder_path, filename) # get the full file path for each csv
            day_data = pd.read_csv(file_path, usecols=[0]) # read each file's first column
            user_ids.extend(day_data.iloc[:, 0].tolist())  # convert the column to a list, append it to user_ids
    
            # now user_ids is a list of lists, each sublist containing unique opens of a specific day.

    # Step 2: Combine & Count User IDs
    user_counts = pd.Series(user_ids).value_counts()    # creates a user_counts series, counting each user's occurences. For exmaple, frequency of user X opening: 3 times a week

    # Step 3: Generate read_frequency Table
    frequency_series = user_counts.value_counts()   # creates a table for frquency of frequencies. For example: frequency of opening 5 times: 1000.
    frequency_series.name = "tally"  # Explicitly setting the name to avoid naming collisions
    frequency_df = frequency_series.reset_index() 
    print(frequency_series.index)

    frequency_df.columns = ["frequency", "tally"]
    frequency_df["percentage"] = (frequency_df["tally"] / frequency_df["tally"].sum()) * 100
    frequency_df = frequency_df.sort_values(by="frequency").reset_index(drop=True)
    
    return frequency_df # This function can now be called for each week's folder to get the corresponding read_frequency table
def visualize_weekly_engagement(week_folder_paths, img_name):
    """
    Generate a stacked bar chart representing email open frequency for multiple weeks 
    with consistent coloring and folder names as x-axis labels.
    
    Parameters:
    - week_folder_paths (list): A list of folder paths for each week.
    
    Returns:
    - Displays the stacked bar chart.
    """
    
    # Color map for frequencies
    color_map = {
        1: "#1f77b4",  # blue
        2: "#ff7f0e",  # orange
        3: "#2ca02c",  # green
        4: "#d62728",  # red
        # ... add more colors if expecting higher frequencies
    }
    
    # Gather data for each week
    weekly_data = [generate_read_frequency(path) for path in week_folder_paths]
    
    # Extracting folder names from paths for x-axis labels
    folder_names = [os.path.basename(path) for path in week_folder_paths]
    
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))
    for week_index, data in enumerate(weekly_data):
        bottom_value = 0  # To stack bars
        for _, row in data.iterrows():
            label = f"Frequency {row['frequency']}" if week_index == 0 else ""  # Avoid duplicate labels
            ax.bar(week_index, row['tally'],bottom=bottom_value, label=label, color=color_map.get(row['frequency'], "#333333"))
            # Adding percentage text inside bars
            ax.text(week_index, bottom_value + (0.5 * row['tally']), f"{row['percentage']:.2f}%", 
                    ha='center', va='center', color='white', fontsize=10)
            ax.set_xlim(-1,6) #makes the x axis scale fixed, to fit 6 bars even when there are less. this way, the bars are not "Scaled in" when you have less than 6 weeks being displayed

            bottom_value += row['tally']
        # Labeling total tally on top of each bar
        ax.text(week_index, bottom_value, str(int(bottom_value)), ha='center', va='bottom', color='black', fontsize=10)
    
    # Adjusting the plot
    ax.set_xticks(range(len(week_folder_paths)))
    ax.set_xticklabels(folder_names)
    ax.set_ylabel("Number of Users")
    ax.set_title("Weekly Email Open Frequencies")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], title="Open Frequency", loc='upper center', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(img_name)  
def visualize_combined_engagement(en_week_folders, ar_week_folders, img_name):
    """
    Generate a stacked bar chart representing email open frequency for multiple weeks 
    with a distinct color scheme for English and Arabic data.
    
    Parameters:
    - en_week_folders (list): A list of folder paths for each English week.
    - ar_week_folders (list): A list of folder paths for each Arabic week.
    - img_name (str): Name of the image file to save the plot.
    
    Returns:
    - Displays the stacked bar chart.
    """
    
    # Distinct Color map for EN and AR frequencies
    en_color_map = {
        1: "#add8e6",  # light blue
        2: "#1f77b4",  # medium blue
        3: "#1565c0",  # darker blue
        4: "#0d47a1"   # darkest blue
    }
    
    ar_color_map = {
        1: "#90ee90",  # light green
        2: "#2ca02c",  # medium green
        3: "#008000",  # darker green
        4: "#006400"   # darkest green
    }
    
    # Combine EN and AR folders and label names
    combined_folders = en_week_folders + ar_week_folders
    en_labels = [os.path.basename(path) + " EN" for path in en_week_folders]
    ar_labels = [os.path.basename(path) + " AR" for path in ar_week_folders]
    combined_labels = en_labels + ar_labels
    
    # Gather data for each week
    weekly_data = [generate_read_frequency(path) for path in combined_folders]
    
    # Plotting
    fig, ax = plt.subplots(figsize=(15, 8))
    for week_index, data in enumerate(weekly_data):
        bottom_value = 0  # To stack bars
        color_map = en_color_map if week_index < len(en_week_folders) else ar_color_map
        for _, row in data.iterrows():
            ax.bar(week_index, row['tally'], bottom=bottom_value, color=color_map.get(row['frequency'], "#333333"))
            # Adding percentage text inside bars
            ax.text(week_index, bottom_value + (0.5 * row['tally']), f"{row['percentage']:.2f}%", 
                    ha='center', va='center', color='white', fontsize=10)
            bottom_value += row['tally']
        # Labeling total tally on top of each bar
        ax.text(week_index, bottom_value, str(int(bottom_value)), ha='center', va='bottom', color='black', fontsize=10)
    
    # Adjusting the plot
    ax.set_xticks(range(len(combined_folders)))
    ax.set_xticklabels(combined_labels, rotation=45)
    ax.set_ylabel("Number of Users")
    ax.set_title("Weekly Email Open Frequencies (EN & AR)")
    plt.tight_layout()
    plt.savefig(img_name)
    
    # The function is now updated with a distinct color scheme for English and Arabic data.


#Step 1: Create a new subfolder inside weeks/ar, weeks/en, and weeks_saudi. the folder name should be the first day of the engagment week (open weeks/ar and weeks/en to see previous example)
#Step 2: download the previous week's files from Braze
#Step 3: place the english files into weeks/en/(your new subfolder) and the arabic files into weeks/ar/(your new subfolder), and Saudi files into weeks_saudi/(your new subfolder)
#Step 4: Below, Add the new subfolder name as the last line in each of the 3 lists 
#Step 4.1: should be added like the previous line, aka "weeks/en/(your subfoler name)" for example
EG_en_week_folders = [
    "weeks/EG/en/apr21",
    "weeks/EG/en/apr28",
    "weeks/EG/en/may7",
    "weeks/EG/en/may12",
    "weeks/EG/en/may19",
    "weeks/EG/en/may26",
]

EG_ar_week_folders = [
    "weeks/EG/ar/apr21",
    "weeks/EG/ar/apr28",
    "weeks/EG/ar/may7",
    "weeks/EG/ar/may12",
    "weeks/EG/ar/may19",
    "weeks/EG/ar/may26",
]

KSA_ar_week_folders = [
    "weeks/KSA/ar/apr21",
    "weeks/KSA/ar/apr28",
    "weeks/KSA/ar/may5",
    "weeks/KSA/ar/may12",
    "weeks/KSA/ar/may19",
    "weeks/KSA/ar/may26",
]
KSA_en_week_folders = [
    "weeks/KSA/en/apr21",
    "weeks/KSA/en/apr28",
    "weeks/KSA/en/may5",
    "weeks/KSA/en/may12",
    "weeks/KSA/en/may19",
    "weeks/KSA/en/may26",
]


#Step 5: edit the  quotation marks in each of the 4 lines below (such as "Latest/EN_Engagment_jan21") to the right date. so if its jan21 it will be jan 28, if its feb4 it will be feb11
visualize_weekly_engagement(EG_en_week_folders, "latest/EG_EN_may26")
visualize_weekly_engagement(EG_ar_week_folders, "latest/EG_AR_may26")
visualize_weekly_engagement(KSA_en_week_folders, "latest/KSA_EN_may26")
visualize_weekly_engagement(KSA_ar_week_folders, "latest/KSA_AR_may26")
#visualize_combined_engagement(en_week_folders, ar_week_folders, "latest/Combined_Engagement_feb18")

