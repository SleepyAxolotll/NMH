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
pair<int, int> dfs(int node, vector<vector<pair<int, int>>> &adj, int &total, int &min, int parent) {
    visited[node] = true;
    for (pair<int, int> child : adj.at(node)) {
        if (!visited[child.first]) {
            total += child.second;
            if (child.second < min) {
                min = child.second;
            }
            dfs(child.first, adj, total, min, parent);
        } else if (child.first == parent) {
            total += child.second;
            if (child.second < min) {
                min = child.second;
            }
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
        adj.at(i).push_back(make_pair(a - 1, b));
    }
    int ans = 0;
    visited.resize(n, false);
    for (int i = 0; i < n; i++) {
        if (!visited[i]) {
            int totalWeight = 0;
            int minEdge = INT_MAX;
            pair<int, int> result = dfs(i, adj, totalWeight, minEdge, i);
            // cout << result.first <<" " << result.second << " ";
            ans += (result.first - result.second);
        }
    }
    printf("%d", ans);
}
