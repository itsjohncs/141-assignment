#pragma once

#include <iostream>
#include <vector>

typedef int score_t;

typedef int action_t;
action_t const NONE = 0;
action_t const MATCH = 1;
action_t const DELETION = 2;
action_t const INSERTION = 3;

class SmithMatrix {
    /// The width of the matrix.
    unsigned width_;

    /// The height of the matrix.
    unsigned height_;

    /// The scores as fixed width integers (2.2 would be stored as 220)
    std::vector<score_t> scores_;

    std::vector<action_t> actions_;

public:
    SmithMatrix(unsigned width, unsigned height);

    void print(std::ostream & out = std::cout) const;

    inline unsigned width() const {
        return width_;
    }

    inline unsigned height() const {
        return height_;
    }

    inline action_t & action_at(unsigned i, unsigned j) {
        return actions_[j * width_ + i];
    }

    inline action_t const & action_at(unsigned i, unsigned j) const {
        return actions_[j * width_ + i];
    }

    inline score_t & score_at(unsigned i, unsigned j) {
        return scores_[j * width_ + i];
    }

    inline score_t const & score_at(unsigned i, unsigned j) const {
        return scores_[j * width_ + i];
    }
};
