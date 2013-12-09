#include "similarity.hpp"

#include <iostream>

int main(int argc, char * * argv) {
    std::string a, b;

    std::getline(std::cin, a);
    std::getline(std::cin, b);

    similarity_score(a, b);

    return 0;
}
