#ifndef SOCKETUTIL_H
#define SOCKETUTIL_H

#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>

struct sockaddr_in *createAddress(char *ip, int port);

int createTCPSocket();

#endif // SOCKETUTIL_H