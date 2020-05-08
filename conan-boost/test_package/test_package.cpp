#include <cstdlib>
#include <boost/smart_ptr/shared_ptr.hpp>

int main (int argc, char * argv[])
{
    ::boost::shared_ptr<int> p1{new int{1}};
    ::boost::shared_ptr<int> p2{p1};

    if(*p1 != *p2)
    {
      return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
