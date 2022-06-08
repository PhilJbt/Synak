/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server's Panel Web watcher
* synak_masterserver_webpanel.cpp
*/

#include "master server/synak_masterserver.h"

int SK::MasterServer::m_WP_fdPipeKill[2] { -1, -1 };


/* SynakManager::WP_signalBlockAllExcept
** Block unix signals
** If no flag provided to int _iFlags, all flags are blocked
*/
void SK::MasterServer::WP_signalBlockAllExcept(int _iFlags) {
    sigset_t ssIgnoreAll;
    ::sigemptyset(&ssIgnoreAll);
    ::sigfillset(&ssIgnoreAll);
    if (_iFlags > 0)
        ::sigdelset(&ssIgnoreAll, _iFlags);
    ::pthread_sigmask(SIG_SETMASK, &ssIgnoreAll, NULL);
}

/* MasterServer::WP_signalHandler
** Handle unix signals sent from Web Panel
*/
void SK::MasterServer::WP_signalHandler(int _signum) {
    m_bRun = false;
    ::write(m_WP_fdPipeKill[1], "1", ::strlen("1"));
    //::exit(_signum);
}

/* MasterServer::WatcherTerminal
** Launch the threaded Terminal Watcher
*/
void SK::MasterServer::WP_watcherTerminal_Launch() {
    if (!m_WP_thdWatcherTerminal)
        m_WP_thdWatcherTerminal = new std::thread(&MasterServer::WP_watcherTerminal_thd, this);
}

/* MasterServer::WP_watcherTerminal_thd
** Monitors for an keyboard input in the terminal
*/
void SK::MasterServer::WP_watcherTerminal_thd() {
    WP_signalBlockAllExcept(SIGUSR1);

    // Initialize input command string
    std::string strCmd;

    // Check commands written in the terminal
    int epfd = ::epoll_create(3);
    if(epfd == -1)
        SK_LOG_ERR(STRERROR);

    epoll_event ev[3];

    int iFlagsCreate(EPOLLIN | EPOLLOUT | EPOLLRDHUP | EPOLLERR);
    epollAdd(&ev[0], epfd, ::fileno(stdin),    EPOLL_CTL_ADD, true, iFlagsCreate);
    epollAdd(&ev[1], epfd, m_WP_fdPipeKill[0], EPOLL_CTL_ADD, true, iFlagsCreate);
    epollAdd(&ev[2], epfd, m_WP_fdPipeKill[1], EPOLL_CTL_ADD, true, iFlagsCreate);

    while(m_bRun) {
        int nfds = ::epoll_wait(epfd, ev, 3, 60000);
        if(nfds < 0)
            SK_LOG_ERR(STRERROR);
        else {
            for(int i = 0; i < nfds; ++i) {
                if(ev[i].data.fd == ::fileno(stdin)
                    && ev[i].events & EPOLLIN) {
                    std::getline(std::cin, strCmd);
                    if(strCmd == "stop") {
                        m_bRun = false;
                        ::write(m_WP_fdPipeKill[1], "1", ::strlen("1"));
                    }
                }
            }
        }
    }

    epollAdd(&ev[0], epfd, ::fileno(stdin),    EPOLL_CTL_DEL);
    epollAdd(&ev[1], epfd, m_WP_fdPipeKill[0], EPOLL_CTL_DEL);
    epollAdd(&ev[2], epfd, m_WP_fdPipeKill[1], EPOLL_CTL_DEL);
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
void SK::MasterServer::WP_watcherWebPanel_Launch(int _iPort) {
    linger sl { 1, 0 };
    SK::SsocketOperations sockOpts(m_WP_sckfd);
    sockOpts.socketCreate();
    sockOpts.optionsAdd({
        { SOL_SOCKET,	SO_REUSEADDR,	1  },
        { SOL_SOCKET,	SO_REUSEPORT,	1  },
        { IPPROTO_IPV6, IPV6_V6ONLY,	0  },
        { SOL_SOCKET,	SO_LINGER,		sl },
        { IPPROTO_TCP,	TCP_NODELAY,	1  }, // Disable Nagle's algorithm
        { IPPROTO_TCP,	TCP_CORK,	    0  }  // Disable Cork
    });
    sockOpts.socketBind(static_cast<uint16_t>(_iPort), IN6ADDR_LOOPBACK_INIT);

    // Create pipe for emergency stop
    if (::pipe2(m_WP_fdPipeKill, O_NONBLOCK) == -1)
        SK_LOG_ERR(STRERROR);

    // Launch thread
    if (!m_WP_thdWatcherWebpanel)
        m_WP_thdWatcherWebpanel = new std::thread(&MasterServer::WP_watcherWebPanel_tdh, this);
}

/* MasterServer::WP_watcherWebPanel_tdh
** Monitors for a command input though the web panel
*/
void SK::MasterServer::WP_watcherWebPanel_tdh() {
    WP_signalBlockAllExcept(SIGUSR1);

    // Accept web panel incoming connections
    if (::listen(m_WP_sckfd, SOMAXCONN) != 0)
        SK_LOG_ERR(STRERROR);

    // Check incoming web panel instructions
    int epfd = ::epoll_create(3);
    if(epfd == -1)
        SK_LOG_ERR(STRERROR);

    epoll_event ev[3];

    int iFlagsCreate(EPOLLIN | EPOLLOUT | EPOLLRDHUP | EPOLLERR);
    epollAdd(&ev[0], epfd, m_WP_sckfd,         EPOLL_CTL_ADD, true, iFlagsCreate);
    epollAdd(&ev[1], epfd, m_WP_fdPipeKill[0], EPOLL_CTL_ADD, true, iFlagsCreate);
    epollAdd(&ev[2], epfd, m_WP_fdPipeKill[1], EPOLL_CTL_ADD, true, iFlagsCreate);

    while(m_bRun) {
        int nfds = ::epoll_wait(epfd, ev, 3, 60000);
        if(nfds < 0)
            SK_LOG_ERR(STRERROR);
        else {
            for(int i = 0; i < nfds; ++i) {
                if(ev[i].data.fd == m_WP_sckfd
                    && ev[i].events & EPOLLIN) {
                    in6_addr  addrRecv { 0 };
                    socklen_t len(sizeof(addrRecv));
                    SOCKET m_sckfdNew = ::accept(m_WP_sckfd, (sockaddr *)&addrRecv, &len);
                    if(m_sckfdNew == SOCKET_ERROR)
                        SK_LOG_ERR(STRERROR);
                    else {
                        // Receive checksum
                        std::uint32_t ui32CrcRecv(0);
                        if (::recv(m_sckfdNew, &ui32CrcRecv, sizeof(ui32CrcRecv), MSG_NOSIGNAL) <= 0)
                            SK_LOG_ERR(STRERROR);
                        else {
                            // Receive message size
                            std::uint32_t ui32BuffSize(0);
                            if (::recv(m_sckfdNew, &ui32BuffSize, sizeof(ui32BuffSize), MSG_NOSIGNAL) <= 0)
                                SK_LOG_ERR(STRERROR);
                            else {
                                // Cast buffer size to host-endianness
                                ui32BuffSize = ::ntohl(ui32BuffSize);

                                // If the size of the payload does not exceed 5 megabytes
                                if (ui32BuffSize <= 5242880) {
                                    // Cast cheskum to host-endianness
                                    ui32CrcRecv = ::ntohl(ui32CrcRecv);

                                    // Declare and initialize packet payload buffer
                                    // with 4 extra bytes corresping to the payload length,
                                    // the latter being part of the data calculated for the checksum
                                    char *ptrRecvBeg(new char[ui32BuffSize + sizeof(ui32BuffSize)]);
                                    ::memset(ptrRecvBeg, 0, ui32BuffSize + sizeof(ui32BuffSize));

                                    // Copy the payload length into the receive buffer
                                    ::memcpy(ptrRecvBeg, &ui32BuffSize, sizeof(ui32BuffSize));

                                    // Receive the payload data
                                    char *ptrRecvDat(ptrRecvBeg + sizeof(ui32BuffSize));
                                    if (::recv(m_sckfdNew, ptrRecvDat, ui32BuffSize, MSG_NOSIGNAL) <= 0)
                                        SK_LOG_ERR(STRERROR);
                                    else {
                                        // Verify checksum
                                        std::uint32_t ui32CrcRecvVerif;
                                        ui32CrcRecvVerif = crc32_fast(ptrRecvBeg, ui32BuffSize + sizeof(ui32BuffSize), 0);
                                        if (ui32CrcRecv != ui32CrcRecvVerif)
                                            SK_LOG_ERR("Checksum is not valid.", ui32CrcRecv, ui32CrcRecvVerif);
                                        else {
                                            // Try to parse received json
                                            bool           bJsonParsed(true);
                                            int            iError(-1);
                                            std::string    strErrMess;
                                            nlohmann::json jRecv,
                                                           jSend;
                                            try {
                                                jRecv = nlohmann::json::parse(std::string(ptrRecvDat, ui32BuffSize));
                                            }
                                            catch (const std::exception &_e) {
                                                SK_LOG_ERR("json parse error:", _e.what(), "data:", std::string(ptrRecvDat, ui32BuffSize)/*, "data size:", static_cast<int>(ui32BuffSize)*/);
                                                bJsonParsed = false;
                                            }
                                            if (bJsonParsed) {
                                                std::cerr << jRecv.dump() << std::endl;

                                                if (!jRecv.is_null()
                                                    && jRecv.contains("type")) {
                                                    bool bHasData(jRecv.contains("data"));

                                                    // Master Server statistics
                                                    if (jRecv.at("type").get<std::string>() == "stats") {
                                                        jSend["type"] = "stats";
                                                        jSend["data"]["conn"] = "-1";
                                                        jSend["data"]["prty"] = "-2";
                                                    }
                                                    // Master Server options get
                                                    else if (jRecv.at("type").get<std::string>() == "optgt") {
                                                        jSend["type"] = "optgt";
                                                        jSend["data"]["lglv"] = std::to_string(static_cast<int>(m_LW_eLogLevel));
                                                    }
                                                    // Master Server options set
                                                    else if (jRecv.at("type").get<std::string>() == "optst"
                                                        && bHasData) {
                                                        jSend["type"] = "optst";

                                                        if (jRecv["data"].contains("lglv")) {
                                                            bool bstoiErr(false);
                                                            int iLglv_tmp(0);
                                                            try {
                                                                iLglv_tmp = std::stoi(jRecv["data"].at("lglv").get<std::string>());
                                                            }
                                                            catch (const std::exception &_e) {
                                                                SK_LOG_ERR("std::stoi failed:", _e.what(), "data:", std::string(ptrRecvDat, ui32BuffSize));
                                                                bstoiErr = true;
                                                            }
                                                            if (!bstoiErr
                                                                && (static_cast<int>(m_LW_eLogLevel) != iLglv_tmp)) {
                                                                m_LW_eLogLevel = static_cast<SK::MasterServer::eLogType>(iLglv_tmp);
                                                                jSend["data"]["lglv"] = std::to_string(static_cast<int>(m_LW_eLogLevel));

                                                                // Update the configuration file
                                                                configBackup();
                                                            }
                                                        }

                                                        if (!jSend.contains("data")
                                                            || jSend["data"].empty()) {
                                                            strErrMess = "The values of the sent options are the same as those currently used.";
                                                            iError = 1;
                                                        }
                                                    }
                                                    else {
                                                        strErrMess = "Unknown type, or no data.";
                                                        iError = 2;
                                                    }
                                                }
                                                else {
                                                    strErrMess = "Type is missing.";
                                                    iError = 2;
                                                }
                                            }
                                            else {
                                                strErrMess = "Json cannot be parsed.";
                                                iError = 2;
                                            }

                                            if (iError > -1) {
                                                jSend = nlohmann::json();
                                                jSend["type"] = "erro";
                                                jSend["data"]["titl"] = "MASTER SERVER ANSWER";
                                                jSend["data"]["mess"] = strErrMess;

                                                switch (iError) {
                                                case 0:
                                                {
                                                    jSend["data"]["colr"] = "blue";
                                                    jSend["data"]["icon"] = "info circle";
                                                    jSend["data"]["mess"] = strErrMess;
                                                }
                                                break;
                                                case 1:
                                                {
                                                    jSend["data"]["colr"] = "orange";
                                                    jSend["data"]["icon"] = "exclamation circle";
                                                    jSend["data"]["mess"] = strErrMess;
                                                }
                                                break;
                                                case 2:
                                                {
                                                    jSend["data"]["colr"] = "red";
                                                    jSend["data"]["icon"] = "exclamation triangle";
                                                    jSend["data"]["mess"] = strErrMess;
                                                }
                                                break;
                                                }
                                                jSend["data"] = jSend["data"].dump();
                                            }

                                            // Serialize Json
                                            std::string strJson(jSend.dump());

                                            // Calculate message size (network-endianness)
                                            std::uint32_t uiMesslen(::htonl(static_cast<std::uint32_t>(strJson.length())));

                                            // Declare and initiliaze checksum placeholder
                                            std::uint32_t ui32CrcSend(0);

                                            // Calculate the packet length
                                            std::uint32_t ui32Messlen {
                                                static_cast<std::uint32_t>(
                                                    sizeof(uiMesslen) + sizeof(ui32CrcSend)
                                                )
                                                + static_cast<std::uint32_t>(
                                                    strJson.length()
                                                )
                                            };

                                            // Declare and initialize sending buffer and its pointers
                                            char *ptrBuffMessSend_Raw(new char[ui32Messlen]),
                                                 *ptrBuffMessSend_Chk(ptrBuffMessSend_Raw),
                                                 *ptrBuffMessSend_Len(ptrBuffMessSend_Chk + sizeof(ui32CrcSend)),
                                                 *ptrBuffMessSend_Dat(ptrBuffMessSend_Len + sizeof(uiMesslen));
                                            ::memset(ptrBuffMessSend_Raw, 0, ui32Messlen);

                                            // Populate sending buffer with payload length
                                            ::memcpy(ptrBuffMessSend_Len, &uiMesslen, sizeof(uiMesslen));

                                            // Populate sending buffer with payload
                                            ::memcpy(ptrBuffMessSend_Dat, strJson.data(), strJson.length());

                                            // Calculate checksum (network-endianness)
                                            ui32CrcSend = ::htonl(crc32_fast(ptrBuffMessSend_Len, sizeof(uiMesslen) + strJson.length(), 0));

                                            // Populate sending buffer with checksum
                                            ::memcpy(ptrBuffMessSend_Chk, &ui32CrcSend, sizeof(ui32CrcSend));

                                            // Send
                                            if (::send(m_sckfdNew, ptrBuffMessSend_Raw, ui32Messlen, MSG_NOSIGNAL) == -1)
                                                SK_LOG_ERR(STRERROR);

                                            // Erase sending buffer
                                            delete[] ptrBuffMessSend_Raw;
                                        }
                                    }
                                    delete[] ptrRecvBeg;
                                }
                                else
                                    SK_LOG_ERR("Data size exceed the 5MB limit.", ui32BuffSize);
                            }
                        }
                    }

                    SK_CLOSESOCKET(m_sckfdNew);
                }
            }
        }
    }

    epollAdd(&ev[0], epfd, m_WP_sckfd,         EPOLL_CTL_DEL);
    epollAdd(&ev[1], epfd, m_WP_fdPipeKill[0], EPOLL_CTL_DEL);
    epollAdd(&ev[2], epfd, m_WP_fdPipeKill[1], EPOLL_CTL_DEL);

    SK_CLOSESOCKET(m_WP_sckfd);
}
