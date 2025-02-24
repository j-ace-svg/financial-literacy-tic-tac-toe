# Installation instructions
## Setting up python
In order to develop or run the game, you need to install python as well as pygame-ce. This can be done using the `flake.nix` file provided, or using the following pip command:
```
pip install pygame-ce
```

Please note that the game is tested with pygame-ce but not pygame, so if you choose to install pygame instead it may or may not run properly.

## Downloading the game
You can download from github by selecting the green `Code` button, and then download zip. To extract the zip on Windows, right click the zip in File Explorer and select `Extract All`.

## Running the game
After extracting the project in File Explorer, open the extracted folder. Then, press <kbd>⇧ Shift</kbd> + <kbd>Right click</kbd> in any empty space and select `Open command window here` or `Open PowerShell window here`.

In the Powershell or Command Prompt window, type `python main.py` and then press <kbd>Enter</kbd>, and the program should launch. Pay attention to the warning that is displayed in the console, which I also reproduce here:

> HEY!!! You!
> <br><br>
> Yeah, you running the program.
> <br><br>
> This program is designed to use Pygame-CE (Pygame Community Edition), not regular Pygame. They're very similar, but there might be some slight differences, and I only test this on Pygame-CE.
> <br><br>
> So, if you get an error that seems weird (or, if you aren't familiar with python, any error), MAKE SURE YOU'RE USING PYGAME-CE.
> <br><br>
> You can install pygame-ce the same way you installed pygame (if you weren't the person who installed pygame on this computer, talk to them). If you used pip, then you would run `pip uninstall pygame` and then `pip install pygame-ce`.
> <br><br>
> Thank you for your time, and have fun running the program.
