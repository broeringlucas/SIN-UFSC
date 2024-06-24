#include <stdbool.h>
#include "socketUtil.h"

int main() {

    int socketFD = createTCPSocket();

    struct sockaddr_in *address = createAddress("127.0.0.1", 2000);

    int result = connect(socketFD, (struct sockaddr *)address, sizeof(*address));;

    if (result == 0)
        printf("Connection was successful\n");

    char *line = NULL;
    size_t lineSize = 0;
    printf("Enter a message: \n");

    while(true) {
        ssize_t charCount = getline(&line, &lineSize, stdin);

        if (charCount > 0) {

            if (strcmp(line, "exit\n") == 0) {
                break;
            }
            
            ssize_t amountWasSent = send(socketFD, line, charCount, 0);
        }
    }

    close(socketFD);
    
    return 0;
}

