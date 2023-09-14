#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

void create_child_processes(int parent_pid, int depth, int max_depth) {
    if (depth > max_depth) {
        return;
    }

    for (int i = 0; i < 2; i++) {
        pid_t child_pid = fork();

        if (child_pid == -1) {
            perror("Erro na criação do processo filho");
            exit(1);
        } else if (child_pid == 0) {
            // Este trecho de código será executado pelo processo filho
            printf("Processo %d filho de %d\n", getpid(), parent_pid);
            create_child_processes(getpid(), depth + 1, max_depth);
            exit(0);
        }
    }
}

int main() {
    int parent_pid = getpid();
    printf("Processo pai %d\n", parent_pid);

    create_child_processes(parent_pid, 1, 2);

    // O processo pai espera que todos os processos filhos terminem
    for (int i = 0; i < 2; i++) {
        wait(NULL);
    }

    return 0;
}
