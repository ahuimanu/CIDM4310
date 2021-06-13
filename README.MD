# CIDM 4310 Repo

## Summer 2021

### Book: Hands-On Data Analysis with Pandas - Second Edition

### Git

__Initialize__

Create a new repo

`git init`

__Git Ignore__

Do not track instructions

__Git Add__

Adds files for tracking

`git add -A`

__Git Commit__

Commit recent tracked changes

`git commit -m 'commit message'`

__Set up Remote__

Set up a remote peer (like Github)

`git remote add origin https://github.com/account/reponame.git`

__Push to remote__

Push your recent commit to the remote peet (e.g. Github)

`git push -u origin master`

## Markdown

[Jupyter Notebook-oriented Markdown Guide](https://medium.com/analytics-vidhya/the-ultimate-markdown-guide-for-jupyter-notebook-d5e5abf728fd)

## Setups Steps for Virtual Environment and Jupyter Notebook Use

1. Make virutal environment: `python -m venv ch03_env`
2. Activate virtual environment: `venv\Scripts\activate` (assumes you are on Windows and using PowerShell)
3. install necessary requirements using the requirements.txt file from the book: `pip install -r requirements.txt`
4. Run Jupyter Lab: `jupyter lab`