import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_path = '/Users/ravimore/Library/CloudStorage/Dropbox/Reanalysis_29_trios_paper_revision/Tables_Figs_Suppl/s3.xlsx'
raw = pd.read_excel(file_path, header=None)
header_rows = raw.iloc[:4]
data_rows = raw.iloc[4:].reset_index(drop=True)

# Combine multirow header
col_names = []
for col_idx in range(raw.shape[1]):
    parts = []
    for row_idx in range(4):
        value = header_rows.iloc[row_idx, col_idx]
        if pd.notna(value):
            parts.append(str(value).strip())
    col_name = '_'.join(part.replace(' ', '_').replace('#', '').replace('(', '').replace(')', '') for part in parts)
    col_name = col_name.replace('__', '_')
    col_names.append(col_name)

df = data_rows.copy()
df.columns = col_names

# Convert numerics
for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Extract series
phase = df['Reanalysis_Phases'].astype(int)
A_per_trio_static = df['Method-A_differential_cost_Per_trio_Static_cost_GBP']
B_per_trio_static = df['Method-B_differential_cost_Per_trio_Static_cost_GBP']
A_per_trio_fold = df['Method-A_differential_cost_Per_trio_10-fold_decrease_GBP']
B_per_trio_fold = df['Method-B_differential_cost_Per_trio_2-fold_decrease_GBP']
A_cum_static = df['Method-A_differential_cumulative_cost_Per_trio_Static_cost_GBP']
B_cum_static = df['Method-B_differential_cumulative_cost_Per_trio_Static_cost_GBP']
A_cum_fold = df['Method-A_differential_cumulative_cost_Per_trio_10-fold_decrease_GBP']
B_cum_fold = df['Method-B_cumulative_differential_cost_Per_trio_2-fold_decrease_GBP']

fig, axs = plt.subplots(2, 2, figsize=(14, 9))

# 1. Static cost bar chart
bar1 = axs[0, 0].bar(phase - 0.15, A_per_trio_static, width=0.3, label='Method A', color='#1f77b4')
bar2 = axs[0, 0].bar(phase + 0.15, B_per_trio_static, width=0.3, label='Method B', color='#ff7f0e')
axs[0, 0].set_title('Per‑trio static cost (GBP)')
axs[0, 0].set_xlabel('Reanalysis phase')
axs[0, 0].set_ylabel('Cost (GBP)')
axs[0, 0].set_xticks(phase)
axs[0, 0].legend(loc='upper left', bbox_to_anchor=(1.02, 1))

# Annotate values on top of bars — precisely at bar height
for b in bar1 + bar2:
    height = b.get_height()
    axs[0, 0].text(
        b.get_x() + b.get_width() / 2,
        height,
        f'{height:.0f}',
        ha='center',
        va='bottom',
        fontsize=9
    )


# 2. Fold‑reduction bar chart
bar3 = axs[0, 1].bar(phase - 0.15, A_per_trio_fold, width=0.3, label='Method A (10‑fold)', color='#1f77b4')
bar4 = axs[0, 1].bar(phase + 0.15, B_per_trio_fold, width=0.3, label='Method B (2‑fold)', color='#ff7f0e')
axs[0, 1].set_title('Per‑trio fold‑reduction cost')
axs[0, 1].set_xlabel('Reanalysis phase')
axs[0, 1].set_ylabel('Cost (GBP)')
axs[0, 1].set_xticks(phase)
axs[0, 1].legend(loc='upper left', bbox_to_anchor=(1.02, 1))

# Annotate bar tops precisely
for b in bar3 + bar4:
    height = b.get_height()
    axs[0, 1].text(
        b.get_x() + b.get_width() / 2,
        height,
        f'{height:.0f}',
        ha='center',
        va='bottom',
        fontsize=9
    )

# 3. Cumulative static line plot
axs[1, 0].plot(phase, A_cum_static, marker='o', label='Method A', color='#1f77b4')
axs[1, 0].plot(phase, B_cum_static, marker='o', label='Method B', color='#ff7f0e')
axs[1, 0].set_title('Cumulative static cost per trio (GBP)')
axs[1, 0].set_xlabel('Reanalysis phase')
axs[1, 0].set_ylabel('Cumulative cost (GBP)')
axs[1, 0].set_xticks(phase)
axs[1, 0].legend(loc='upper left', bbox_to_anchor=(1.02, 1))
axs[1, 0].margins(x=0.1, y=0.3)
for x, y in zip(phase, A_cum_static):
    axs[1, 0].text(x, y + 300, f'{y:.0f}', ha='center', fontsize=9)
for x, y in zip(phase, B_cum_static):
    axs[1, 0].text(x, y + 300, f'{y:.0f}', ha='center', fontsize=9)

# 4. Cumulative fold-reduction line plot
axs[1, 1].plot(phase, A_cum_fold, marker='o', label='Method A (10‑fold)', color='#1f77b4')
axs[1, 1].plot(phase, B_cum_fold, marker='o', label='Method B (2‑fold)', color='#ff7f0e')
axs[1, 1].set_title('Cumulative fold‑reduction cost per trio')
axs[1, 1].set_xlabel('Reanalysis phase')
axs[1, 1].set_ylabel('Cumulative cost (GBP)')
axs[1, 1].set_xticks(phase)
axs[1, 1].legend(loc='upper left', bbox_to_anchor=(1.02, 1))
axs[1, 1].margins(x=0.1, y=0.3)
for x, y in zip(phase, A_cum_fold):
    axs[1, 1].text(x, y + 300, f'{y:.0f}', ha='center', fontsize=9)
for x, y in zip(phase, B_cum_fold):
    axs[1, 1].text(x, y + 300, f'{y:.0f}', ha='center', fontsize=9)

# Adjust layout for outer spacing
plt.tight_layout(pad=3.0)
plt.subplots_adjust(right=0.85, bottom=0.08, top=0.92)

# Save and show
fig.savefig('per_trio_comparison_spaced.png', bbox_inches='tight')
plt.show()
