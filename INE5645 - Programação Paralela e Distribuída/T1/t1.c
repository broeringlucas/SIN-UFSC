#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <semaphore.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <stdbool.h>

// compilar com gcc -o t1 t1.c -lpthread
// Trocar n_sensores e n_atuadores para o valor desejado e compilar novamente
#define N_SENSORES 5
#define N_ATUADORES 5
#define THREADS_POOL 8
#define BUFFER_SIZE 5
#define MAX_ITEMS 10
sem_t empty;
sem_t full;

pthread_mutex_t mutexBuffer;
pthread_mutex_t mutexFila;
pthread_cond_t condFila;
pthread_mutex_t *mutexAtuador[N_ATUADORES];
pthread_mutex_t mutexTarefasConcluidas;
pthread_mutex_t mutexChance;

int buffer[BUFFER_SIZE];

typedef struct Tarefa
{
    int atuador;
    int nivel_de_atividade;
} Tarefa;

Tarefa tarefaFila[MAX_ITEMS];
int tarefaCount = 0;

int produced_count = 0;
int consumed_count = 0;
int in = 0;
int out = 0;

int atuadorTable[N_ATUADORES];

int tarefasConcluidas = 0;

bool should_exit = false;

void signal_thread_exit() {
    should_exit = true;
    pthread_cond_broadcast(&condFila); 
    printf("Thread exit signal sent.\n");
}

void alterarComportamento(Tarefa* t) {
    int * atuador = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    int * nivel_de_atividade = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    int * stMudanca = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    pid_t child;
    int stChild;
    child = fork();

    if(child < 0) {
        perror("fork");
        exit(0);
    }

    if(child == 0) {
        *atuador = t->atuador;
        *stMudanca = 0;

        int chance = rand() % 100;

        if (chance <= 20) {
            *stMudanca = 1;
            exit(0);
        } else {
            *nivel_de_atividade = t->nivel_de_atividade;
            pthread_mutex_lock(mutexAtuador[*atuador]);
            atuadorTable[*atuador] = *nivel_de_atividade;
            sleep(rand() % 2 + 2);
            pthread_mutex_unlock(mutexAtuador[*atuador]);
            exit(0);
        }

        exit(0);
    }
    waitpid(child, &stChild, 0);

    int chance = rand() % 100;
    if (chance <= 20 || *stMudanca == 1) {
        printf("Atuador: %d Falhou\n", *atuador);
        sleep(1);
    } else {
        printf("Atuador: %d, Nivel de atividade: %d\n", *atuador, *nivel_de_atividade);
        sleep(1);
    }

    pthread_mutex_lock(&mutexTarefasConcluidas);
    tarefasConcluidas++;
    if (tarefasConcluidas == MAX_ITEMS) {
        signal_thread_exit();
    } 
    pthread_mutex_unlock(&mutexTarefasConcluidas);
}

void submeterTarefa(Tarefa t) {
    pthread_mutex_lock(&mutexFila);
    tarefaFila[tarefaCount] = t;
    tarefaCount++;
    pthread_mutex_unlock(&mutexFila);
    pthread_cond_signal(&condFila);
}

void* unidade_controle(void* args) {
    while (!should_exit) {
        Tarefa t;

        pthread_mutex_lock(&mutexFila);
        while (tarefaCount == 0 && !should_exit) {
            pthread_cond_wait(&condFila, &mutexFila);
        }

        if (should_exit) { 
            pthread_mutex_unlock(&mutexFila);
            break; 
        }
        
        t = tarefaFila[0];
        for (int i = 0; i < tarefaCount - 1; i++) {
            tarefaFila[i] = tarefaFila[i + 1];
        }

        tarefaCount--;

        pthread_mutex_unlock(&mutexFila);
        alterarComportamento(&t);
    }

    pthread_exit(NULL); 
}


void *sensor(void *arg) {
    while (produced_count < MAX_ITEMS) {
        int ds = rand() % 1000;
        int interval = rand() % 5 + 1;
        sleep(interval);

        sem_wait(&empty);
        pthread_mutex_lock(&mutexBuffer);

        buffer[in] = ds;

        in = (in + 1) % BUFFER_SIZE;
        
        produced_count++;
        pthread_mutex_unlock(&mutexBuffer);

        sem_post(&full);

    }
    pthread_exit(NULL);
}


void *central_de_controle(void *arg) {
    while (consumed_count < MAX_ITEMS) {
        int ds = -1;
        int atuador;
        int nivel_de_atividade;
        
        sem_wait(&full);
        pthread_mutex_lock(&mutexBuffer);

        ds = buffer[out];
        atuador = ds % N_ATUADORES;
        nivel_de_atividade = rand() % 100;

        Tarefa t = {
            .atuador = atuador,
            .nivel_de_atividade = nivel_de_atividade};

        out = (out + 1) % BUFFER_SIZE;
        submeterTarefa(t);
        consumed_count++;

        pthread_mutex_unlock(&mutexBuffer);
        sem_post(&empty);
    }

    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    srand(time(NULL));

    struct timeval t1, t2;
    double t_total;

    pthread_t sensor_thread[N_SENSORES], central_de_controle_thread, pool_thread[THREADS_POOL];
    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);

    pthread_mutex_init(&mutexBuffer, NULL);
    pthread_mutex_init(&mutexFila, NULL);
    pthread_cond_init(&condFila, NULL);
    pthread_mutex_init(&mutexTarefasConcluidas, NULL);
    pthread_mutex_init(&mutexChance, NULL);

    for (int i = 0; i < N_ATUADORES; i++) {
        mutexAtuador[i] = mmap(NULL, sizeof(pthread_mutex_t), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
        pthread_mutex_init(mutexAtuador[i], NULL);
    }

    gettimeofday(&t1, NULL);
    for (int i = 0; i < N_SENSORES; i++) {
        pthread_create(&sensor_thread[i], NULL, &sensor, NULL);
    }

    for (int i = 0; i < THREADS_POOL; i++) {
        pthread_create(&pool_thread[i], NULL, &unidade_controle, NULL);
    }

    pthread_create(&central_de_controle_thread, NULL, &central_de_controle, NULL);

    for (int i = 0; i < N_SENSORES; i++) {
        pthread_join(sensor_thread[i], NULL);
        printf("Sensor %d finalizado\n", i);
    }

    for (int i = 0; i < THREADS_POOL; i++) {
        pthread_join(pool_thread[i], NULL);
    }

    pthread_join(central_de_controle_thread, NULL);

    gettimeofday(&t2, NULL);

    t_total = (t2.tv_sec - t1.tv_sec) + ((t2.tv_usec - t1.tv_usec) / 1000000.0);

    sem_destroy(&empty);
    sem_destroy(&full);
    pthread_mutex_destroy(&mutexBuffer);
    pthread_mutex_destroy(&mutexFila);
    pthread_mutex_destroy(&mutexTarefasConcluidas);
    pthread_mutex_destroy(&mutexChance);
    
    for (int i = 0; i < N_ATUADORES; i++) {
        pthread_mutex_destroy(mutexAtuador[i]);
    }

    pthread_cond_destroy(&condFila);

    printf("Tempo total: %f\n", t_total);

    return 0;
}