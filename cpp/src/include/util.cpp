#include <iostream>

const void eprint(const char* string)
{
    std::cout << string << std::endl;
}

const void eprint(const std::string string)
{
    std::cout << string << std::endl;
}
