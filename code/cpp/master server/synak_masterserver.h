/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* synak_masterserver.h
*/

#pragma once

#include <network layer/synak.h>

namespace SK {
    /* class SynakManager
    **
    */
    class MasterServer {
        friend std::thread;

    public:
        void initialization();
        void desinitialization();
        void watcherTerminal();
        void watcherWebpanel(uint16_t _ui8Port);
        static void epollAdd(epoll_event *_ev, const int &_epfd, int _fd, int _iAction, bool _bAssign = false, int _iFlags = 0);
        static void signalBlockAllExcept(int _iFlags = 0);
        static void signalHandler(int _signum);
        template<typename... Args>
        static void writeLog(std::string _strFileLine, std::string _strType = "ERR", Args&& ... args);

        template<typename T>
        static std::string _writeLog_toStr(T _rval) {
            return std::to_string(_rval);
        }

        static std::string _writeLog_toStr(std::string _str) {
            return _str;
        }

        static std::string _writeLog_toStr(const char *_cz) {
            return std::string(_cz);
        }

        SOCKET m_sckfdWP { SOCKET_ERROR };
        static volatile std::atomic_bool m_bRun;
        static int m_fdPipeKill[2];

        static int  m_iLogID;
        static bool m_bLogTruncate;

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

    /*

    int epfd = ::epoll_create(2);
    if(epfd == -1)
        SK_WRITELOG(SK_FILENLINE, STRERROR);

    epoll_event ev[2];
    ev[0].events = EPOLLIN | EPOLLRDHUP | EPOLLERR;
    ev[0].data.fd = STDIN_FILENO;
    if(::epoll_ctl(epfd, EPOLL_CTL_ADD, STDIN_FILENO, &ev[0]) != 0)
        SK_WRITELOG(SK_FILENLINE, STRERROR);

    ev[1].events = EPOLLIN | EPOLLRDHUP | EPOLLERR;
    ev[1].data.fd = m_fdPipeKill[0];
    if(::epoll_ctl(epfd, EPOLL_CTL_ADD, m_fdPipeKill[0], &ev[0]) != 0)
        SK_WRITELOG(SK_FILENLINE, STRERROR);

    while(m_bRun) {
        int nfds = ::epoll_wait(epfd, ev, 10, 5000);
        if (nfds < 0)
            SK_WRITELOG(SK_FILENLINE, STRERROR);
        else {
            for(int i = 0; i < nfds; ++i) {
                if(ev[i].data.fd == STDIN_FILENO
                    && ev[i].events & EPOLLIN) {
                    std::getline(std::cin, strCmd);
                    if(strCmd == "stop") {
                        m_bRun = false;
                        ::write(m_fdPipeKill[1], "1", strlen("1"));
                    }
                }
            }
        }
    }

    if(::epoll_ctl(epfd, EPOLL_CTL_DEL, STDIN_FILENO, &ev[0]) == -1)
        SK_WRITELOG(SK_FILENLINE, STRERROR);

    if(::epoll_ctl(epfd, EPOLL_CTL_DEL, m_fdPipeKill[0], &ev[1]) == -1)
        SK_WRITELOG(SK_FILENLINE, STRERROR);

    */
}

#define NoExtraWarning_SK_MS_TEMPLATE
#include "synak_masterserver_template.cpp" NoExtraWarning_SK_MS_TEMPLATE
