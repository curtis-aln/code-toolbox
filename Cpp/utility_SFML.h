#pragma once

#include <SFMl/Graphics.hpp>

inline void draw_rect_outline(sf::Vector2f top_left, sf::Vector2f bottom_right, sf::RenderWindow& window, const sf::RenderStates& render_states = sf::RenderStates())
{
	sf::VertexArray lines(sf::Lines, 8);

	// Top line
	lines[0].position = top_left;
	lines[1].position = { bottom_right.x, top_left.y };

	// bottom line
	lines[2].position = bottom_right;
	lines[3].position = { top_left.x, bottom_right.y };

	// right line
	lines[4].position = bottom_right;
	lines[5].position = { bottom_right.x, top_left.y };

	// Left line
	lines[6].position = top_left;
	lines[7].position = { top_left.x, bottom_right.y };

	window.draw(lines, render_states);
}


inline void draw_rect_outline(const sf::Rect<float>& rect, sf::RenderWindow& window, const sf::RenderStates& render_states = sf::RenderStates())
{
	draw_rect_outline({ rect.left, rect.top }, { rect.left + rect.width, rect.top + rect.height }, window, render_states);
}


inline sf::VertexArray make_line(const sf::Vector2f& start_position, const sf::Vector2f& end_position, const sf::Color color = sf::Color::White)
{
	sf::VertexArray line(sf::Lines, 2);
	line[0] = { start_position, color };
	line[1] = { end_position, color };
	return line;
}

inline sf::Vector2u clip_to_grid(const sf::Vector2u position, const sf::Vector2u tile_size)
{
	const sf::Vector2u index(position.x / tile_size.x, position.y / tile_size.y);
	return { index.x * tile_size.x, index.y * tile_size.y };
}


inline float dist_squared(const sf::Vector2f position_a, const sf::Vector2f position_b)
{
	const sf::Vector2f delta = position_b - position_a;
	return delta.x * delta.x + delta.y * delta.y;
}

inline sf::Rect<float> resize_rect(const sf::Rect<float>& rect, const sf::Vector2f resize)
{
	return {
		rect.left + resize.x,
		rect.top + resize.y,
		rect.width - resize.x * 2.f,
		rect.height - resize.y * 2.f
	};
}


inline sf::Rect<float> convert_coordinates(const sf::Vector2f& v1, const sf::Vector2f& v2) {
	const float x = std::min(v1.x, v2.x);
	const float y = std::min(v1.y, v2.y);
	const float width = std::abs(v1.x - v2.x);
	const float height = std::abs(v1.y - v2.y);

	return { x, y, width, height };
}


inline sf::VertexArray create_triangle(const float center_x, const float center_y,
	const float orientation, const float width, const float height)
{
	sf::VertexArray triangle(sf::Triangles, 3);

	// Calculate the vertices of the triangle based on the parameters
	const sf::Vector2f p1(center_x - width / 2, center_y + height / 2);
	const sf::Vector2f p2(center_x + width / 2, center_y + height / 2);
	const sf::Vector2f p3(center_x, center_y - height / 2);

	// Rotate the vertices based on the orientation
	const float cos_theta = std::cos(orientation);
	const float sin_theta = std::sin(orientation);

	triangle[0].position = {
		cos_theta * (p1.x - center_x) - sin_theta * (p1.y - center_y) + center_x,
		sin_theta * (p1.x - center_x) + cos_theta * (p1.y - center_y) + center_y
	};

	triangle[1].position = {
		cos_theta * (p2.x - center_x) - sin_theta * (p2.y - center_y) + center_x,
		sin_theta * (p2.x - center_x) + cos_theta * (p2.y - center_y) + center_y
	};

	triangle[2].position = {
		cos_theta * (p3.x - center_x) - sin_theta * (p3.y - center_y) + center_x,
		sin_theta * (p3.x - center_x) + cos_theta * (p3.y - center_y) + center_y
	};

	return triangle;
}


inline void rotate_triangle(sf::VertexArray& triangle, const float angle_radians)
{
	const sf::Vector2f pivot = (triangle[0].position + triangle[1].position + triangle[2].position) / 3.0f;

	for (size_t i = 0; i < 3; ++i)
	{
		const sf::Vector2f new_pos = triangle[i].position - pivot;
		const float x = new_pos.x * cos(angle_radians) - new_pos.y * sin(angle_radians);
		const float y = new_pos.x * sin(angle_radians) + new_pos.y * cos(angle_radians);
		triangle[i].position = sf::Vector2f(x, y) + pivot;
	}
}