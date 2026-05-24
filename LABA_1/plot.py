#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('result/timings.csv')
print("Данные:\n", df.to_string(index=False))

colors = ['#1976D2', '#E53935', '#43A047', '#8E24AA']

plt.figure(figsize=(10, 6))
for idx, t in enumerate(sorted(df['threads'].unique())):
    data = df[df['threads'] == t]
    plt.plot(data['size'], data['total_time'], 'o-',
             color=colors[idx], label=f'{t} thread(s)', linewidth=2, markersize=7)
plt.xlabel('Размер матрицы')
plt.ylabel('Время (мс)')
plt.title('Производительность умножения матриц')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xscale('log')
plt.yscale('log')
plt.savefig('result/performance.png', dpi=300, bbox_inches='tight')
plt.show()

plt.figure(figsize=(10, 6))
seq = df[df['threads'] == 1]
for size in sorted(df['size'].unique()):
    base = seq[seq['size'] == size]['total_time'].values[0]
    data = df[df['size'] == size]
    plt.plot(data['threads'], base / data['total_time'], 'o-',
             label=f'n={size}', linewidth=2, markersize=7)
threads = np.array(sorted(df['threads'].unique()))
plt.plot(threads, threads, 'k--', label='Идеальное', linewidth=2)
plt.xlabel('Количество потоков')
plt.ylabel('Ускорение')
plt.title('Ускорение при параллельных вычислениях')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('result/speedup.png', dpi=300, bbox_inches='tight')
plt.show()

print("Графики сохранены в result/")