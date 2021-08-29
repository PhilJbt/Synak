#pragma once

#define _WINSOCKAPI_

// C++
#include <iostream>
#include <cstring>
#include <stdio.h>

// NETWORK
#ifdef _WIN32
    #include <windows.h>
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #include <iphlpapi.h>
    #pragma comment(lib, "Ws2_32.lib")
#else
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    #include <errno.h>
#endif

// DEPENDENCIES
#include <nlohmann/json.hpp>
using json = nlohmann::json;

// SYNAK
#include "synak_define.h"
#include "synak_manager.h"
