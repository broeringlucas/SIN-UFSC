#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <pthread.h>

#define MAX_NUMBERS 500000000
#define MAX_VALUE 1000
#define NUM_THREADS 4

float numbers[MAX_NUMBERS];

void* process_chunk(void* arg) {
    unsigned int start = *(unsigned int*)arg;
    unsigned int end = start + MAX_NUMBERS / NUM_THREADS;

    for (unsigned int i = start; i < end; i++) {
        numbers[i] = numbers[i] * 0.2 + numbers[i] / 0.3;
    }

    return NULL;
}

int main() {
    struct timeval t1, t2;
    srand(time(NULL));

    for (unsigned int i = 0; i < MAX_NUMBERS; i++)
        numbers[i] = ((float)rand() / (float)RAND_MAX) * MAX_VALUE;

    gettimeofday(&t1, NULL);

    pthread_t threads[NUM_THREADS];
    unsigned int thread_args[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        thread_args[i] = i * (MAX_NUMBERS / NUM_THREADS);
        pthread_create(&threads[i], NULL, process_chunk, &thread_args[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++)
        pthread_join(threads[i], NULL);

    gettimeofday(&t2, NULL);
    double t_total = (t2.tv_sec - t1.tv_sec) + ((t2.tv_usec - t1.tv_usec) / 1000000.0);

    printf("Total time: %f seconds\n", t_total);
    return 0;
}
