#include <cstdio>
#include <iostream>
#include <vector>
#include <cmath>
#include <climits>
#include <algorithm>
using namespace std;
// DSU for all connected components of graph (cycles); for each cycle, add the sum of edges - minimum edge;
//DSU only works fo undirected graphs; DFS for all cyclic components of graph.

vector<bool> visited;
pair<int, int> dfs(int node, int parent, vector<vector<pair<int, int>>> adj, int total, int min) {
    visited[node] = true;
    for (pair<int, int> child : adj.at(node)) {
        if (!visited[child.first]) {
            total += child.second;
            if (child.second < min) {
                min = child.second;
            }
            dfs(child.first, node, adj, total, min);
        }
    }
    return make_pair(total, min);
}
int main() {
    int n;
    scanf("%d", &n);
    vector<vector<pair<int, int>>> adj(n, vector<pair<int, int>>());
    for (int i = 0; i < n; i++) {
        int a, b;
        scanf("%d %d", &a, &b);
        adj.at(i).push_back(make_pair(a, b));
    }
    int ans = 0;
    visited.resize(n, false);
    cout << "hi";
    for (int i = 0; i < n; i++) {
        cout << "hii";
        if (!visited[i]) {
            int totalWeight = 0;
            int minEdge = INT_MAX;
            pair<int, int> result = dfs(i, -1, adj, totalWeight, minEdge);
            ans += (result.first - result.second);
        }
    }
    printf("%d\n", ans);
}