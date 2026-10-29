#include <iostream>
#include <vector>
#include <chrono>

using namespace std;
using namespace std::chrono;

void insertionSort(vector<int>& arr)
{
    int n = arr.size();
    long long comparisons = 0;
    long long shifts = 0;
    
    auto start = high_resolution_clock::now();
    
    for(int i=1; i < n; i++)
    {
        int key = arr[i];
        int j = i-1;
    
        while(j >= 0)
        {
            comparisons++;
            if(arr[j] > key)
            {
                arr[j+1] = arr[j];
                shifts++;
                j--;
            }
            else
            {
                break;
            }
        }
        arr[j+1] = key;
    }
    
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);
    
    cout << "Comparisons: " << comparisons << endl;
    cout << "Shifts: " << shifts << endl;
    cout << "Execution Time: " << duration.count() << " microseconds" << endl;
}

int main()
{
    vector<int> sample = {25,17,31,13,2};
    cout <<"Original Array: ";
    for(int x : sample) cout << x << " ";
    cout << endl;
    
    insertionSort(sample);
    cout << "Sorted Array: ";
    for(int x : sample) cout << x << " ";
    cout << endl;

    return 0;
}