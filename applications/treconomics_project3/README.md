#Treconomics3: Return of the Snippet

Treconomics3 is a web application that harnesses the power of A/B testing 
to evaluate whether snippet length in search engine result pages (SERPs) has 
any significant effect on user behaviour or performance.
It heavily builds on previous applications developed by Leif Azzopardi and David Maxwell.

## Installation

These are the initial steps you required before you can run the application on your machine.

### Prerequisites
`Python 2.7`, `pip` package manager, `virtualenv` or `pyenv`, `git`
Clone the repository to a preferred location
```
git clone https://github.com/leifos/ifind/
```

### Dependencies
Navigate to the `treconomics_project3` folder
Run the `requirements.txt` file which will download and install all dependencies.
```
pip install -r requirements.txt
```

### Database population
Create a database with the predefined models (old synchronize)
```
python manage.py migrate
```

Use the `populate_treconomics_db.py` to add data
```
python populate_treconomics_db.py
```

This will create test accounts with the following format
```
username: testX
password: X
```
where X is a number between 1-23

### Importing `ifind`
Finally you will need to add `ifind` to your `PYTHONPATH`
which you can do by insert the following line at the bottom of your `.bashrc`

```
export PYTHONPATH=/Users/mickeypash/ifind/:/Users/mickeypash/ifind/applications/slowsearch_project:$PYTHONPATH
```

### Downloading the NLTK corpus
```
python -c "import nltk; nltk.download()"
```
A GUI window should pop-up with download options.
Alternatively you will see a CLI which will require you to specify and option.
Type `d` for Download and then `book` to download the book corpus (that is all you need).
You could also select  `all` and install the whole corpus (this will take a few minutes).

The files will be installed in 
 + `/Users/<username>/nltk_data` (Mac)
 + `/usr/share/nltk_data` (Unix)
 + `C:\nltk_data` (Windows)

## Deployment

In order to run the application
```
python manage.py runserver
```

Simply navigate to [http://localhost:8000](http://localhost:8000)
