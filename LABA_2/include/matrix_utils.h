#pragma once

#include <vector>
#include <fstream>
#include <random>
#include <chrono>
#include <stdexcept>
#include <string>
#include <iostream>
#include <iomanip>

using namespace std;

using value_t = double;
using Matrix  = vector<vector<value_t>>;

class Timer {
    chrono::high_resolution_clock::time_point t0;
public:
    void start() { t0 = chrono::high_resolution_clock::now(); }
    double stop() const {
        return chrono::duration<double, milli>(
            chrono::high_resolution_clock::now() - t0).count();
    }
};

namespace MatrixUtils {

    inline Matrix generateRandom(int n, unsigned seed = 42) {
        mt19937 gen(seed);
        uniform_real_distribution<> dist(-100.0, 100.0);
        Matrix M(n, vector<value_t>(n));
        for (auto& row : M)
            for (auto& val : row)
                val = dist(gen);
        return M;
    }

    inline Matrix multiply(const Matrix& A, const Matrix& B, int n) {
        Matrix C(n, vector<value_t>(n, 0.0));
        for (int i = 0; i < n; ++i)
            for (int k = 0; k < n; ++k) {
                value_t a_ik = A[i][k];
                for (int j = 0; j < n; ++j)
                    C[i][j] += a_ik * B[k][j];
            }
        return C;
    }

    // ─── FIX: setprecision(15) для сохранения полной точности double ──
    inline void writeMatrix(const string& path, const Matrix& M) {
        int n = M.size();
        ofstream f(path);
        if (!f) throw runtime_error("Ошибка записи: " + path);
        f << n << "\n";
        f << setprecision(15);
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                f << M[i][j];
                if (j + 1 < n) f << " ";
            }
            f << "\n";
        }
    }

    // ─── FIX: убран fixed, setprecision(15) ──
    inline void writeResult(const string& path, const Matrix& C,
                            int n, double ms, long long ops) {
        ofstream f(path);
        if (!f) throw runtime_error("Ошибка записи: " + path);
        f << "# Результат перемножения матриц\n"
          << "# Размер: " << n << " x " << n << "\n"
          << "# Время вычисления: " << ms << " мс\n"
          << "# Объём задачи: " << ops << " операций\n"
          << n << "\n";
        f << setprecision(15);
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                f << C[i][j];
                if (j + 1 < n) f << " ";
            }
            f << "\n";
        }
    }

} 