/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* synak_define.h
*/

#pragma once

#include <network layer/synak.h>



#define SK_DEBUG true



#define SK_FILENAME     (::strrchr(__FILE__, '/') ? ::strrchr(__FILE__, '/') + 1 : __FILE__)
#define SK_FILELINE     std::to_string(__LINE__)

#ifndef _WIN32
    #define SOCKET          int
    #define SOCKET_ERROR    -1
    #define STRERROR        SK::SynakManager::strerror_sk()
    #define closesocket(s)  ::close(s)
#else
    #define SOCKET          SOCKET
    #define STRERROR        SK::SynakManager::strerror_sk()
#endif



#define SK_FILENLINE                    SK_FILENAME + std::string(" ") + SK_FILELINE
#define SK_ARRSIZE(ARR)                 sizeof(ARR)/sizeof(ARR[0])
#define SK_CLOSESOCKET(SCKT)            ::shutdown(SCKT, SHUT_RDWR); closesocket(SCKT); SCKT = SOCKET_ERROR
#if(SK_DEBUG == true)
    #define SK_SHOWERROR(MESS, ERR)     std::cerr << MESS << " (" << ERR << ")" << std::endl;
#else
    #define SK_SHOWERROR                NULL
#endif



using socketoptval_t = std::variant<int, linger>;
