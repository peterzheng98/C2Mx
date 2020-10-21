#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
#define N	1000
#define M	1000
#define K	1000
#define INF	0x3f3f3f3f
 
int min(int a, int b) { return a < b ? a : b; }
 
int ii[M], jj[M], ww[M];
int *oh[N], oo[N];
 
void append(int i, int h) {
	int o = oo[i]++;
 
	if (o >= 2 && (o & o - 1) == 0)
		oh[i] = (int *) realloc(oh[i], o * 2 * sizeof *oh[i]);
	oh[i][o] = h;
}
 
int *dd_, iq[1 + N], pq[N], cnt;
 
int lt(int i, int j) {
	return dd_[i] < dd_[j];
}
 
int p2(int p) {
	return (p *= 2) > cnt ? 0 : (p < cnt && lt(iq[p + 1], iq[p]) ? p + 1 : p);
}
 
void pq_up(int i) {
	int p, q, j;
 
	for (p = pq[i]; (q = p / 2) && lt(i, j = iq[q]); p = q)
		iq[pq[j] = p] = j;
	iq[pq[i] = p] = i;
}
 
void pq_dn(int i) {
	int p, q, j;
 
	for (p = pq[i]; (q = p2(p)) && lt(j = iq[q], i); p = q)
		iq[pq[j] = p] = j;
	iq[pq[i] = p] = i;
}
 
void pq_add_last(int i) {
	iq[pq[i] = ++cnt] = i;
}
 
int pq_remove_first() {
	int i = iq[1], j = iq[cnt--];
 
	if (j != i)
		pq[j] = 1, pq_dn(j);
	pq[i] = 0;
	return i;
}
 
void dijkstra(int n, int s) {
	memset(dd_, 0x3f, n * sizeof *dd_);
	dd_[s] = 0, pq_add_last(s);
	while (cnt) {
		int i = pq_remove_first(), o;
 
		for (o = 0; o < oo[i]; o++) {
			int h = oh[i][o], j = i ^ ii[h] ^ jj[h], d = dd_[i] + ww[h];
 
			if (dd_[j] > d) {
				if (dd_[j] == INF)
					pq_add_last(j);
				dd_[j] = d, pq_up(j);
			}
		}
	}
}
 
int main() {
	static int dd[N][N], uu[K], vv[K];
	int n, m, k, g, h, i, j, ans;
 
	scanf("%d%d%d", &n, &m, &k);
	for (i = 0; i < n; i++)
		oh[i] = (int *) malloc(2 * sizeof *oh[i]);
	for (h = 0; h < m; h++) {
		scanf("%d%d%d", &ii[h], &jj[h], &ww[h]), ii[h]--, jj[h]--;
		append(ii[h], h), append(jj[h], h);
	}
	for (g = 0; g < k; g++)
		scanf("%d%d", &uu[g], &vv[g]), uu[g]--, vv[g]--;
	for (i = 0; i < n; i++)
		dd_ = dd[i], dijkstra(n, i);
	ans = INF;
	for (h = 0; h < m; h++) {
		int sum;
 
		i = ii[h], j = jj[h], sum = 0;
		for (g = 0; g < k; g++)
			sum += min(dd[uu[g]][vv[g]], min(dd[uu[g]][i] + dd[j][vv[g]], dd[uu[g]][j] + dd[i][vv[g]]));
		ans = min(ans, sum);
	}
	printf("%d\n", ans);
	return 0;
}