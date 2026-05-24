#!/usr/bin/env python3
import sys
import numpy as np

def read_matrix(filename):
    """Чтение матрицы из файла (пропускает комментарии #)."""
    with open(filename) as f:
        lines = [l.strip() for l in f if l.strip() and not l.strip().startswith('#')]
    n = int(lines[0])
    return np.array([[float(x) for x in lines[i + 1].split()] for i in range(n)])

def main():
    if len(sys.argv) != 4:
        print("Использование: verify.py <A.txt> <B.txt> <result.txt>")
        sys.exit(1)

    A = read_matrix(sys.argv[1])
    B = read_matrix(sys.argv[2])
    expected = A @ B

    C = read_matrix(sys.argv[3])

    max_err = np.max(np.abs(C - expected))

    if np.allclose(C, expected, rtol=1e-9, atol=1e-6):
        print(f"✓ Верификация пройдена (макс. ошибка: {max_err:.2e})")
    else:
        print(f"✗ Верификация НЕ пройдена (макс. ошибка: {max_err:.2e})")
        sys.exit(1)

if __name__ == "__main__":
    main()