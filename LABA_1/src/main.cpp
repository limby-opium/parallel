include "matrix_utils.h"
#include <omp.h>
#include <sys/stat.h>

using namespace std;

// ─── Параллельное умножение (OpenMP) ────────────────────────
Matrix multiplyParallel(const Matrix& A, const Matrix& B, int n, int threads) {
    Matrix C(n, vector<value_t>(n, 0.0));
    omp_set_num_threads(threads);

    #pragma omp parallel for collapse(2)
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++)
                sum += A[i][k] * B[k][j];
            C[i][j] = sum;
        }
    return C;
}

// ─── Точка входа ────────────────────────────────────────────
int main(int argc, char* argv[]) {
    int n;

    // Ввод размера: из аргумента командной строки или интерактивно
    if (argc > 1) {
        try { n = stoi(argv[1]); }
        catch (...) { cerr << "Ошибка: некорректный аргумент!\n"; return 1; }
    } else {
        cout << "Размер матрицы для генерации: ";
        cin >> n;
    }

    if (n <= 0) {
        cerr << "Ошибка: некорректный размер!\n";
        return 1;
    }

    mkdir("result", 0755);

    // ── Генерация ────────────────────────────────────────────
    cout << "Генерация матриц " << n << "x" << n << "...\n";
    Matrix A = MatrixUtils::generateRandom(n, 42);
    Matrix B = MatrixUtils::generateRandom(n, 123);

    MatrixUtils::writeMatrix("result/A.txt", A);
    MatrixUtils::writeMatrix("result/B.txt", B);

    long long volume = 2LL * n * n * n - (long long)n * n;

    // ── CSV: дописываем данные ───────────────────────────────
    bool isNew = !ifstream("result/timings.csv").good();
    ofstream csv("result/timings.csv", ios::app);
    if (isNew)
        csv << "size,threads,total_time,compute_time\n";

    // ── Бенчмарк по числу потоков ────────────────────────────
    vector<int> threadCounts = {1, 2, 4, 8};
    Matrix C;

    cout << "\n========== БЕНЧМАРК ==========\n";
    cout << "  Объём задачи: " << volume << " операций\n\n";

    for (int t : threadCounts) {
        Timer timer;
        timer.start();
        C = (t == 1) ? MatrixUtils::multiply(A, B, n)
                     : multiplyParallel(A, B, n, t);
        double ms = timer.stop();

        csv << n << "," << t << "," << ms << "," << ms << "\n";

        cout << "  " << setw(2) << t << " поток(ов): "
             << fixed << setprecision(2) << setw(8) << ms << " мс\n";
    }
    csv.close();

    // ── Сохранение результата ────────────────────────────────
    MatrixUtils::writeResult("result/result.txt", C, n, 0, volume);

    cout << "\nГотово! Результаты в result/\n";
    return 0;
}