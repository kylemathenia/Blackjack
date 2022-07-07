#include <iostream>

void
extra(int a)
{
    for (int i=0;i<a;i++)
    {
        std::cout << "Testing" << std::endl;
    }
}

int main()
{   
    extra(3);
    std::cout << "Hello World" << std::endl;
    std::cin.get();
}