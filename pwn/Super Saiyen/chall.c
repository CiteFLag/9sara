#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct super_saiyan {
    char hero_name[32];
    void (*show_power)(struct super_saiyan *);
};

void display_power(struct super_saiyan *h) {
    printf("Hero: %s is ready to fight evil!\n", h->hero_name);
}

void legendary_saiyan() {
    printf("You have awakened your Legendary Saiyan powers!\n");
    system("/bin/sh");
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    
    printf("===== ANIME HEROES ACADEMY =====\n");
    printf("Only the Legendary Saiyan can access the ultimate power...\n\n");
    
    struct super_saiyan *student = malloc(sizeof(struct super_saiyan));
    struct super_saiyan *sensei = malloc(sizeof(struct super_saiyan));
    
    student->show_power = display_power;
    sensei->show_power = display_power;
    
    printf("Enter hero name for new student: ");
    char input[256];
    fgets(input, 256, stdin);
    
    strcpy(student->hero_name, input);
    
    printf("\n[Student demonstrating powers]\n");
    student->show_power(student);
    
    printf("\n[Sensei demonstrating powers]\n");
    sensei->show_power(sensei);
    
    free(student);
    free(sensei);
    
    return 0;
} 