
mkdir -p result

SIZES=(200 400 800 1200 1600 2000)

echo "Начинаем бенчмарк..."

for size in "${SIZES[@]}"; do
    echo "=== Тестирование размера: $size ==="
    ./main $size
    echo "" 
done

echo "Бенчмарк завершён."
echo "Результаты собраны в result/timings.csv."
echo "Для просмотра графиков выполните: make plot"