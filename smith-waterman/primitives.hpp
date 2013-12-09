#pragma once

struct Point {
    unsigned x;
    unsigned y;

    inline static Point create(unsigned x, unsigned y) {
        Point p = {x, y};
        return p;
    }
};

struct RelativePoint {
    int dx;
    int dy;

    inline static RelativePoint create(int dx, int dy) {
        RelativePoint p = {dx, dy};
        return p;
    }
};
