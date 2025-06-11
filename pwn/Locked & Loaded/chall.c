#include <stdio.h>
#include <stdlib.h>

int can_read_flag = 0;


int file_found = 0;
int unlocked_one = 0;
int unlocked_two = 0;
int unlocked_three = 0;


void read_flag(){
	if(!(file_found && unlocked_one && unlocked_two && unlocked_three)) {
		printf("You aren't allowed to read the flag!");
		exit(1);
	}
	FILE *f;
	f = fopen("flag.txt","r");
	if (f == NULL){
		printf("flag.txt doesn't exist, try again on the server");
		exit(0);
	}
	char flag[0x32];
	fgets(flag,0x32,f);
	printf("%s\n",flag);
	fflush(stdout);
}

void find_file(char* file) {
	if(strcmp(file, "flag.txt") == 0) {
		file_found = 1;
	}
}

void unlock_one() {
	unlocked_one = 1;
}

void unlock_two(int auth) {
	if(auth == 0x12345678) {
		unlocked_two = 1;
	}
}

void unlock_three(int auth1, int auth2) {
	if(auth1 == 0x1e9c66e6 && auth2 == 0xadaf1212) {
		unlocked_three = 1;
	}
}

void vuln() {
	char data[32];

	printf("Howdy! We have a function to read the flag but you aren't allowed to use it.  Can you convince me otherwise?\n");
	gets(data);
}

int main(){
	setvbuf(stdout, NULL, _IONBF, 0);
	vuln();
}