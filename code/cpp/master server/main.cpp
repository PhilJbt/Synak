#include "synak.h"


int main() {
    std::cerr << "[START] " << SK_BUILDTIMESTAMP << std::endl;

    SynakManager mngr; 
    mngr.Launch();

    std::cerr << "[STOP] " << std::endl;

    return 0;
}