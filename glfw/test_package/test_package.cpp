#include <cstdlib>
#include <GLFW/glfw3.h>

int main (int argc, char * argv[]) {
	GLFWwindow* window;
    GLFWmonitor* monitor = NULL;

    monitor = glfwGetPrimaryMonitor();

    window = glfwCreateWindow(640, 480, "Window name", monitor, NULL);

    glfwDestroyWindow(window);
    glfwTerminate();
    return EXIT_SUCCESS;
}
