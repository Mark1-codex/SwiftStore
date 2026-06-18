#include <iostream>
#include <cstdlib>
#include <string>
#include <unistd.h>

int main() {
    char hostname[256] = {0};
    gethostname(hostname, sizeof(hostname));
    std::cout << "SwiftStore v1.1 terminal.\nType 'exit' or 'quit' to quit.\n\n";
    while (true) {
        std::string cmd;

        // Get current directory
        char cwd[1024] = {0};
        getcwd(cwd, sizeof(cwd));

        std::cout << "[" << std::getenv("USER") << "@" << hostname 
                  << " " << cwd << "]$ ";
        
        std::getline(std::cin, cmd);

        if (cmd == "exit" || cmd == "quit") break;
        if (cmd.empty()) continue;

        // Special handling for cd
        if (cmd.rfind("cd ", 0) == 0 || cmd == "cd") {
            std::string path = (cmd == "cd") ? std::getenv("HOME") : cmd.substr(3);
            if (chdir(path.c_str()) != 0) {
                std::cout << "cd: " << path << ": No such directory\n";
            }
        } 
        else {
            std::system(cmd.c_str());
        }
    }
    return 0;
}