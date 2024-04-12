#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <pthread.h>

//#define IMPRIME
#define NUM_THREADS 4

typedef struct {
    int **elementos;
    int inicio;
    int fim;
    int tam;
} ThreadData;

void imprime(int **array, int num_arrays, int size) {
    int i, j;
    for (i = 0; i < num_arrays; i++) {
        for (j = 0; j < size; j++) {
            printf("%d ", array[i][j]);
        }
        printf("\n");
    }
}

int bubble(int *array, unsigned int size) {
    int i, j;
    int temp;
    for (i = 0; i < size - 1; i++) {
        for (j = 0; j < size - i - 1; j++) {
            if (array[j] > array[j + 1]) {
                temp = array[j];
                array[j] = array[j + 1];
                array[j + 1] = temp;
            }
        }
    }
}

void *thread_bubble(void *args) {
    ThreadData *data = (ThreadData *) args;
    int i;
    for (i = data->inicio; i < data->fim; i++) {
        bubble(data->elementos[i], data->tam);
    }
    pthread_exit(NULL);
}

int main(int argc, char **argv) {
    int **elementos, n, tam, i, j;
    struct timeval t1, t2;
    double t_total;

    if (argc != 3) {
        printf("Digite %s Num_arrays Num_elementos\n", argv[0]);
        exit(0);
    }
    n = atoi(argv[1]);
    tam = atoi(argv[2]);

    elementos = (int **) malloc(n * sizeof(int *));
    for (i = 0; i < n; i++)
        elementos[i] = (int *) malloc(tam * sizeof(int));

    srand(time(NULL));

    for (i = 0; i < n; i++)
        for (j = 0; j < tam; j++)
            elementos[i][j] = rand() % 1000;

#ifdef IMPRIME
    printf("Antes da ordenacao!\n");
    imprime(elementos, n, tam);
    printf("\n");
#endif

    gettimeofday(&t1, NULL);
    pthread_t threads[NUM_THREADS];
    ThreadData thread_data[NUM_THREADS];
    int elementos_por_thread = n / NUM_THREADS;
    int elementos_restantes = n % NUM_THREADS;
    int inicio = 0;
    int fim;
    for (i = 0; i < NUM_THREADS; i++) {
        fim = inicio + elementos_por_thread + (i < elementos_restantes ? 1 : 0);
        thread_data[i].elementos = elementos;
        thread_data[i].inicio = inicio;
        thread_data[i].fim = fim;
        thread_data[i].tam = tam;
        pthread_create(&threads[i], NULL, thread_bubble, (void *) &thread_data[i]);
        inicio = fim;
    }

    for (i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    gettimeofday(&t2, NULL);

    t_total = (t2.tv_sec - t1.tv_sec) + ((t2.tv_usec - t1.tv_usec) / 1000000.0);

#ifdef IMPRIME
    printf("apos a ordenacao!\n");
    imprime(elementos, n, tam);
    printf("\n");
#endif

    for (i = 0; i < n; i++) {
        free(elementos[i]);
    }
    free(elementos);

    printf("tempo total = %f\n", t_total);

    return 0;
}

// Cada thread ordena uma quantidade de array