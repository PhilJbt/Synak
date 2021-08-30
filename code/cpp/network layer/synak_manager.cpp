/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* synak_manager.cpp
*/

#include <network layer/synak.h>


/* SynakManager::Initialization
** Initialization Network Layer class
*/
void SynakManager::initialization() {
#ifdef _WIN32
    WSADATA wsa;

    if (::WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
        return;
#else
    SynakManager::signalBlockAll();
#endif
}

void SynakManager::signalBlockAll() {
    sigset_t ssIgnoreAll;
    ::sigemptyset(&ssIgnoreAll);
    ::sigfillset(&ssIgnoreAll);
    ::sigprocmask(SIG_SETMASK, &ssIgnoreAll, NULL);
    ::pthread_sigmask(SIG_SETMASK, &ssIgnoreAll, NULL);
}

/* SynakManager::Unitialization
** Clean Network Layer class
*/
void SynakManager::unitialization() {
#ifdef _WIN32
    WSACleanup();
#endif
}

/* SynakManager::_TEST
**
*/
void SynakManager::_TEST() {
#ifdef _WIN32
	if ((sockfd = ::socket(AF_INET6, SOCK_STREAM, IPPROTO_IP)) == INVALID_SOCKET)
		::printf("Could not create socket : %d\n", ::WSAGetLastError());
#else
	
	//sockOpts.socketListen();

	{
		/*char buff[INET6_ADDRSTRLEN] = { 0 };
		::inet_ntop(AF_INET6, &addrAccept.sin6_addr, buff, INET6_ADDRSTRLEN);
		std::cerr << "IP(" << buff << ") PORT(" << ntohs(addrAccept.sin6_port) << ")" << std::endl;*/
	}
	
#endif
}



/* SsocketOperations::SsocketOperations
** Initialization, store socket pointer
*/
SsocketOperations::SsocketOperations(SOCKET &_ptrSockfd) {
    m_ptrSockfd = &_ptrSockfd;
}

/* SsocketOperations::optionsAdd
** Add options to the socket
*/
bool SsocketOperations::optionsAdd(std::vector<Sopt> _vecOpts) {
    // For all options stored in the vector
    for (auto elem : std::as_const(_vecOpts)) {
        // Apply the option
        if (::setsockopt(*m_ptrSockfd, elem.m_iLevel, elem.m_iOptName, (void*)&elem.m_aOptVal, sizeof(elem.m_aOptVal)) != 0) {
            SK_SHOWERROR(STRERROR);
            return false;
        }
        // The option has been successfully applied
        else {
            // Create a temporary option initialized to zero
            socklen_t  iOptLen{ sizeof(elem.m_aOptVal) };
            char* cArrOptVal{ new char[iOptLen] };
            ::memset(cArrOptVal, 0, iOptLen);

            // Get the current option state of the socket
            if (::getsockopt(*m_ptrSockfd, elem.m_iLevel, elem.m_iOptName, (void*)cArrOptVal, &iOptLen) != 0) {
                SK_SHOWERROR(STRERROR);
                return false;
            }
            // Check if the current option's state is equal
            else if (::memcmp(cArrOptVal, &elem.m_aOptVal, iOptLen) != 0) {
                SK_SHOWERROR(STRERROR);
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
bool SsocketOperations::socketCreate() {
    // Create a new socket
    if ((*m_ptrSockfd = ::socket(AF_INET6, SOCK_STREAM, 0)) == SOCKET_ERROR) {
        SK_SHOWERROR(STRERROR);
        return false;
    }
    return true;
}


/* SsocketOperations::socketBind
** Bind the socket to an IP/PORT
*/
bool SsocketOperations::socketBind(uint16_t _ui8Port, in6_addr _addr6in) {
    // Initializing the local address/port
    sockaddr_in6 addrAccept;
    ::memset(&addrAccept, 0, sizeof(addrAccept));
    addrAccept.sin6_addr = _addr6in;
    addrAccept.sin6_port = htons(_ui8Port);
    addrAccept.sin6_family = AF_INET6;

    // Bind the socket to that address
    if (::bind(*m_ptrSockfd, (sockaddr*)&addrAccept, INET6_ADDRSTRLEN) == SOCKET_ERROR) {
        SK_SHOWERROR(STRERROR);
        return false;
    }

    // Bind successful
    return true;
}
