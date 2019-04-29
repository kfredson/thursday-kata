#include <bits/stdc++.h>
#include <random>
#include <time.h>
#include <chrono>


using namespace std;


bool sortFunction (long i,long j) { return (abs(i)<abs(j)); }

vector<vector<long>> get_random_arrays() {
	unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
	std::default_random_engine eng(seed);
    uniform_int_distribution<long> distr(-10000000,10000000);
	uniform_int_distribution<long> array_size_distr(1,10000000);
	long size1 = array_size_distr(eng);
	long size2 = array_size_distr(eng);
	vector<long> array1(size1);
	vector<long> array2(size2);
	for (long i = 0; i < size1; i++) array1[i] = distr(eng);
	for (long i = 0; i < size2; i++) array2[i] = distr(eng);
	vector<vector<long>> triple;
	triple.push_back(array1);
	triple.push_back(array2);
	int chooseMult = distr(eng)%2;
	if (chooseMult==0) {
		long i1 = (array_size_distr(eng))%size1;
		long i2 = (array_size_distr(eng))%size2;
		vector<long> mult = {array1[i1]*array2[i2]};
		triple.push_back(mult);
	} else {
		vector<long> mult = {distr(eng)};
		triple.push_back(mult);
	}
	return triple;
}

vector<long> twoPointer(vector<long> array1, vector<long> array2, long targetInt) {
	vector<long> ans;
	long pt1 = array1.size()-1;
	long pt2 = 0;
	//sort by absolute values
	sort(array1.begin(),array1.end(),sortFunction);
	sort(array2.begin(),array2.end(),sortFunction);
	while (pt1 > -1 && pt2 < array2.size()) {
		long mult = array1[pt1]*array2[pt2];
		if (abs(mult) < abs(targetInt)) pt2++;
		else if (abs(mult) > abs(targetInt)) pt1--;
		else {
			//We matched with numbers multiplying to targetInt up to a sign,
			//but still need to check we can get correct sign
			if (mult==targetInt) {			
				ans = {array1[pt1],array2[pt2]};
				return ans;
			} else {
				//Know we can get correct answer as long as one of the arrays has both + and - of the number
				if (pt2 < array2.size()-1 && abs(array2[pt2])==abs(array2[pt2+1])) pt2++;
				else pt1--;
			}
		}
	}
	return ans;
}

vector<long> divideWithSet(vector<long> array1, vector<long> array2, long targetInt) {
	vector<long> ans;

	if (targetInt==0) {
		if (array1.size()==0 || array2.size()==0) return ans;
		else {
		for (int i = 0; i < array1.size(); i++) if (array1[i]==0) { ans={0,array2[0]}; return ans; }		
		for (int i = 0; i < array2.size(); i++) if (array2[i]==0) { ans={array1[0],0}; return ans; } 
		}
	}

	int flipped = 0;
	if (array1.size() < array2.size()) {swap(array1,array2); flipped = 1;}
	set<long> checkSet(array2.begin(),array2.end());
	for (long i = 0; i < array1.size(); i++) {
		if (array1[i] != 0 && targetInt%array1[i]==0) {
			long div = targetInt/array1[i];
			if (checkSet.find(div) != checkSet.end()) {
				if (!flipped) 
				ans = {array1[i],div};
				else
				ans = {div,array1[i]};
				return ans;
			}
		}
	}
	return ans;
}

vector<long> divideWithSet_flipped(vector<long> array1, vector<long> array2, long targetInt) {
	vector<long> ans;

	if (targetInt==0) {
		if (array1.size()==0 || array2.size()==0) return ans;
		else {
		for (int i = 0; i < array1.size(); i++) if (array1[i]==0) { ans={0,array2[0]}; return ans; }		
		for (int i = 0; i < array2.size(); i++) if (array2[i]==0) { ans={array1[0],0}; return ans; } 
		}
	}

	int flipped = 0;
	if (array1.size() > array2.size()) {swap(array1,array2); flipped = 1;}
	set<long> checkSet(array2.begin(),array2.end());
	for (long i = 0; i < array1.size(); i++) {
		if (array1[i] != 0 && targetInt%array1[i]==0) {
			long div = targetInt/array1[i];
			if (checkSet.find(div) != checkSet.end()) {
				if (!flipped) 
				ans = {array1[i],div};
				else
				ans = {div,array1[i]};
				return ans;
			}
		}
	}
	return ans;
}

//WINNER!
vector<long> divideWithUnorderedSet(vector<long> array1, vector<long> array2, long targetInt) {
	vector<long> ans;

	if (targetInt==0) {
		if (array1.size()==0 || array2.size()==0) return ans;
		else {
		for (int i = 0; i < array1.size(); i++) if (array1[i]==0) { ans={0,array2[0]}; return ans; }		
		for (int i = 0; i < array2.size(); i++) if (array2[i]==0) { ans={array1[0],0}; return ans; } 
		}
	}

	int flipped = 0;
	if (array1.size() < array2.size()) {swap(array1,array2); flipped = 1;}
	unordered_set<long> checkSet(array2.begin(),array2.end());
	for (long i = 0; i < array1.size(); i++) {
		if (array1[i] != 0 && targetInt%array1[i]==0) {
			long div = targetInt/array1[i];
			if (checkSet.find(div) != checkSet.end()) {
				if (!flipped) 
				ans = {array1[i],div};
				else
				ans = {div,array1[i]};
				return ans;
			}
		}
	}
	return ans;
}

vector<long> divideWithUnorderedSet_flipped(vector<long> array1, vector<long> array2, long targetInt) {
	vector<long> ans;

	if (targetInt==0) {
		if (array1.size()==0 || array2.size()==0) return ans;
		else {
		for (int i = 0; i < array1.size(); i++) if (array1[i]==0) { ans={0,array2[0]}; return ans; }		
		for (int i = 0; i < array2.size(); i++) if (array2[i]==0) { ans={array1[0],0}; return ans; } 
		}
	}

	int flipped = 0;
	if (array1.size() > array2.size()) {swap(array1,array2); flipped = 1;}
	unordered_set<long> checkSet(array2.begin(),array2.end());
	for (long i = 0; i < array1.size(); i++) {
		if (array1[i] != 0 && targetInt%array1[i]==0) {
			long div = targetInt/array1[i];
			if (checkSet.find(div) != checkSet.end()) {
				if (!flipped) 
				ans = {array1[i],div};
				else
				ans = {div,array1[i]};
				return ans;
			}
		}
	}
	return ans;
}

vector<long> divideWithBinarySearch(vector<long> array1, vector<long> array2, long targetInt) {
	vector<long> ans;

	if (targetInt==0) {
		if (array1.size()==0 || array2.size()==0) return ans;
		else {
		for (int i = 0; i < array1.size(); i++) if (array1[i]==0) { ans={0,array2[0]}; return ans; }		
		for (int i = 0; i < array2.size(); i++) if (array2[i]==0) { ans={array1[0],0}; return ans; } 
		}
	}

	int flipped = 0;
	if (array1.size() < array2.size()) {swap(array1,array2); flipped = 1;}
	sort(array2.begin(),array2.end());
	for (long i = 0; i < array1.size(); i++) {
		if (array1[i] != 0 && targetInt%array1[i]==0) {
			long div = targetInt/array1[i];
			if (binary_search(array2.begin(),array2.end(),div)) {
				if (!flipped) 
				ans = {array1[i],div};
				else
				ans = {div,array1[i]};
				return ans;
			}
		}
	}
	return ans;
}

vector<long> divideWithBinarySearch_flipped(vector<long> array1, vector<long> array2, long targetInt) {
	vector<long> ans;

	if (targetInt==0) {
		if (array1.size()==0 || array2.size()==0) return ans;
		else {
		for (int i = 0; i < array1.size(); i++) if (array1[i]==0) { ans={0,array2[0]}; return ans; }		
		for (int i = 0; i < array2.size(); i++) if (array2[i]==0) { ans={array1[0],0}; return ans; } 
		}
	}

	int flipped = 0;
	if (array1.size() > array2.size()) {swap(array1,array2); flipped = 1;}
	sort(array2.begin(),array2.end());
	for (long i = 0; i < array1.size(); i++) {
		if (array1[i] != 0 && targetInt%array1[i]==0) {
			long div = targetInt/array1[i];
			if (binary_search(array2.begin(),array2.end(),div)) {
				if (!flipped) 
				ans = {array1[i],div};
				else
				ans = {div,array1[i]};
				return ans;
			}
		}
	}
	return ans;
}


int main() {
	struct timespec start, finish;
	double elapsed;
	double final_results[7];  for (int i = 0; i < 7; i++) final_results[i] = 0;
	
	for (int i=0; i < 10; i++) {
	vector<vector<long>> v = get_random_arrays();
	cout << "Array sizes: " << v[0].size() << " " << v[1].size() << "\n";
	
	cout << "Running two-pointer function:\n";
	clock_gettime(CLOCK_MONOTONIC, &start);
	vector<long> ans = twoPointer(v[0],v[1],v[2][0]);
	clock_gettime(CLOCK_MONOTONIC, &finish);
	elapsed = (finish.tv_sec - start.tv_sec);
	elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
	cout << elapsed << " seconds elapsed\n";
	final_results[0] += elapsed;
	if (ans.size()==0) cout << "No solution\n";
	else cout << ans[0] << " " << ans[1] << " " << "\n";
	cout << "----------------------------------------------------------------\n";
	
	cout << "Running divide-with-set function:\n";
	clock_gettime(CLOCK_MONOTONIC, &start);
	ans = divideWithSet(v[0],v[1],v[2][0]);
	clock_gettime(CLOCK_MONOTONIC, &finish);
	elapsed = (finish.tv_sec - start.tv_sec);
	elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;	
	final_results[1] += elapsed;
	cout << elapsed << " seconds elapsed\n";
	if (ans.size()==0) cout << "No solution\n";
	else cout << ans[0] << " " << ans[1] << " " << "\n";
	cout << "----------------------------------------------------------------\n";
	
	cout << "Running divide-with-set-flipped function:\n";
	clock_gettime(CLOCK_MONOTONIC, &start);
	ans = divideWithSet_flipped(v[0],v[1],v[2][0]);
	clock_gettime(CLOCK_MONOTONIC, &finish);
	elapsed = (finish.tv_sec - start.tv_sec);
	elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;	
	final_results[2] += elapsed;
	cout << elapsed << " seconds elapsed\n";
	if (ans.size()==0) cout << "No solution\n";
	else cout << ans[0] << " " << ans[1] << " " << "\n";
	cout << "----------------------------------------------------------------\n";    	

	cout << "Running divide-with-unordered-set function:\n";
	clock_gettime(CLOCK_MONOTONIC, &start);
	ans = divideWithUnorderedSet(v[0],v[1],v[2][0]);
	clock_gettime(CLOCK_MONOTONIC, &finish);
	elapsed = (finish.tv_sec - start.tv_sec);
	elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;	
	final_results[3] += elapsed;
	cout << elapsed << " seconds elapsed\n";
	if (ans.size()==0) cout << "No solution\n";
	else cout << ans[0] << " " << ans[1] << " " << "\n";
	cout << "----------------------------------------------------------------\n"; 
	
	cout << "Running divide-with-unordered-set-flipped function:\n";
	clock_gettime(CLOCK_MONOTONIC, &start);
    ans = divideWithUnorderedSet_flipped(v[0],v[1],v[2][0]);
	clock_gettime(CLOCK_MONOTONIC, &finish);
	elapsed = (finish.tv_sec - start.tv_sec);
	elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;	
	final_results[4] += elapsed;
	cout << elapsed << " seconds elapsed\n";
	if (ans.size()==0) cout << "No solution\n";
	else cout << ans[0] << " " << ans[1] << " " << "\n";
	cout << "----------------------------------------------------------------\n"; 
	
	cout << "Running divide-with-binary-search function:\n";
	clock_gettime(CLOCK_MONOTONIC, &start);
    ans = divideWithUnorderedSet_flipped(v[0],v[1],v[2][0]);
	clock_gettime(CLOCK_MONOTONIC, &finish);
	elapsed = (finish.tv_sec - start.tv_sec);
	elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;	
	final_results[5] += elapsed;
	cout << elapsed << " seconds elapsed\n";
	if (ans.size()==0) cout << "No solution\n";
	else cout << ans[0] << " " << ans[1] << " " << "\n";
	cout << "----------------------------------------------------------------\n"; 
	
	cout << "Running divide-with-binary-search-flipped function:\n";
	clock_gettime(CLOCK_MONOTONIC, &start);
    ans = divideWithUnorderedSet_flipped(v[0],v[1],v[2][0]);
	clock_gettime(CLOCK_MONOTONIC, &finish);
	elapsed = (finish.tv_sec - start.tv_sec);
	elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;	
	final_results[6] += elapsed;
	cout << elapsed << " seconds elapsed\n";
	if (ans.size()==0) cout << "No solution\n";
	else cout << ans[0] << " " << ans[1] << " " << "\n";
	cout << "----------------------------------------------------------------\n"; 
	
	cout << "----------------------------------------------------------------\n"; 	
	cout << "----------------------------------------------------------------\n"; 
	}
	
	cout << "FINAL RESULTS:\n";
	cout << "Two-pointer: " << final_results[0] << "\n";	
	cout << "Divide-with-set: " << final_results[1] << "\n";	
	cout << "Divide-with-set-flipped: " << final_results[2] << "\n";	
	cout << "Divide-with-unordered-set: " << final_results[3] << "\n";	
	cout << "Divide-with-unordered-set-flipped: " << final_results[4] << "\n";
	cout << "Divide-with-binary-search: " << final_results[5] << "\n";
	cout << "Divide-with-binary-search-flipped: " << final_results[6] << "\n";

	return 0;
}

