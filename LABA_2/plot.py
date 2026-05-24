
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    df = pd.read_csv('result/timings.csv')
    print("--- Загруженные данные ---")
    print(df.to_string(index=False))
    print("--------------------------\n")
except FileNotFoundError:
    print("Ошибка: Файл result/timings.csv не найден. Пожалуйста, запустите benchmark.sh перед запуском plot.py.")
    exit(1)
except Exception as e:
    print(f"Ошибка при чтении файла: {e}")
    exit(1)
try:
  colors = plt.get_cmap('tab10', len(df['threads'].unique()))
except AttributeError: 
  colors = plt.cm.get_cmap('tab10', len(df['threads'].unique()))

plt.figure(figsize=(12, 7))
unique_threads = sorted(df['threads'].unique())

for idx, t in enumerate(unique_threads):
    data_for_thread = df[df['threads'] == t].sort_values('size')
    plt.plot(data_for_thread['size'], data_for_thread['compute_time'], marker='o', linestyle='-',
             color=colors(idx), label=f'{t} поток(ов)', markersize=7)

plt.xlabel('Размер матрицы (n x n)')
plt.ylabel('Время вычисления (мс)')
plt.title('Производительность умножения матриц (Время вычисления)')
plt.legend()
plt.grid(True, which="both", linestyle='--', linewidth=0.5, alpha=0.6)

plt.xscale('log')
plt.yscale('log')

plt.savefig('result/compute_time_performance.png', dpi=300, bbox_inches='tight')
print("График 'compute_time_performance.png' сохранен.")

plt.figure(figsize=(12, 7)) 

seq_times_df = df[df['threads'] == 1].set_index('size')

for size in sorted(df['size'].unique()):
    seq_time = seq_times_df.loc[size, 'compute_time'] 
    data_for_size = df[(df['size'] == size) & (df['threads'] > 1)].sort_values('threads') 

    current_threads = data_for_size['threads'].values
    current_compute_times = data_for_size['compute_time'].values

    speedups = np.where(current_compute_times > 0, seq_time / current_compute_times, np.nan)

    plt.plot(current_threads, speedups, marker='o', linestyle='-',
             color=colors(unique_threads.index(data_for_size['threads'].iloc[0]) if data_for_size['threads'].iloc[0] in unique_threads else 0),
             label=f'n={size}', markersize=7)

plt.plot(unique_threads, unique_threads, 'k--', label='Идеальное ускорение (Y=X)', linewidth=2)

plt.xlabel('Количество потоков')
plt.ylabel('Ускорение (Speedup)')
plt.title('Ускорение в зависимости от количества потоков')
plt.legend()
plt.grid(True, which="both", linestyle='--', linewidth=0.5, alpha=0.6)
plt.xscale('log') 
plt.yscale('log') 

plt.savefig('result/speedup.png', dpi=300, bbox_inches='tight')
print("График 'speedup.png' сохранен.")

plt.show() 