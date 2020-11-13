#include <stdio.h>

int main() {
	int t,a[100][50],b[50],n,x;
	scanf("%d",&t);
	for(int i=0;i<t;i++){
		scanf("%d %d",&n,&x);
		for(int j=0;j<n;j++){
			scanf("%d",&a[j]);
		}
		for(int j=0;j<n;j++){
			scanf("%d",&b[j]);
		}
		int flag = 1;
		for(int j=0;j<n;j++){
			if((b[n-j-1] + a[j]) <=x)
				continue;
			else{
				flag = 0;
				break;
			}
		}
		if(flag==0)
		printf("NO\n");
		else
		printf("YES\n");
	}
}