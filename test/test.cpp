#include <SFML/Window.hpp>

int main()
{
    sf::ContextSettings contextSettings;
    contextSettings.depthBits = 24;
    sf::Window window(sf::VideoMode(640, 480), "SFML window with OpenGL", sf::Style::Default, contextSettings);
}
