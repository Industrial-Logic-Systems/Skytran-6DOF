# HOW TO USE

### CONVERT THE PROFILES:
1. Run the python file `convert.py`
2. Select the profile you wish to convert
3. If there are any errors follow the directions to shift the whole profile. It is recommended to shift in amount of ~10mm at a time.
4. Save the converted profile

# RUN THE PROFILES:
1. Double click "Skytan_6DOF.exe"
2. Chose the profile to run.
3. After a couple of seconds the platform will do the sequence of moves and will close when completed.


# Build the C++ From Scratch:

You need 3 peices of software:
1. CMake - https://cmake.org/download/
2. Clang Compiler - https://github.com/llvm/llvm-project/releases/tag/llvmorg-14.0.1 - LLVM-14.0.1-win64.exe is the installer for windows
3. Ninja Build - https://github.com/ninja-build/ninja/releases/tag/v1.10.2 - ninja-win.zip is the file for windows

CMake and Clang will both prompt you to add them to the System Path when installing, Select yes
For ninja build you will need to but it in a folder alreay in the System Path Variable, or add it yourself.

Once you have those installed you can now build the software

### Commands to build
``` bash
mkdir build
cd build
cmake -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=Release .. -G Ninja
cmake --build .
```
If done properly then the build directory will contain `Skytran_6DOF.exe` which is the compiled code.
