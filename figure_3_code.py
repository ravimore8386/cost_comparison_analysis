import pandas as pd
import matplotlib.pyplot as plt

# === Load Excel File ===
file_path = '/Users/Supplementary_Table_3.xlsx'
raw = pd.read_excel(file_path, header=None)

# === Process header and data ===
header_rows = raw.iloc[:4]
data_rows = raw.iloc[4:].reset_index(drop=True)

# Build header
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
for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

phase = df['Reanalysis_Phases'].astype(int)

# === Extract required columns ===
A_per_trio_static = df['Method-A_differential_cost_Per_trio_Static_cost_GBP']
B_per_trio_static = df['Method-B_differential_cost_Per_trio_Static_cost_GBP']
A_per_trio_fold = df['Method-A_differential_cost_Per_trio_10-fold_decrease_GBP']
B_per_trio_fold = df['Method-B_differential_cost_Per_trio_2-fold_decrease_GBP']
A_cum_static = df['Method-A_differential_cumulative_cost_Per_trio_Static_cost_GBP']
B_cum_static = df['Method-B_differential_cumulative_cost_Per_trio_Static_cost_GBP']
A_cum_fold = df['Method-A_differential_cumulative_cost_Per_trio_10-fold_decrease_GBP']
B_cum_fold = df['Method-B_cumulative_differential_cost_Per_trio_2-fold_decrease_GBP']

A_UK_cum_static = df['Method-A_cumulative_differential_cost_UK_RD_NICU/PICU_trios_Static_cost_Million_GBP']
B_UK_cum_static = df['Method-B_cumulative_differential_cost_UK_RD_NICU/PICU_trios_Static_cost_Million_GBP']
A_UK_cum_fold = df['Method-A_cumulative_differential_cost_UK_RD_NICU/PICU_trios_10-fold_decrease_Million_GBP']
B_UK_cum_fold = df['Method-B_cumulative_differential_cost_UK_RD_NICU/PICU_trios_2-fold_decrease_Million_GBP']

# === Create 2x3 plot layout ===
fig, axs = plt.subplots(2, 3, figsize=(18, 9))
axs = axs.flatten()

# A. Per-trio static cost (legend moved outside)
axs[0].bar(phase - 0.15, A_per_trio_static, width=0.3, label='Method A', color='#1f77b4')
axs[0].bar(phase + 0.15, B_per_trio_static, width=0.3, label='Method B', color='#ff7f0e')
axs[0].set_title('Per-trio static cost (GBP)')
axs[0].set_xlabel('Reanalysis phase')
axs[0].set_ylabel('Cost (GBP)')
axs[0].set_xticks(phase)
axs[0].legend(loc='center left', bbox_to_anchor=(1.02, 0.5))  # moved legend outside
for x, y in zip(phase, A_per_trio_static): axs[0].text(x - 0.15, y, f'{y:.0f}', ha='center', va='bottom', fontsize=8)
for x, y in zip(phase, B_per_trio_static): axs[0].text(x + 0.15, y, f'{y:.0f}', ha='center', va='bottom', fontsize=8)

# B. Cumulative static cost per trio
axs[1].plot(phase, A_cum_static, marker='o', label='Method A', color='#1f77b4')
axs[1].plot(phase, B_cum_static, marker='o', label='Method B', color='#ff7f0e')
axs[1].set_title('Cumulative static cost per trio (GBP)')
axs[1].set_xlabel('Reanalysis phase')
axs[1].set_ylabel('Cumulative cost (GBP)')
axs[1].set_xticks(phase)
axs[1].legend()
for x, y in zip(phase, A_cum_static): axs[1].text(x, y + 300, f'{y:.0f}', ha='center', fontsize=8)
for x, y in zip(phase, B_cum_static): axs[1].text(x, y + 300, f'{y:.0f}', ha='center', fontsize=8)

# C. UK cumulative static cost
axs[2].plot(phase, A_UK_cum_static, marker='o', label='Method A', color='#1f77b4')
axs[2].plot(phase, B_UK_cum_static, marker='o', label='Method B', color='#ff7f0e')
axs[2].set_title('Cumulative static cost for UK RD trios')
axs[2].set_xlabel('Reanalysis phase')
axs[2].set_ylabel('Cumulative cost (Million GBP)')
axs[2].set_xticks(phase)
axs[2].legend()
for x, y in zip(phase, A_UK_cum_static): axs[2].text(x, y + 20, f'{y:.1f}', ha='center', fontsize=8)
for x, y in zip(phase, B_UK_cum_static): axs[2].text(x, y + 5, f'{y:.1f}', ha='center', fontsize=8)

# D. Per-trio fold-reduction cost
axs[3].bar(phase - 0.15, A_per_trio_fold, width=0.3, label='Method A (10‑fold)', color='#1f77b4')
axs[3].bar(phase + 0.15, B_per_trio_fold, width=0.3, label='Method B (2‑fold)', color='#ff7f0e')
axs[3].set_title('Per-trio fold-reduction cost')
axs[3].set_xlabel('Reanalysis phase')
axs[3].set_ylabel('Cost (GBP)')
axs[3].set_xticks(phase)
axs[3].legend()
for x, y in zip(phase, A_per_trio_fold): axs[3].text(x - 0.15, y, f'{y:.0f}', ha='center', va='bottom', fontsize=8)
for x, y in zip(phase, B_per_trio_fold): axs[3].text(x + 0.15, y, f'{y:.0f}', ha='center', va='bottom', fontsize=8)

# E. Cumulative fold-reduction cost per trio
axs[4].plot(phase, A_cum_fold, marker='o', label='Method A (10‑fold)', color='#1f77b4')
axs[4].plot(phase, B_cum_fold, marker='o', label='Method B (2‑fold)', color='#ff7f0e')
axs[4].set_title('Cumulative fold-reduction cost per trio')
axs[4].set_xlabel('Reanalysis phase')
axs[4].set_ylabel('Cumulative cost (GBP)')
axs[4].set_xticks(phase)
axs[4].legend()
for x, y in zip(phase, A_cum_fold): axs[4].text(x, y + 300, f'{y:.0f}', ha='center', fontsize=8)
for x, y in zip(phase, B_cum_fold): axs[4].text(x, y + 100, f'{y:.0f}', ha='center', fontsize=8)

# F. UK cumulative fold-reduction cost
axs[5].plot(phase, A_UK_cum_fold, marker='o', label='Method A (10‑fold)', color='#1f77b4')
axs[5].plot(phase, B_UK_cum_fold, marker='o', label='Method B (2‑fold)', color='#ff7f0e')
axs[5].set_title('Cumulative fold-reduction cost for UK RD trios')
axs[5].set_xlabel('Reanalysis phase')
axs[5].set_ylabel('Cumulative cost (Million GBP)')
axs[5].set_xticks(phase)
axs[5].legend()
for x, y in zip(phase, A_UK_cum_fold): axs[5].text(x, y + 10, f'{y:.1f}', ha='center', fontsize=8)
for x, y in zip(phase, B_UK_cum_fold): axs[5].text(x, y + 5, f'{y:.1f}', ha='center', fontsize=8)

# Final layout
plt.tight_layout(pad=3.0)
fig.suptitle('Cost Comparison Across Reanalysis Phases', fontsize=16, y=1.02)

# Save and display
fig.savefig('six_panel_cost_plot_fixed_legend.png', bbox_inches='tight')
plt.show()
