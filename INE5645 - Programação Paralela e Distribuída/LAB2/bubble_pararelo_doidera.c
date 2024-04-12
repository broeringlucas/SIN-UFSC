#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <pthread.h>

void imprime(int **array, int num_arrays, int size) {
    int i, j;
    for (i = 0; i < num_arrays; i++) {
        for (j = 0; j < size; j++) {
            printf("%d ", array[i][j]);
        }
        printf("\n");
    }
}

typedef struct {
    int** array;
    int index;
    int size;
} ThreadArgs;

void* bubble(void* arg) {
    ThreadArgs* args = (ThreadArgs*)arg;
    int** array = args->array;
    int index = args->index;
    int size = args->size;
    
    int i, j, temp;
    for (i = 0; i < size - 1; i++) {
        for (j = 0; j < size - i - 1; j++) {
            if (array[index][j] > array[index][j + 1]) {
                temp = array[index][j];
                array[index][j] = array[index][j + 1];
                array[index][j + 1] = temp;
            }
        }
    }
    
    pthread_exit(NULL);
}

int main(int argc, char** argv) {
    int **elementos, n, tam, i, j;
    struct timeval t1, t2;
    double t_total;

    if (argc != 3) {
        printf("Digite %s Num_arrays Num_elementos\n", argv[0]);
        exit(0);
    }
    n = atoi(argv[1]);
    tam = atoi(argv[2]);

    elementos = (int**)malloc(n * sizeof(int*));
    for (i = 0; i < n; i++)
        elementos[i] = (int*)malloc(tam * sizeof(int));

    for (i = 0; i < n; i++)
        for (j = 0; j < tam; j++)
            elementos[i][j] = rand() % 1000;

    gettimeofday(&t1, NULL);

    pthread_t threads[n];
    ThreadArgs args[n];

    for (i = 0; i < n; i++) {
        args[i].array = elementos;
        args[i].index = i;
        args[i].size = tam;
        pthread_create(&threads[i], NULL, bubble, &args[i]);
    }

    for (i = 0; i < n; i++) {
        pthread_join(threads[i], NULL);
    }

    gettimeofday(&t2, NULL);

    t_total = (t2.tv_sec - t1.tv_sec) + ((t2.tv_usec - t1.tv_usec) / 1000000.0);

    printf("tempo total = %f\n", t_total);

    for (i = 0; i < n; i++)
        free(elementos[i]);
    free(elementos);

    return 0;
}

// Cria uma thread para cada vetor, meio errado, mas rápido.