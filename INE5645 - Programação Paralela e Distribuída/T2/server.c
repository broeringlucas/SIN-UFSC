#include <stdbool.h>
#include "socketUtil.h"

int main() {

    int serverFD = createTCPSocket();
    struct sockaddr_in *address = createAddress("", 2000);

    int result = bind(serverFD, (struct sockaddr *)address, sizeof(*address));

    if (result == 0)
        printf("socket was bound succesfully\n");

    int listenResult = listen(serverFD, 10);

    struct sockaddr_in clientAddress;
    int clientAddressSize = sizeof(struct sockaddr_in);
    int clientSocketFD = accept(serverFD, (struct sockaddr *)&clientAddress, &clientAddressSize);

    char buffer[1024];

    while (true) {
        ssize_t amountReceived = recv(clientSocketFD, buffer, 1024, 0);

        if (amountReceived > 0) {
            buffer[amountReceived] = 0;

            printf("Response was %s\n", buffer);
        }

        if (amountReceived == 0) {
            printf("Client disconnected\n");
            break;
        }

    }

    close(clientSocketFD);
    shutdown(serverFD, SHUT_RDWR);

    return 0;
}