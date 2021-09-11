/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* synak_manager.h
*/

#pragma once

#include <network layer/synak.h>

namespace SK {
    /* struct SsocketOperations
    ** Struct for sockets operations (options, bind, etc)
    */
    struct SsocketOperations {
        /* SsocketOperations::Sopt
        ** Struct used to store socket options
        */
        struct Sopt {
            Sopt(int _iLevel, int _iOptName, socketoptval_t _aOptVal)
                : m_iLevel(_iLevel), m_iOptName(_iOptName), m_aOptVal(_aOptVal) {}

            int m_iLevel  { 0 },
                m_iOptName{ 0 };
            socketoptval_t m_aOptVal;
        };

        SsocketOperations(SOCKET &_ptrSockfd);
        bool optionsAdd(std::vector<Sopt> _vecOpts);
        bool socketCreate();
        bool socketBind(uint16_t _ui8Port, in6_addr _addr6in = IN6ADDR_ANY_INIT);

    private:
        SOCKET *m_ptrSockfd{ nullptr };
    };

    /* class SynakManager
    ** 
    */
    class SynakManager
    {
    public:
        ~SynakManager() {
            unitialization();
        }

        void unitialization();
        void initialization();
        static void signalBlockAllExcept(int _iFlags = 0);

        static void epollAdd(epoll_event *_ev, const int &_epfd, int _fd, int _iAction, bool _bAssign = false, int _iFlags = 0);

        static CRC::Table<std::uint32_t, 32> m_crcTable;

        void _TEST();

    private:
    };
}