#include "SmithMatrix.hpp"

#include <iostream>
#include <vector>

SmithMatrix::SmithMatrix(unsigned width, unsigned height) :
        width_(width), height_(height), scores_(width * height),
        actions_(width * height) {
    // Do nothing
}

std::string to_str(action_t action) {
    switch (action) {
        case NONE: return "NONE";
        case INSERTION: return "INSERTION";
        case DELETION: return "DELETION";
        case MATCH: return "MATCH";
    }
}

void SmithMatrix::print(std::ostream & out) const {
    for (unsigned i = 0; i < width(); ++i) {
        for (unsigned j = 0; j < height(); ++j) {
            out << "(" << score_at(i, j) << ", " << to_str(action_at(i, j))
                << ") ";
        }
        out << "\n";
    }
    out.flush();
}
