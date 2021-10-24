#include <cstdlib>
#include <iostream>

#include "pugixml.hpp"

int main() {
    pugi::xml_document doc;
    pugi::xml_parse_result result = doc.load_file("example.xml");
    if (!result) {
        std::cerr << "Could not load file example.xml" << std::endl;
        return EXIT_FAILURE;
    }

    pugi::xml_node node = doc.child("conan").child("package");
    if (!node) {
        std::cerr << "Could not load node conan" << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << node.attribute("category").name() << ": " << node.attribute("category").value() << std::endl;
    std::cout << node.child("name").name() << ": " << node.child("name").text().as_string() << std::endl;
    std::cout << node.child("author").name() << ": " << node.child("author").text().as_string() << std::endl;
    std::cout << node.child("language").name() << ": " << node.child("language").text().as_string() << std::endl;

    return EXIT_SUCCESS;
}