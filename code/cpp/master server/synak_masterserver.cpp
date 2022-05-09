/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* synak_masterserver.cpp
*/

#include <network layer/synak.h>
#include <master server/synak_masterserver.h>
#include <master server/synak_masterserver_define.h>


int SK::MasterServer::m_fdPipeKill[2] { -1, -1 };
int SK::MasterServer::m_iLogID { 0 };
volatile std::atomic_bool SK::MasterServer::m_bRun { false };

/* MasterServer::Initialization
** Initialization the Master Server class
*/
void SK::MasterServer::initialization() {
    m_bRun = true;

    signalBlockAllExcept();

    struct sigaction sigbreak;
    ::sigemptyset(&sigbreak.sa_mask);
    sigbreak.sa_handler = &MasterServer::signalHandler;
    sigbreak.sa_flags = 0;
    if (::sigaction(SIGUSR1, &sigbreak, NULL) != 0)
        SK_WRITELOG(SK_FILENLINE, { STRERROR });
}

/* MasterServer::Unitialization
** Clean the Master Server class
*/
void SK::MasterServer::desinitialization() {
    m_bRun = false;

    // Close the terminal watcher thread
    if (m_thdWatcherTerminal) {
        m_thdWatcherTerminal->join();
        delete m_thdWatcherTerminal;
        m_thdWatcherTerminal = nullptr;
    }

    // Close the webpanel watcher thread
    if (m_thdWatcherWebpanel) {
        m_thdWatcherWebpanel->join();
        delete m_thdWatcherWebpanel;
        m_thdWatcherWebpanel = nullptr;
    }
    SK_CLOSESOCKET(m_sckfdWP);

    // Close shutdown pipe notification
    ::close(m_fdPipeKill[0]);
    ::close(m_fdPipeKill[1]);
}

/* SynakManager::signalBlockAllExcept
** Block unix signals
** If no flag provided to int _iFlags, all flags are blocked
*/
void SK::MasterServer::signalBlockAllExcept(int _iFlags) {
    sigset_t ssIgnoreAll;
    ::sigemptyset(&ssIgnoreAll);
    ::sigfillset(&ssIgnoreAll);
    if (_iFlags > 0)
        ::sigdelset(&ssIgnoreAll, _iFlags);
    ::pthread_sigmask(SIG_SETMASK, &ssIgnoreAll, NULL);
}

/* MasterServer::signalHandler
** Handle unix signals sent from Web Panel
*/
void SK::MasterServer::signalHandler(int _signum) {
    std::cerr << "SIGUSR1" << std::endl;
    m_bRun = false;
    ::write(m_fdPipeKill[1], "1", ::strlen("1"));
    //::exit(_signum);
}

/* MasterServer::WatcherTerminal
** Launch the threaded Terminal Watcher
*/
void SK::MasterServer::watcherTerminal() {
    if (!m_thdWatcherTerminal)
        m_thdWatcherTerminal = new std::thread(&MasterServer::_watcherterminal, this);
}

/* MasterServer::_watcherterminal
** Monitors for an keyboard input in the terminal
*/
void SK::MasterServer::_watcherterminal() {
    signalBlockAllExcept(SIGUSR1);

    // Initialize input command string
    std::string strCmd;
    
    // Check commands written in the terminal
    int epfd = ::epoll_create(3);
    if(epfd == -1)
        SK_WRITELOG(SK_FILENLINE, { STRERROR });

    epoll_event ev[3];

    int iFlagsCreate { EPOLLIN | EPOLLOUT | EPOLLRDHUP | EPOLLERR };    
    epollAdd(&ev[0], epfd, ::fileno(stdin), EPOLL_CTL_ADD, true, iFlagsCreate);
    epollAdd(&ev[1], epfd, m_fdPipeKill[0], EPOLL_CTL_ADD, true, iFlagsCreate);
    epollAdd(&ev[2], epfd, m_fdPipeKill[1], EPOLL_CTL_ADD, true, iFlagsCreate);

    while(m_bRun) {
        int nfds = ::epoll_wait(epfd, ev, 3, 60000);
        if(nfds < 0)
            SK_WRITELOG(SK_FILENLINE, { STRERROR });
        else {
            for(int i = 0; i < nfds; ++i) {
                if(ev[i].data.fd == ::fileno(stdin)
                    && ev[i].events & EPOLLIN) {
                    std::getline(std::cin, strCmd);
                    if(strCmd == "stop") {
                        m_bRun = false;
                        ::write(m_fdPipeKill[1], "1", ::strlen("1"));
                    }
                }
            }
        }
    }

    epollAdd(&ev[0], epfd, ::fileno(stdin), EPOLL_CTL_DEL);
    epollAdd(&ev[1], epfd, m_fdPipeKill[0], EPOLL_CTL_DEL);
    epollAdd(&ev[2], epfd, m_fdPipeKill[1], EPOLL_CTL_DEL);
}

/* SynakManager::epollAdd
** Add file descriptor to epoll event watcher
*/
void SK::MasterServer::epollAdd(epoll_event *_ev, const int &_epfd, int _fd, int _iAction, bool _bAssign, int _iFlags) {
    if (_bAssign) {
        _ev->events = _iFlags;
        _ev->data.fd = _fd;
    }
    if (::epoll_ctl(_epfd, _iAction, _fd, _ev) != 0)
        SK_SHOWERROR(SK_FILENLINE, STRERROR);
}

/* MasterServer::WatcherTerminal
** Launch the threaded Terminal Watcher
*/
void SK::MasterServer::watcherWebpanel(uint16_t _ui8Port) {
    linger sl { 1, 0 };
    SK::SsocketOperations sockOpts(m_sckfdWP);
    sockOpts.socketCreate();
    sockOpts.optionsAdd({
        { SOL_SOCKET,	SO_REUSEADDR,	1  },
        { SOL_SOCKET,	SO_REUSEPORT,	1  },
        { IPPROTO_IPV6, IPV6_V6ONLY,	0  },
        { SOL_SOCKET,	SO_LINGER,		sl },
        { IPPROTO_TCP,	TCP_NODELAY,	1  }, // Disable Nagle's algorithm
        { IPPROTO_TCP,	TCP_CORK,	    0  }  // Disable Cork
    });
    sockOpts.socketBind(_ui8Port);

    // Create pipe for emergency stop
    if (::pipe2(m_fdPipeKill, O_NONBLOCK) == -1)
        SK_WRITELOG(SK_FILENLINE, { STRERROR });

    // Launch thread
    if (!m_thdWatcherWebpanel)
        m_thdWatcherWebpanel = new std::thread(&MasterServer::_watcherwebpanel, this);
}

/* MasterServer::_watcherwebpanel
** Monitors for a command input though the web panel
*/
void SK::MasterServer::_watcherwebpanel() {
    signalBlockAllExcept(SIGUSR1);

    // Accept web panel incoming connections
    if (::listen(m_sckfdWP, SOMAXCONN) != 0)
        SK_WRITELOG(SK_FILENLINE, { STRERROR });

    // Check incoming web panel instructions
    int epfd = ::epoll_create(3);
    if(epfd == -1)
        SK_WRITELOG(SK_FILENLINE, { STRERROR });

    epoll_event ev[3];

    int iFlagsCreate { EPOLLIN | EPOLLOUT | EPOLLRDHUP | EPOLLERR };
    epollAdd(&ev[0], epfd, m_sckfdWP,       EPOLL_CTL_ADD, true, iFlagsCreate);
    epollAdd(&ev[1], epfd, m_fdPipeKill[0], EPOLL_CTL_ADD, true, iFlagsCreate);
    epollAdd(&ev[2], epfd, m_fdPipeKill[1], EPOLL_CTL_ADD, true, iFlagsCreate);

    while(m_bRun) {
        int nfds = ::epoll_wait(epfd, ev, 3, 60000);
        if(nfds < 0)
            SK_WRITELOG(SK_FILENLINE, { STRERROR });
        else {
            for(int i = 0; i < nfds; ++i) {
                if(ev[i].data.fd == m_sckfdWP
                    && ev[i].events & EPOLLIN) {
                    in6_addr  addrRecv { 0 };
                    socklen_t len { sizeof(addrRecv) };
                    SOCKET m_sckfdNew = ::accept(m_sckfdWP, (sockaddr *)&addrRecv, &len);
                    if(m_sckfdNew == SOCKET_ERROR)
                        SK_WRITELOG(SK_FILENLINE, { STRERROR });
                    else {
                        // Receive message size
                        std::uint32_t ui32BuffSize { 0 };
                        if (::recv(m_sckfdNew, &ui32BuffSize, sizeof(ui32BuffSize), MSG_NOSIGNAL) <= 0)
                            SK_WRITELOG(SK_FILENLINE, { STRERROR });
                        else {
                            // Receive checksum
                            std::uint32_t ui32CrcRecv { 0 };
                            if (::recv(m_sckfdNew, &ui32CrcRecv, sizeof(ui32CrcRecv), MSG_NOSIGNAL) <= 0)
                                SK_WRITELOG(SK_FILENLINE, { STRERROR });
                            else {
                                // Cast buffer size to host-endianness
                                ui32BuffSize = ::ntohl(ui32BuffSize);

                                // Cast cheskum to host-endianness
                                ui32CrcRecv = ::ntohl(ui32CrcRecv);

                                // Declare buffer size
                                char *ptrRecv { new char[ui32BuffSize] };
                                if (::recv(m_sckfdNew, ptrRecv, ui32BuffSize, MSG_NOSIGNAL) <= 0)
                                    SK_WRITELOG(SK_FILENLINE, { STRERROR });
                                else {
                                    // Verify checksum
                                    std::uint32_t ui32CrcRecvVerif;
                                    ui32CrcRecvVerif = CRC::Calculate(ptrRecv, ui32BuffSize, SK::SynakManager::m_crcTable);
                                    if (ui32CrcRecv != ui32CrcRecvVerif)
                                        SK_WRITELOG(SK_FILENLINE, { "Checksum is not valid." });
                                    else {
                                        json        jRecv { json::parse(ptrRecv) },
                                                    jSend;
                                        std::string strErrMess;
                                        bool        bError { false };
                                        jRecv = jRecv[0]; // https://github.com/nlohmann/json/issues/1359

                                        if (!jRecv.is_null()
                                            && jRecv.contains("type")) {
                                            // Master Server statistics
                                            if (jRecv.at("type").get<std::string>() == "stats") {
                                                jSend["type"] = "stats";
                                                jSend["data"]["conn"] = "-1";
                                                jSend["data"]["prty"] = "-2";
                                            }
                                            // ...
                                        }
                                        else {
                                            strErrMess = "Type is missing.";
                                            bError = true;
                                        }

                                        if (bError) {
                                            jSend["type"] = "erro";
                                            jSend["data"]["colr"] = "red";
                                            jSend["data"]["icon"] = "exclamation";
                                            jSend["data"]["titl"] = "MASTER SERVER ANSWER";
                                            jSend["data"]["mess"] = strErrMess;
                                            jSend["data"] = jSend["data"].dump();
                                        }

                                        // Serialize Json
                                        std::string strJson { jSend.dump() };

                                        // Calculate message size (network-endianness)
                                        std::uint32_t uiMesslen { ::htonl(static_cast<std::uint32_t>(strJson.length())) };

                                        // Calculate checksum (network-endianness)
                                        std::uint32_t ui32CrcSend { ::htonl(CRC::Calculate(strJson.data(), strJson.length(), SK::SynakManager::m_crcTable)) };

                                        // Pack and send message
                                        std::uint32_t ui32Messlen {
                                            static_cast<std::uint32_t>(
                                                sizeof(uiMesslen) + sizeof(ui32CrcSend)
                                            )
                                            + static_cast<std::uint32_t>(
                                                strJson.length()
                                            )
                                        };
                                        char *ptrBuffMessSend { new char[ui32Messlen] };
                                        ::memset(ptrBuffMessSend,                                           0,              ui32Messlen);
                                        ::memcpy(ptrBuffMessSend,                                           &uiMesslen,     sizeof(uiMesslen));
                                        ::memcpy(ptrBuffMessSend + sizeof(uiMesslen),                       &ui32CrcSend,   sizeof(ui32CrcSend));
                                        ::memcpy(ptrBuffMessSend + sizeof(uiMesslen) + sizeof(ui32CrcSend), strJson.data(), strJson.length());
                                        if (::send(m_sckfdNew, ptrBuffMessSend, ui32Messlen, MSG_NOSIGNAL) == -1)
                                            SK_WRITELOG(SK_FILENLINE, { STRERROR });
                                        delete[] ptrBuffMessSend;
                                    }
                                }
                                delete[] ptrRecv;
                            }
                        }
                    }

                    SK_CLOSESOCKET(m_sckfdNew);
                }
            }
        }
    }

    epollAdd(&ev[0], epfd, m_sckfdWP,       EPOLL_CTL_DEL);
    epollAdd(&ev[1], epfd, m_fdPipeKill[0], EPOLL_CTL_DEL);
    epollAdd(&ev[2], epfd, m_fdPipeKill[1], EPOLL_CTL_DEL);

    SK_CLOSESOCKET(m_sckfdWP);
}

/* MasterServer::writeLog
** Write messages in log file
*/
void SK::MasterServer::writeLog(std::string _strFileLine, std::vector<std::string> _vecMess, std::string _strType, bool _bTruncate) {
    
    std::string strMess { "[" };
    size_t iNbrMess { _vecMess.size() };
    for (unsigned int i = 0; i < iNbrMess; ++i)
        strMess += "\"" + _vecMess[i] + (i < iNbrMess - 1 ? "\"," : "\"]");

    std::string strTime(100, 0);
    std::time_t t = std::time(nullptr);
    strTime.resize(std::strftime(&strTime[0], strTime.size(),
        "%H:%M:%S %d/%m/%Y", std::localtime(&t)));

    std::ios_base::openmode iosOpenmode { std::ios_base::binary | std::ios_base::out | (_bTruncate ? std::ios_base::trunc : std::ios_base::app) };
    std::string strPath { "/synak_ms/synak_ms.log" },
    strLine {
        "[\"" + std::to_string(++m_iLogID) + "\","
        "\"" + _strType + "\","
        "\"" + _strFileLine + "\","
        "\"" + strTime + "\","
        + strMess + "]"
    };
    std::ofstream fLogFile(strPath, iosOpenmode);
    
    if(fLogFile) {
        fLogFile << strLine << std::endl;
        if(fLogFile.bad())
            std::cerr << "Can't write the log file (file permissions?): " << STRERROR << std::endl;
        else {
            fLogFile.close();
            std::cout.flush();
        }
    }
    else
        std::cerr << "Can't open/create the log file (file permissions?): " << STRERROR << std::endl;
}