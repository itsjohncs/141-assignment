#include "similarity.hpp"

#include <iostream>

int main(int argc, char * * argv) {
    std::string a, b;

    std::getline(std::cin, a);
    a.resize(a.size() - 1);

    std::getline(std::cin, b);
    b.resize(b.size() - 1);

    similarity_score(a, b);

    return 0;
}
