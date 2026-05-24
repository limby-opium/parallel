import pandas as pd
import matplotlib
matplotlib.use('Agg')  # без окон — только сохранение в файл (решает ошибку Qt/Wayland)
import matplotlib.pyplot as plt
import numpy as np

# ─── Загрузка данных ─────────────────────────────────────────
try:
    df = pd.read_csv('result/timings.csv')
except FileNotFoundError:
    print("Ошибка: Файл result/timings.csv не найден. Запустите benchmark.sh")
    exit(1)
except Exception as e:
    print(f"Ошибка при чтении файла: {e}")
    exit(1)

# ✅ КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: убираем дубликаты (benchmark мог запускаться несколько раз)
df = df.drop_duplicates(subset=['size', 'threads'], keep='last')
df = df.sort_values(['size', 'threads']).reset_index(drop=True)

print("--- Загруженные данные ---")
print(df.to_string(index=False))
print("--------------------------\n")

# Цвета для графиков
colors = plt.colormaps['tab10'].resampled(len(df['threads'].unique()))

# ═══════════════════════════════════════════════════════════════
# График 1: Производительность (время vs размер матрицы)
# ═══════════════════════════════════════════════════════════════
plt.figure(figsize=(12, 7))
unique_threads = sorted(df['threads'].unique())

for idx, t in enumerate(unique_threads):
    data_for_thread = df[df['threads'] == t].sort_values('size')
    plt.plot(data_for_thread['size'], data_for_thread['compute_time'],
             marker='o', linestyle='-', color=colors(idx),
             label=f'{t} поток(ов)', markersize=7)

plt.xlabel('Размер матрицы (n x n)')
plt.ylabel('Время вычисления (мс)')
plt.title('Производительность умножения матриц (Время вычисления)')
plt.legend()
plt.grid(True, which="both", linestyle='--', linewidth=0.5, alpha=0.6)
plt.xscale('log')
plt.yscale('log')
plt.savefig('result/compute_time_performance.png', dpi=300, bbox_inches='tight')
print("График 'compute_time_performance.png' сохранён.")
plt.close()

# ═══════════════════════════════════════════════════════════════
# График 2: Ускорение (speedup vs потоки)
# ═══════════════════════════════════════════════════════════════
plt.figure(figsize=(12, 7))

# Берём только последний замер для каждого (size, threads)
# и формируем таблицу: строки = size, столбцы = threads
pivot = df.pivot_table(index='size', columns='threads',
                       values='compute_time', aggfunc='last')

for idx, size in enumerate(sorted(pivot.index)):
    # ✅ Берём скаляр: .loc[size, 1] возвращает одно число
    if 1 not in pivot.columns:
        print(f"Предупреждение: нет данных для threads=1 при size={size}, пропуск")
        continue

    seq_time = pivot.loc[size, 1]  # scalar!

    # Все потоки > 1 для этого размера
    thread_cols = [t for t in sorted(pivot.columns) if t > 1]
    if not thread_cols:
        continue

    current_times = pivot.loc[size, thread_cols].values.astype(float)
    speedups = np.where(current_times > 0, seq_time / current_times, np.nan)

    plt.plot(thread_cols, speedups, marker='o', linestyle='-',
             color=colors(idx), label=f'n={size}', markersize=7)

# Идеальная линия
max_threads = max(unique_threads)
plt.plot(unique_threads, unique_threads, 'k--',
         label='Идеальное ускорение (Y=X)', linewidth=2)

plt.xlabel('Количество потоков')
plt.ylabel('Ускорение (Speedup)')
plt.title('Ускорение в зависимости от количества потоков')
plt.legend()
plt.grid(True, which="both", linestyle='--', linewidth=0.5, alpha=0.6)
plt.xscale('log')
plt.yscale('log')
plt.savefig('result/speedup.png', dpi=300, bbox_inches='tight')
print("График 'speedup.png' сохранён.")
plt.close()

print("\nГотово! Графики в result/")