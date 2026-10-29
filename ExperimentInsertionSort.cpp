#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>

using namespace std;
using namespace std::chrono;

struct Metrics {
    long long comparisons;
    long long shifts;
    long long durationMicroseconds;
};

Metrics insertionSortWithMetrics(vector<int>& arr) {
    int n = arr.size();
    long long comparisons = 0;
    long long shifts = 0;
    
    auto start = high_resolution_clock::now();
    
    for(int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
    
        while(j >= 0) {
            comparisons++;
            if(arr[j] > key) {
                arr[j + 1] = arr[j];
                shifts++;
                j--;
            } else {
                break;
            }
        }
        arr[j + 1] = key;
    }
    
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    
    return {comparisons, shifts, duration.count()};
}

int main() {
    vector<int> testSizes = {100, 500, 1000, 2000, 5000};
    
    random_device rd;
    mt19937 gen(rd());
    
    cout << "n\tState\t\tComparisons\tShifts\t\tTime (us)" << endl;
    cout << "------------------------------------------------------------------" << endl;
    
    for(int n : testSizes) {
        vector<int> randomArr(n);
        uniform_int_distribution<> dis(1, 100000);
        for(int i = 0; i < n; i++) {
            randomArr[i] = dis(gen);
        }
        
        vector<int> sortedArr = randomArr;
        sort(sortedArr.begin(), sortedArr.end());
        
        vector<int> reverseArr = sortedArr;
        reverse(reverseArr.begin(), reverseArr.end());
        
        Metrics mRandom = insertionSortWithMetrics(randomArr);
        cout << n << "\tRandom\t\t" << mRandom.comparisons << "\t\t" << mRandom.shifts << "\t\t" << mRandom.durationMicroseconds << endl;
        
        Metrics mSorted = insertionSortWithMetrics(sortedArr);
        cout << n << "\tSorted\t\t" << mSorted.comparisons << "\t\t" << mSorted.shifts << "\t\t" << mSorted.durationMicroseconds << endl;
        
        Metrics mReverse = insertionSortWithMetrics(reverseArr);
        cout << n << "\tReverse\t\t" << mReverse.comparisons << "\t\t" << mReverse.shifts << "\t\t" << mReverse.durationMicroseconds << endl;
        
        cout << "------------------------------------------------------------------" << endl;
    }

    return 0;
}