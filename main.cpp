#include <iostream>
#include <thread>
#include <vector>

template<typename T>
void Sort(T* begin, int n)
{
	qsort(dynamic_cast<void*>(begin), n, sizeof(T), [](){});
}

int cmpr(int a, int b)
{
	if (a > b) return 1;
	if (a < b) return -1;
	return 0;
}

int main()
{
	int N = 60E+6;
	int n = 10E+6;
	int* arr = new int[N];
	for (int i = 0; i < N; ++i)
	{
		arr[i] = rand() % 100;
	}

	std::vector<std::thread> vec;


	/*for (size_t i = 0; i < std::thread::hardware_concurrency(); ++i)
	{
		vec.emplace_back(Sort, arr + n*i, n);
	}*/
    std::thread t(Sort, arr + 100, n);

	for (auto& i : vec)
	{
		i.join();
	}
}
