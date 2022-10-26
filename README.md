# Robotics at Iowa Rover Code
### Getting started:

First navigate to where you want to download the code and run the following command in the terminal
```
$ git clone https://github.com/roboticsatiowa/UIRobotics2022.git
```
All necessary dependencies are listed below with instructions to install them

### Running the code:

on the laptop (base station) navigate to UIRovotics/src/
Then run the following command
```
python3 start_GUI.py
```

then on the rover run
```
python3 start_rover.py
```

### dependencies:
- Install [PyGame](https://github.com/pygame/pygame) package: `pip3 install pygame`

__________________________________________________________________________________________________________________________________________________________

### Terminal Commands:
- ls – list all files in current directory 
- cd - change directory 
  - cd dir1/dir2/dir3/etc to navigate forward through multiple directories 
  - cd .. /../etc to go backwards through directories 
  - cd takes you to home directory 
- mkdir -  
- sudo (command) - run administrator commands 
- whatis (command) - find function of different command 
- exit() - exit python to get back to (base) 

### Git Commands:
- git diff – check for differences 
- git pull – pull upstream changes and update your local repository 
- git push – push changes from your local repository to remote repository 
- git checkout  
  - -b  <name of branch> – make new branch 
  - <name of branch> - switch to <name> branch 
- git status – check which files have been changed 
- git add <file/folder name> - stage a file for commit 
- git commit -m “COMMENT” - commit changes to branch 
  - -a -m “COMMENT” - commit all changes 
  
### Extra resources: 
- https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html  
- https://www.techrepublic.com/article/16-terminal-commands-every-user-should-know/  

### Launching rover and base station 
- Connect antennas 
- ssh into Jetson 
```
  >>> ssh robotics@192.168.1.23
```
- Run rover launch file 
```
  >>> ./ launch_rover.sh.sh 
```
- Open base station terminal 
- Run base station launch file 
```
  >>> ./ launch_base.sh 
```
- Rover running :) 
