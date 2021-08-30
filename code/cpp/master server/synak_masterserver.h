/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* synak_masterserver.h
*/

#pragma once

#include <network layer/synak.h>

/* class SynakManager
**
*/
class MasterServer {
    friend std::thread;

public:
    void initialization();
    void unitialization();
    void watcherTerminal();
    void watcherWebpanel(uint16_t _ui8Port);

    void stop();



    SOCKET m_sckfdWP { SOCKET_ERROR };
    volatile std::atomic_bool m_bRun { false };
    int m_fdPipeKill[2] { -1, -1 };

private:
    void _watcherterminal();
    void _watcherwebpanel();



    std::thread *m_thdWatcherTerminal { nullptr },
                *m_thdWatcherWebpanel { nullptr };
};

/* // MS CLIENTS SOCKET
SOL_SOCKET, SO_KEEPALIVE, 1
IPPROTO_TCP, TCP_KEEPIDLE, 1
IPPROTO_TCP, TCP_KEEPINTVL, 2
IPPROTO_TCP, TCP_KEEPCNT, 15
SOL_SOCKET, SO_RCVBUF, 212990
SOL_SOCKET, SO_SNDBUF, 212990
*/