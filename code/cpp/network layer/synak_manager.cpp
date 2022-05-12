/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* synak_manager.cpp
*/

#include "synak.h"


CRC::Table<std::uint32_t, 32> SK::SynakManager::m_crcTable(CRC::CRC_32_C());


/* SynakManager::Initialization
** Initialization Network Layer class
*/
void SK::SynakManager::initialization() {
#ifdef _WIN32
    WSADATA wsa;

    if (::WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
        return;
#else
    NULL;
#endif
}

/* SynakManager::Unitialization
** Clean Network Layer class
*/
void SK::SynakManager::desinitialization() {
#ifdef _WIN32
    WSACleanup();
#endif
}



/* SsocketOperations::SsocketOperations
** Initialization, store socket pointer
*/
SK::SsocketOperations::SsocketOperations(SOCKET &_ptrSockfd) {
    m_ptrSockfd = &_ptrSockfd;
}

/* SsocketOperations::optionsAdd
** Add options to the socket
*/
bool SK::SsocketOperations::optionsAdd(std::vector<Sopt> _vecOpts) {
    // For all options stored in the vector
    for (auto elem : std::as_const(_vecOpts)) {
        // Apply the option
        //if (::setsockopt(*m_ptrSockfd, elem.m_iLevel, elem.m_iOptName, (void*)&elem.m_aOptVal, sizeof(elem.m_aOptVal)) != 0) {
        if (::setsockopt(*m_ptrSockfd, elem.m_iLevel, elem.m_iOptName, (const char*)&elem.m_aOptVal, sizeof(elem.m_aOptVal)) != 0) {
            SK_SHOWERROR(SK_FILENLINE, STRERROR);
            return false;
        }
        // The option has been successfully applied
        else {
            // Create a temporary option initialized to zero
            socklen_t  iOptLen( sizeof(elem.m_aOptVal) );
            char* cArrOptVal( new char[iOptLen] );
            ::memset(cArrOptVal, 0, iOptLen);

            // Get the current option state of the socket
            //if (::getsockopt(*m_ptrSockfd, elem.m_iLevel, elem.m_iOptName, (void*)cArrOptVal, &iOptLen) != 0) {
            if (::getsockopt(*m_ptrSockfd, elem.m_iLevel, elem.m_iOptName, (char*)cArrOptVal, &iOptLen) != 0) {
                SK_SHOWERROR(SK_FILENLINE, STRERROR);
                return false;
            }
            // Check if the current option's state is equal
            else if (::memcmp(cArrOptVal, &elem.m_aOptVal, iOptLen) != 0) {
                SK_SHOWERROR(SK_FILENLINE, STRERROR);
                return false;
            }
        }
    }
    // All options have been applied successfully
    return true;
}


/* SsocketOperations::socketCreate
** Create a new socket and store it
*/
bool SK::SsocketOperations::socketCreate() {
    // Create a new socket
    if ((*m_ptrSockfd = ::socket(AF_INET6, SOCK_STREAM, 0)) == SOCKET_ERROR) {
        SK_SHOWERROR(SK_FILENLINE, STRERROR);
        return false;
    }
    return true;
}


/* SsocketOperations::socketBind
** Bind the socket to an IP/PORT
*/
bool SK::SsocketOperations::socketBind(uint16_t _ui8Port, in6_addr _addr6in) {
    // Initializing the local address/port
    sockaddr_in6 addrAccept;
    ::memset(&addrAccept, 0, sizeof(addrAccept));
    addrAccept.sin6_addr = _addr6in;
    addrAccept.sin6_port = htons(_ui8Port);
    addrAccept.sin6_family = AF_INET6;

    // Bind the socket to that address
    if (::bind(*m_ptrSockfd, (sockaddr*)&addrAccept, INET6_ADDRSTRLEN) == SOCKET_ERROR) {
        SK_SHOWERROR(SK_FILENLINE, STRERROR);
        return false;
    }

    // Bind successful
    return true;
}
