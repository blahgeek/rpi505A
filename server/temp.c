
#include <wiringPi.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#define PIN 17

#define READ_NUM 5
#define READ_BIT READ_NUM*8
#define IGNORE_BEGIN 2
#define IGNORE_END 1
#define IGNORE_NUM IGNORE_BEGIN+IGNORE_END

#define LASTBYTE_IS_CHECKSUM 1

int get_usec(struct timeval * t){
    return t->tv_sec * 1000000 + t->tv_usec;
}

int count = 0;
struct timeval time[READ_BIT + 5];

void handle(){
    gettimeofday(time+count, NULL);
    count += 1;
}

int main(int argc, char const *argv[])
{
    int i, j;
    piHiPri(0);
    wiringPiSetupGpio();
    wiringPiISR(PIN, INT_EDGE_RISING, handle);

    pinMode(PIN, INPUT);  // input
    pullUpDnControl(PIN, PUD_UP);  // pull up
    delay(5);
    pinMode(PIN, OUTPUT);
    digitalWrite(PIN, 0);  // write 0
    delay(5);
    pinMode(PIN, INPUT);  // release

    delay(30);   // handling...
    if(count != IGNORE_NUM + READ_BIT){
        printf("Error, please retry.\n");
        return -1;
    }
    uint8_t val[READ_NUM];
    uint8_t sum = 0;
    for(i = 0 ; i < READ_NUM ; i += 1){
        val[i] = 0;
        for(j = IGNORE_BEGIN+8*i ; j < IGNORE_BEGIN+8*(i+1) ; j += 1){
            int tmp = get_usec(time+j+1) - get_usec(time+j);
            val[i] <<= 1;
            if(tmp > 100) val[i] |= 0x01;
        }
        if(i < READ_NUM-1) sum += val[i];
        else if(sum != val[i]){
            printf("Checksum error, please retry.");
            return -2;
        }
    }
    for(i = 0 ; i < READ_NUM-1 ; i += 1)
        printf("%d\n", val[i]);
    return 0;
}
