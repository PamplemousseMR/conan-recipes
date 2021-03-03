#include <OGRE/OgreRoot.h>
#include <OGRE/OgreSingleton.h>
#include <OGRE/OgrePlugin.h>

#include <iostream>

int main (int argc, char * argv[]) {

	const std::string configPath = "bin\\plugins.cfg";

    ::Ogre::Root* root = OGRE_NEW::Ogre::Root(configPath);
    const ::Ogre::RenderSystemList& rsList = root->getAvailableRenderers();

	std::cout << "Render system : " << std::endl;
    std::for_each(rsList.begin(), rsList.end(), [&](const ::Ogre::RenderSystem* const _renderSystem)
    {
        std::cout << "\tRender found : " << _renderSystem->getName() << std::endl;
    });

    ::Ogre::Root::PluginInstanceList plList = root->getInstalledPlugins();

    std::cout << "Plugins : " << std::endl;
    std::for_each(plList.begin(), plList.end(), [&](const ::Ogre::Plugin* const _plugin)
    {
        std::cout << "\tPlugin found : " << _plugin->getName() << std::endl;
    });
    return EXIT_SUCCESS;
}
