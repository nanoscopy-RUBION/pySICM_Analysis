# Installation Instructions


## Install Git (For group Member only!)

Download git for your operating system by following the instructions on this link:

https://git-scm.com/book/en/v2/Getting-Started-Installing-Git


## I. Creating Github account and Private Access Token (PAS) (For group Member only!)

Create your own github account on https://github.com. Write one of the group members an email so you can be added to the group account and have access to our private repositories. Generate a personal access token (PAT) on github so you can navigate to github repositories on your command line. Follow the following link:

https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

For Step 8 just click all the permissions. You get a random code in the end which you have to save! If you lose the code you have to make a new one, so save it properly!


## II. Install Python 3

Install Python by follow the instruction on this link for your operating system:

https://realpython.com/installing-python/


## III. Install virtualenv

In your command line type in the following command:

	python -m pip install --upgrade pip
  
This should upgrade your python packet manager pip. If you have the newest version already "Requirement already satisfied" should appear. Install the module virtualenv through this command:

	python -m pip install virtualenv
  
This makes it possible to generate virtual environments on python.


## IV. Clone Git Respository

Chose a folder where you want to install the analysis program. Direct to this folder in your command line with the following command:

	cd example/directory/Program
  
In this folder type in the following command to get clone the git repository of the program: (For group members only)

	git clone https://github.com/nanoscopy-RUBION/pySICM_Analysis.git
  
If you are an external user ask for the folder from one of the group members and copy it in your folder.
Direct to the pySICM_Analysis folder in your command line.


## V. Create virtual Python Environment

Create a virtual environment in this directory through the following command:

	python -m virtualenv venv
  
venv is the name of the environment which should be visible now as a folder in your directory. With the following command the virtual environment is activated:

	venv\Scripts\activate
  
The Script in venv/Scripts activates the virtual environment of your current command line. This command always has to be executed beforehand if you want to start the program.


## VI. Install dependencies for the program

Now the program dependencies can be installed with the following command:

	python -m pip install -r requirements.txt
  
(Note: This has to be done only once. It could be that while further developing the program new dependencies will be added later on, in this case this has to be done again.)


## VII. Start Program

Type in following command to start the program (be in the correct folder pySICM_Analysis and venv should be activated):

	python sicm_analyzer/main.py
  
The Program should start (this can take several seconds).


## Git pull of the newest version (For group members only!)

Go to the pySICM_Analysis folder in your command line and type:

	git pull
  
The program should be updated.

