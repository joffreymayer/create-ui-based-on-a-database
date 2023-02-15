# Email Scraping

The goal of this repository, will be to:

- **Create an email-scraper** in Python,
- Use the scraper to **extract any kinds of job-data from my email newsletter and store it in a database**,
- **Use the database to create a UI with JavaScript** in order to make a comprehensive visualization for any non-coder.

_The tutorial for this repository was inspired by this article: https://www.thepythoncode.com/article/reading-emails-in-python_

## How is this Repo organized? 🧐

If you want to reproduce the whole repo, this would be the order on how to tackle this project:

1) First, you need to open the "backend"-folder. There, you will find another `readme.md` to describe how you need to procede.
    - <ins>For the context</ins>: _The backend-folder's purpose is to **build the database** via email-scraping and process the raw email-data with NLP._
2) Next in line is the "frontend-ui"-folder. Once again, there is a `readme.md` for the instructions on how to procede.
    - <ins>For the context</ins>: _The frontend-folder's purpose is to **build the UI** via JavaScript, HTML and CSS._

___If you are only here for the results, open the "frontend-ui"-folder. Next, open the `index.html` in a code editor - for example Visual Studio Code - and run the "Live Server"-extension. "Live Server" will open a new browser-window and you will be able to see the UI.___

## Before you get started: Create a Virtual Environment (`venv`)

I will create a virtual environment for this project and work form there:

1) In your terminal, type in the following (make sure that you are inside your `wd`!): `python3 -m venv Your_Env_Name`. This will create the virtual-environment.
2) Next, you need to **activate this environment**: 
    - If you use your Mac: `source Your_Env_Name/bin/activate`.
    - If you are on a **Windows**-Computer: `Your_Env_Name\Scripts\activate.bat`
3) Check if it worked: `python --version`

That's it for the installation of the virtual environment!

### Update `pip`

Before I start with the project, I will make sure that my `pip`-installer is up-to-date. **I am currently using the version `22.2.2` for this project**.

- To check your current version of `pip`, simply type: `pip --version`.
- In order to upgrade `pip`, use the following command: `pip install --upgrade pip`

> Why should `pip` be up-to-date?: 

*If you’re using an old version of pip, installing the latest version of a Python package might fail—or install in a slower, more complex way*. 

### Install the packages

Now you can install the package:

1) `pip install jupyter`
    - For the **exact** Version I used, run the following command instead: `pip install jupyter==1.0.0`
2) `pip install re`
    - I need this package to filter particular text-patterns in my emails.
3) `pip install pandas`
    - I need this package to save the database as a `.csv` for further processing.

## References

- Offical Docs of `imaplib` module: https://docs.python.org/3/library/imaplib.html