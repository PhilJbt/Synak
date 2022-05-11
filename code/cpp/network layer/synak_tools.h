/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* synak_tools.h
*/

#pragma once

#include "network layer/synak.h"

namespace SK {
    class Tools {
    public:
        static void CryptUncrypt(std::uint8_t *ui8Data, std::uint32_t ui32DataLen) {
            for (unsigned int ui = 0; ui < ui32DataLen; ++ui)
                ui8Data[ui] ^= SK::m_ui8ArrKey[ui % SK_ARRSIZE(SK::m_ui8ArrKey)];
        }
    };
}