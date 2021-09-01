/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* main.cpp
*/

#include <network layer/synak.h>


int main() {
    SK_SHOWINFO("[START] " + std::to_string(::getpid()) + " " + SK_BUILDTIMESTAMP);

    // Network Layer initialization
    SynakManager mngr_nl;
    mngr_nl.initialization();

    // Master Server initialization
    MasterServer mngr_ms;
    mngr_ms.initialization();
    mngr_ms.watcherTerminal();      // Optional
    mngr_ms.watcherWebpanel(45318); // Optional

    while (mngr_ms.m_bRun);

    mngr_ms.unitialization();
    mngr_nl.unitialization();

    SK_SHOWINFO("[STOP]");

    return 0;
}
