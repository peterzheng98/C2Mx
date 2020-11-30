#include <stdio.h>

int main() {
	int t,a[50],b[50],n,x;
	char* rs;
	scanf("%d",&t);
	scanf("%s", rs);
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
		printf("NO%dafasfasafssaf%srrr\n", t, rs);
		else
		printf("YES\n");
	}
}