#!/bin/bash
rm -f result/timings.csv
mkdir -p result

for size in 64 128 256 512 1024; do
    echo "=== Benchmarking size $size ==="
    ./main $size
    echo ""
done

echo "Бенчмарк завершён. Запустите: make plot"