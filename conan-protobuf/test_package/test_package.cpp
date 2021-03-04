#include <cstdlib>
#include <iostream>

#include "addressbook.pb.h"

int main()
{
   std::cout << "Pamplemousse\n";

   tutorial::Person p;
   p.set_id(21);
   p.set_name("pamplemousse");
   p.set_email("info@pamplemousse.com");

   std::cout << p.SerializeAsString() << "\n";
   return EXIT_SUCCESS;
}