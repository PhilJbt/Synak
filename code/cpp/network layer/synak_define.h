/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* synak_define.h
*/

#pragma once

#include <network layer/synak.h>



#ifndef _WIN32
    #define SOCKET          int
    #define SOCKET_ERROR    -1
    #define closesocket(s)  ::close(s)
    #define STRERROR        ::strerror(errno)
    #define __FILENAME__    (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)
#endif



#define SK_ARRSIZE(ARR)         sizeof(ARR)/sizeof(ARR[0])
#define SK_BUILDTIMESTAMP       std::string(__DATE__) + " " + std::string(__TIME__)
#define SK_SHOWERROR(MESSAGE)   std::cerr << __FILENAME__ << "::" << __LINE__ << " : " << MESSAGE << std::endl
#define SK_SHOWINFO(MESSAGE)    std::cerr << MESSAGE << std::endl
#define SK_CLOSESOCKET(SCKT)    ::shutdown(SCKT, SHUT_RDWR); closesocket(SCKT); SCKT = SOCKET_ERROR



using socketoptval_t = std::variant<int, linger>;
