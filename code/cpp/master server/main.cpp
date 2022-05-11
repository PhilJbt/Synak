/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* main.cpp
*/

#define SK_NO_CPP_INCLUDING

#include "network layer/synak.h"
#include "master server/synak_masterserver.h"

#define TYPEFORVARIANT     uint8_t, uint16_t, uint32_t, uint64_t, int8_t, int16_t, int32_t, int64_t, float, double, bool, std::string
using VariantType_t     =  std::variant<TYPEFORVARIANT>;
using ItsOk             =  std::variant< TYPEFORVARIANT, std::vector<VariantType_t>, std::map<uint16_t, VariantType_t> >;


// MESSAGE
struct SMessageData {
public:
    template <typename T>
    void Add(std::string  _strName, const ItsOk &_variant) {
        std::visit(endianSupport { _strName , &m_jReturn }, _variant);
    }

    int Length() {
        return static_cast<int>(m_jReturn.dump().length());
    }

    char* ToCharArray() {
        return m_jReturn.dump().data();
    }

    std::string ToString() {
        return m_jReturn.dump();
    }

    struct endianSupport {
        endianSupport(std::string _strName, nlohmann::json *_jReturn) : m_strName(_strName), m_jReturn(_jReturn) { }

        template< typename T >
        void operator() (const T &_val) const {
            // STD::MAP<VARIANT>
            if constexpr (std::is_same_v<T, std::map<uint16_t, VariantType_t>>) {
                //nlohmann::json j = nlohmann::json::parse(v.begin(), v.end());
                //nlohmann::json j_vec(c_vector);
                std::cerr << "std::map<uint16_t, VariantType_t>" << std::endl;
            }
            // STD::VECTOR<VARIANT>
            else if constexpr (std::is_same_v<T, std::vector<VariantType_t>>) {
                //nlohmann::json j = nlohmann::json::parse(v.begin(), v.end());
                //nlohmann::json j_vec(c_vector);
                std::cerr << "std::vector<VariantType_t>>" << std::endl;
            }
            // FUNDAMENTAL TYPES
            else {
                // UINT
                if constexpr (std::is_same_v<T, uint8_t>) {
                    NULL;
                }
                else if constexpr (std::is_same_v<T, uint16_t>) {
                    std::cerr << "uint16_t" << std::endl;
                }
                else if constexpr (std::is_same_v<T, uint32_t>) {
                    std::cerr << "uint32_t" << std::endl;
                }
                else if constexpr (std::is_same_v<T, uint64_t>) {
                    std::cerr << "uint64_t" << std::endl;
                }
                // INT
                else if constexpr (std::is_same_v<T, int8_t>) {
                    std::cerr << "int8_t" << std::endl;
                }
                else if constexpr (std::is_same_v<T, int16_t>) {
                    std::cerr << "int16_t" << std::endl;
                }
                else if constexpr (std::is_same_v<T, int32_t>) {
                    std::cerr << "int32_t" << std::endl;
                }
                else if constexpr (std::is_same_v<T, int64_t>) {
                    std::cerr << "int64_t" << std::endl;
                }
                // FLOAT
                else if constexpr (std::is_same_v<T, _Float32>) {
                    std::cerr << "float" << std::endl;
                }
                // DOUBLE
                else if constexpr (std::is_same_v<T, _Float64>) {
                    std::cerr << "double" << std::endl;
                }
                // STD::STRING
                else if constexpr (std::is_same_v<T, std::string>) {
                    std::cerr << "std::string" << std::endl;
                }
                // BOOL
                else if constexpr (std::is_same_v<T, bool>) {
                    std::cerr << "bool" << std::endl;
                }
                // OOPS
                else
                    throw("TYPE NOT IMPLEMENTED");

                // Insert template value in json
                (*m_jReturn)[m_strName] = _val;
            }
        }
        std::string     m_strName { "" };
        nlohmann::json *m_jReturn { nullptr };
    };

private:
    nlohmann::json m_jReturn;
};

int main() {
    /*
    // MESSAGE
    // Declare
    int         iValA   { 123 },
                iValB   { -987 };
    float       fValA   { 1.234f },
                fValB   { -987.1f };
    std::string strValA { "Val A" },
                u32str  { u8"Бори́са"};
    struct Stest { int   m_i; float m_f; };
    Stest       sStruct { 5, 1.5f };

    // Populate struct
    SMessageData mapData;
    mapData.Add<int>("int1", iValA);
    mapData.Add<int>("int2", iValB);
    mapData.Add<float>("float1", fValA);
    mapData.Add<float>("float2", fValB);
    mapData.Add<std::string>("std::string1", strValA);
    mapData.Add<std::string>("std::string2", u32str);

    // Simulate sending buffer
    std::uint8_t *cBuffSend { new std::uint8_t[mapData.Length()] };
    ::memset(cBuffSend, 0, mapData.Length());
    ::memcpy(cBuffSend, mapData.ToCharArray(), mapData.Length());
    SK::Tools::CryptUncrypt(cBuffSend, mapData.Length());

    // Simulate receiving buffer
    int iLen { mapData.Length() };
    std::uint8_t *cBuffRecv { new std::uint8_t[iLen] };
    ::memcpy(cBuffRecv, cBuffSend, iLen);
    SK::Tools::CryptUncrypt(cBuffRecv, iLen);
    std::cerr << std::to_string(sData.m_i) << std::endl;

    //
    std::string strGet { mapData.Serialize() };

    return 0;
    */

    /*
    SMessageData mapData;

    uint8_t ui8Val { 125 };
    mapData.Add<uint8_t>("abc", 128);
    std::string str { "test" };
    mapData.Add<std::string>("123", "qzd");

    //std::string str { "foobar" };
    //mapData.Add("123", str);

    //std::string u32str { u8"Бори́са"};
    //mapData.Add("1", u32str);

    //std::map<uint16_t, std::variant<TYPEFORNETWORK>> qzd;
    //qzd.insert({ 0, 12345678 });
    //qzd.insert({ 1, "abcdef" });
    //mapData.Add("2", qzd);

    std::string strGet { mapData.Serialize() };

    std::cerr << "RETURN> "  << strGet << std::endl;
    return 0;

    struct sTest {
        std::uint32_t m_i    { 654 };
        std::uint8_t  m_c[5] { 'a', 'b', 'c', 'd', 'e' };
    };
    sTest sData;
    std::uint8_t *cBuff { new std::uint8_t[sizeof(sData)] };
    ::memset(cBuff, 0, sizeof(sData));
    ::memcpy(cBuff, &sData, sizeof(sData));
    SK::Tools::CryptUncrypt(cBuff, sizeof(sData));
    sData.m_i = 69;
    sData.m_c[0] = 69;
    sData.m_c[1] = 69;
    sData.m_c[2] = 69;
    sData.m_c[3] = 69;
    sData.m_c[4] = 69;
    SK::Tools::CryptUncrypt(cBuff, sizeof(sData));
    ::memcpy(&sData, cBuff, sizeof(sData));
    std::cerr << std::to_string(sData.m_i) << std::endl;
    std::cerr << std::to_string(sData.m_c[0]) << std::endl;
    std::cerr << std::to_string(sData.m_c[1]) << std::endl;
    std::cerr << std::to_string(sData.m_c[2]) << std::endl;
    std::cerr << std::to_string(sData.m_c[3]) << std::endl;
    std::cerr << std::to_string(sData.m_c[4]) << std::endl;
    return 0;
    */

    SK_WRITELOG(std::string(SK_FILENLINE), "NFO", "Starting Synak MS.", std::string("PID " + std::to_string(::getpid())), std::string("BUILD " + SK_BUILDTIMESTAMP));
    SK::MasterServer::m_LW_bLogTruncate = false;

    // Network Layer initialization
    SK::SynakManager mngr_nl;
    mngr_nl.initialization();

    // Master Server initialization
    SK::MasterServer mngr_ms;
    mngr_ms.initialization();
    mngr_ms.WP_watcherTerminal_Launch();      // Optional
    mngr_ms.WP_watcherWebPanel_Launch(45318); // Optional

    while (mngr_ms.m_bRun);

    mngr_ms.desinitialization();
    mngr_nl.desinitialization();

    SK_WRITELOG(SK_FILENLINE, "NFO", "Stopping Synak MS.");

    return 0;
}
