#pragma once

#include <chrono>

// A utility class for managing time frames, the GetDelta function updates the time so call it at set frequent intervals
class StopWatch
{
    std::chrono::high_resolution_clock::time_point start_time_;

public:
    // Constructor
    StopWatch() : start_time_(std::chrono::high_resolution_clock::now()) {}

    // Get the time elapsed since the last call to GetDelta
    double get_delta()
    {
        const auto current_time = std::chrono::high_resolution_clock::now();
        const auto delta = current_time - start_time_;
        start_time_ = current_time;
        return std::chrono::duration_cast<std::chrono::duration<double>>(delta).count();
    }
};
