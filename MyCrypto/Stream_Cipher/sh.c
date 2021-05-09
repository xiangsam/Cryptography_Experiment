#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main()
{
	FILE * fp = fopen("temp", "r");
	char s[1024];
	while(fgets(s, 1024,fp)!=NULL){
        char *p = strtok(s, " \t\r\n");
	    while(p != NULL){
		    printf("0x");
            printf("%s,", p);
            p = strtok(NULL, " \t\r\n");
	    }
		printf("\n");
	}
	return 0;
}
