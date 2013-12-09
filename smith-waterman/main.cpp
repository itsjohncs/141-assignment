#include "similarity.hpp"

#include <iostream>

int main(int argc, char * * argv) {
    while (std::cin) {
        std::string a, b;

        std::getline(std::cin, a);
        if (a.empty()) break;
        a.resize(a.size() - 1);

        std::getline(std::cin, b);
        if (b.empty()) break;
        b.resize(b.size() - 1);

        similarity_score(a, b);
    }

    return 0;
}
