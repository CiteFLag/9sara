#include <stdio.h>
#include <stdlib.h>

void vuln() {
	char name[64];

	system("printf \"Hey!  I'll repeat anything you say! \n\"");
	fgets(name, 64, stdin);
	printf(name);
}

int main(){
	setvbuf(stdout, NULL, _IONBF, 0);
	puts("Howdy!");
	printf("You might find this useful: %x\n", puts);
	while(1) {
		vuln();
	}
}