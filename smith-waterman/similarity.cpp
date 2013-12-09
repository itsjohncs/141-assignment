#include "SmithMatrix.hpp"

#include "primitives.hpp"

#include <iostream>
#include <stdexcept>

unsigned symbol_to_index(char symbol) {
    switch (symbol) {
        case 'A': return 0;
        case 'G': return 1;
        case 'C': return 2;
        case 'T': return 3;
        default:
            throw std::runtime_error("Invalid symbol.");
    }
}

score_t sub_score(char a, char b) throw() {
    // The substituion scores as fixed with integers (.2 is encoded as 20)
    static score_t SUB_MATRIX[] = {
        100, -10, -10, -15,
        -10, 100, -15, -10,
        -10, -15, 100, -10,
        -15, -10, -10, 100
    };

    return SUB_MATRIX[symbol_to_index(a) * 4 + symbol_to_index(b)];
}

score_t gap_score(unsigned length) throw() {
    if (length == 1) {
        return 20;
    } else {
        return 5;
    }
}

// Returns a relative position (i, j) that corresponds to the direction to
// move per this action (see the wikipedia article for more info).
RelativePoint find_direction(action_t action) throw() {
    switch (action) {
        case NONE: return RelativePoint::create(0, 0);
        case MATCH: return RelativePoint::create(-1, -1);
        case DELETION: return RelativePoint::create(-1, 0);
        case INSERTION: return RelativePoint::create(0, -1);
    }
}

/// Determine the length of the gap starting at (i, j) in matrix.
unsigned find_gap_length(SmithMatrix const & matrix, unsigned i, unsigned j) {
    action_t start_action = matrix.action_at(i, j);
    if (start_action != DELETION && start_action != INSERTION) {
        return 0;
    }

    unsigned result = 0;
    while (matrix.action_at(i, j) == start_action) {
        RelativePoint dp = find_direction(matrix.action_at(i, j));
        i += dp.dx;
        j += dp.dy;

        result += 1;
    }

    return result;
}

unsigned string_gap_length(std::string const & a, unsigned start) {
    int i = start;
    for (; i >= 0 && a[i] == '_'; --i);
    return start - i;
}

void similarity_score(std::string const & a, std::string const & b,
        std::ostream & out) {
    // Create our matrix
    SmithMatrix matrix(a.size() + 1, b.size() + 1);

    // There's no need to zero our left and top borders because the entire
    // matrix is zeroed to begin with.

    // As we build the matrix we're going to keep track of what the largest
    // value is
    Point largest_cell = {0, 0};

    // Iterate through the matrix top-down left-to-right and fill in the values.
    // Make sure to skip the zeroed borders
    for (unsigned i = 1; i < matrix.width(); ++i) {
        for (unsigned j = 1; j < matrix.height(); ++j) {
            // The score if we leave things be and match up these two symbols.
            // Note that when accessing the original strings we have to be
            // careful since we added zeroed borders
            score_t match_score = matrix.score_at(i - 1, j - 1) +
                sub_score(a[i - 1], b[j - 1]);

            // The score if we add a gap to b here (deletion)
            score_t deletion_score = matrix.score_at(i - 1, j) -
                gap_score(1 + find_gap_length(matrix, i - 1, j));

            // The score if we add a gap to a here (insertion)
            score_t insertion_score = matrix.score_at(i, j - 1) -
                gap_score(1 + find_gap_length(matrix, i, j - 1));

            // Figure out which of the choices is greater (NONE, MATCH,
            // DELETION, or INSERTION).
            score_t max_score = 0;
            score_t max_action = NONE;
            if (match_score > max_score) {
                max_score = match_score;
                max_action = MATCH;
            }
            if (deletion_score > max_score) {
                max_score = deletion_score;
                max_action = DELETION;
            }
            if (insertion_score > max_score) {
                max_score = insertion_score;
                max_action = INSERTION;
            }

            matrix.score_at(i, j) = max_score;
            matrix.action_at(i, j) = max_action;

            // Update what the largest cell is if necessary.
            if (max_score > matrix.score_at(largest_cell.x, largest_cell.y)) {
                largest_cell.x = i;
                largest_cell.y = j;
            }
        }
    }

    // matrix.print();

    // Move through the matrix backwards and determine our path (the blue
    // arrows in the wikipedia article are visualizing this step)
    std::vector<Point> path;
    path.reserve(b.size() * 2);
    Point cur_point = largest_cell;
    while (matrix.action_at(cur_point.x, cur_point.y) != NONE) {
        path.push_back(cur_point);

        RelativePoint p = find_direction(
            matrix.action_at(cur_point.x, cur_point.y));
        cur_point.x += p.dx;
        cur_point.y += p.dy;
    }

    // Construct the alignments by walking through our path backwards.
    std::string aligned_a;
    aligned_a.reserve(a.size() + a.size() / 2);
    std::string aligned_b;
    aligned_b.reserve(b.size() + b.size() / 2);
    for (int i = path.size() - 1; i >= 0; --i) {
        action_t const & cell_action = matrix.action_at(path[i].x, path[i].y);

        // Contruct the two alignments per wikipedia's description. Figuring
        // out which string to add a gap to after an INSERTION vs DELETION was
        // figured out through trying both. Hard to keep it all in my head.
        if (cell_action == MATCH) {
            aligned_a.push_back(a[path[i].x - 1]);
            aligned_b.push_back(b[path[i].y - 1]);
        } else if (cell_action == INSERTION) {
            aligned_a.push_back('_');
            aligned_b.push_back(b[path[i].y - 1]);
        } else if (cell_action == DELETION) {
            aligned_a.push_back(a[path[i].x - 1]);
            aligned_b.push_back('_');
        }
    }

    // Calculate the final score
    score_t final_score = 0;
    for (unsigned i = 0; i < aligned_a.size(); ++i) {
        if (aligned_a[i] == '_') {
            final_score -= gap_score(string_gap_length(aligned_a, i));
        } else if (aligned_b[i] == '_') {
            final_score -= gap_score(string_gap_length(aligned_b, i));
        } else {
            final_score += sub_score(aligned_a[i], aligned_b[i]);
        }
    }

    out << final_score << '\n';
    out << aligned_a << '\n';
    out << aligned_b << '\n';
    out.flush();
}
