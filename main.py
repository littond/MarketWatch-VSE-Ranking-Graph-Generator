import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime

# Path to folder containing CSVs
RESOURCE_DIR = './resources'
MILLION = 1_000_000

# Dictionary to store net worth history
# Format: { "Name": {date1: net_worth, date2: net_worth, ...} }
net_worth_history = {}

# Go through each file in the folder
files = sorted(os.listdir(RESOURCE_DIR), reverse=False)
print("files:", files)
for filename in files:
    if filename.endswith(".csv"):
        filepath = os.path.join(RESOURCE_DIR, filename)
        date_str = filename.split(".")[0]  # Assumes filename is like 'mm-dd.csv'
        try:
            date = datetime.strptime(date_str, "%m-%d").date()
        except ValueError:
            continue  # Skip files that don't match the date format

        df = pd.read_csv(filepath, quotechar='"', on_bad_lines='skip')

        for _, row in df.iterrows():
            name = row["Name"].strip().lower()
            net_worth_str = row["Net Worth"].replace("$", "").replace(",", "")
            try:
                net_worth = float(net_worth_str)/MILLION
            except ValueError:
                continue

            if name not in net_worth_history:
                net_worth_history[name] = {}
            net_worth_history[name][date] = net_worth

# Convert to DataFrame for plotting
df_plot = pd.DataFrame(net_worth_history)

# Plot
plt.figure()
include_all = True
for name in sorted(df_plot.columns):
    print(name)
    if include_all:
        plt.plot(df_plot.index, df_plot[name], label=name.title())
    else:
        if name != "michael ruiz" and name != "lucy mcgovern":
            plt.plot(df_plot.index, df_plot[name], label=name.title())

plt.title("Artisan Partners VSE Intern Game Networth Analysis")
plt.xlabel("Date")
plt.ylabel("Net Worth (Millions)")

ax = plt.gca()
ax.set_xticks(df_plot.index)  # set positions
ax.set_xticklabels([d.strftime("%m-%d") for d in df_plot.index])  # set labels
ax.tick_params(axis='x', rotation=45)

plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1), borderaxespad=0.)
plt.tight_layout()
plt.grid(True)

os.makedirs("out", exist_ok=True)
if include_all:
    file_name = "out/" + str(files[-1]).split(".")[0] + ".png"
else:
    file_name = "out/" + str(files[-1]).split(".")[0] + "-no-m-or-l.png"

plt.savefig(file_name, dpi=300, bbox_inches='tight')

plt.show()