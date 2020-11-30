int main()
{
    int n,m;
	char st[100010];
	int s[100010],sa[100010],rk[100010],height[100010],buc[100010],t1[100010],t2[100010];
	int n,m;

	scanf("%s",st);
	n=strlen(st);
	m=26;
    int i,k;
	for (i=0;i<n;i++) s[i]=st[i]-'a';
	int *x=t1,*y=t2;
	for (i=0;i<m;i++) buc[i]=0;
	for (i=0;i<n;i++) x[i]=s[i];
	for (i=0;i<n;i++) buc[s[i]]++;
	for (i=1;i<m;i++) buc[i]+=buc[i-1];
	for (i=n-1;i>=0;i--) sa[--buc[x[i]]]=i;
	for (k=1;k<=n;k<<=1) {
		int p=0;
		for (i=n-1;i>=n-k;i--) y[p++]=i;
		for (i=0;i<n;i++) if (sa[i]>=k) y[p++]=sa[i]-k;
		for (i=0;i<m;i++) buc[i]=0;
		for (i=0;i<n;i++) buc[x[i]]++;
		for (i=1;i<m;i++) buc[i]+=buc[i-1];
		for (i=n-1;i>=0;i--) sa[--buc[x[y[i]]]]=y[i];
        int* tmp=x;x=y;y=tmp;
		x[sa[0]]=0;
		p=1;
		for (i=1;i<n;i++) {
			if (y[sa[i]]==y[sa[i-1]] && y[sa[i]+k]==y[sa[i-1]+k]) x[sa[i]]=p-1;
			else x[sa[i]]=p++;
        }
		if (p>=n) break;
		m=p;
	}
	for (i=0;i<n;i++)
		rk[sa[i]]=i;
	for (i=0;i<n;i++)
		printf("%d%c",sa[i]+1," \n"[i==n-1]);
    k=0;
	for (i=0;i<n;i++) {
		if (rk[i]==0) {
			height[rk[i]]=0;
			continue;
		}
		if (k) k--;
		int j=sa[rk[i]-1];
		while (s[i+k]==s[j+k] && i+k<n && j+k<n) k++;
		height[rk[i]]=k;
	}
	for (i=1;i<n;i++)
		printf("%d%c",height[i]," \n"[i==n-1]);
	return 0;
}