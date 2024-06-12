#pragma once

#include <SFML/Graphics.hpp>
#include <cmath> 
#include <chrono>


inline std::string format_variables(const std::vector<std::pair<std::string, double>>& variables) {
	std::ostringstream oss;
	oss.precision(2);
	oss << std::fixed;
	for (const auto& [fst, snd] : variables) {
		oss << fst << ": " << snd << ", ";
	}
	const std::string result = oss.str();
	// Remove the last comma and space
	return result.substr(0, result.size() - 2);
}


inline void caption_frame_rate(sf::RenderWindow& window, const std::string& title, const int fps)
{
	std::ostringstream oss;
	oss << title << " " << fps << "fps \n";
	const std::string string_frame_rate = oss.str();
	window.setTitle(string_frame_rate);
}


template<typename T>
T round_to_nearest_n(const T value, const unsigned decimal_places) {
	const T multiplier = pow(10, decimal_places);
	return round(value * multiplier) / multiplier;
}


template<typename T>
std::string trim_decimal_to_string(const T number, const size_t precision, const bool round=true)
{
	if (round)
		number = round_to_nearest_n(number, precision);

	// Convert the double to a string with the specified precision
	std::string result = std::to_string(number);

	if (const size_t dot_position = result.find('.'); dot_position != std::string::npos)
	{
		// Check if there are enough characters after the dot
		if (result.length() - dot_position > precision + 1)
		{
			result = result.substr(0, dot_position + precision + 1);
		}
	}

	return result;
}


inline float dot(const sf::Vector2f& v1, const sf::Vector2f& v2)
{
	return v1.x * v2.x + v1.y * v2.y;
}


inline float length(const sf::Vector2f& v)
{
	return std::sqrt(dot(v, v));
}


inline constexpr float pi = 3.14159265358979323846264338327950f;


inline void normalize_angle(float& angle_radians)
{
	while (angle_radians < 0.f)
	{
		angle_radians += 2.f * pi;
	}
	while (angle_radians >= 2.f * pi)
	{
		angle_radians -= 2.f * pi;
	}
}