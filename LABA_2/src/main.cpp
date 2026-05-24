#include "matrix_utils.h"
#include <omp.h>
#include <sys/stat.h>

using namespace std;

Matrix multiplyParallel(const Matrix& A, const Matrix& B, int n) {
    Matrix C(n, vector<value_t>(n, 0.0));


    #pragma omp parallel for collapse(2)
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }
    return C;
}


int main(int argc, char* argv[]) {
    int n;


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

    
    cout << "Генерация матриц " << n << "x" << n << "...\n";
    Matrix A = MatrixUtils::generateRandom(n, 42);
    Matrix B = MatrixUtils::generateRandom(n, 123);

    MatrixUtils::writeMatrix("result/A.txt", A);
    MatrixUtils::writeMatrix("result/B.txt", B);


    long long num_multiplications = (long long)n * n * n;
    long long num_additions = (long long)n * n * (n - 1);
    long long volume = num_multiplications + num_additions; 


    bool isNew = !ifstream("result/timings.csv").good();
    ofstream csv("result/timings.csv", ios::app);
    if (isNew)
        csv << "size,threads,total_time,compute_time\n";

    vector<int> threadCounts = {1, 2, 4, 8}; 
    Matrix C;

    cout << "\n========== БЕНЧМАРК ==========\n";
    cout << "  Размер матрицы: " << n << "x" << n << "\n";
    cout << "  Объём задачи (умножений): " << num_multiplications << "\n\n"; 
    Timer timer; 

    for (int t : threadCounts) {
        
        omp_set_num_threads(t);

        timer.start(); 
        C = multiplyParallel(A, B, n); 
        double compute_ms = timer.stop();       
        double total_ms = compute_ms;

        csv << n << "," << t << "," << total_ms << "," << compute_ms << "\n";

        cout << "  " << setw(2) << t << " поток(ов): "
             << fixed << setprecision(2) << setw(8) << compute_ms << " мс\n";
    }
    csv.close();


    MatrixUtils::writeResult("result/result.txt", C, n, 0, volume);

    cout << "\nГотово! Результаты записаны в result/\n";
    return 0;
}