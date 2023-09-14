#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
    pid_t parent_pid = getpid();
    printf("Processo pai %d criou:\n", parent_pid);

    for (int i = 1; i <= 4; i++) {
        pid_t child_pid = fork();

        if (child_pid == -1) {
            perror("Erro na criação do processo filho");
            exit(1);
        } else if (child_pid == 0) {
            // Este trecho de código será executado pelo processo filho
            printf("Processo filho %d\n", getpid());
            exit(0);
        } else {
            // Este trecho de código será executado pelo processo pai
            printf("Processo pai %d criou %d\n", parent_pid, child_pid);
        }
    }

    return 0;
}