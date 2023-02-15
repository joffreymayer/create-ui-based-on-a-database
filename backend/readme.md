# Backend of the Project

The goal of this sub-repo is:

- To **generate the initial database** of all the job openings for university graduates. This can be achieved by running the `0-generate-initial-dataset.ipynb` file.
- Furthermore, each day, we receive a new email with new data. Hence, we need to **update the database daily**. This can be done via the `1-update-dataset.ipynb` notebook.
- Last but not least, we need to **pre-render the UI**, because displaying the whole database in the UI would result in a HTML-file that is way too big in size. 

## In which order should you run the files?

All the files - except the "update.py" - are numbered, so this is the order in which someone, who wishes to reproduce the project, should run them.

## How to run a notebook?

In order to run a notebook - e.g. those files that end in `.ipynb` - you should activate your virtual environment (see the `readme.md` file in the root of this repo for a tutorial) and - in your terminal (while being in this project's working directoy) - run the command `jupyter notebook`. As a consequence, a new browser-window should open and you should be able to open the "backend"-subfolder and open any jupyter notebooks there. 

## Note when running `0-generate-initial-dataset.ipynb` and `1-update-dataset.ipynb`

- Those 2 notebooks will not run, unless you give it some valid email and its corresponding password. 
- Furthermore, the setup may differ, depending on which type of email you use (gmail, hotmail, bluewin etc...). In order to make the crawler work, you should use your email provider's IMAP-server. 
    - You can look for your provider's IMAP server on Google or check this page: https://www.systoolsgroup.com/imap/
- <ins>Very important</ins>: ___Last but not least, it is to note that I used the crawler to collect information on a job-newsletter that I collected over the course of 1 year, on a daily basis. This means that - if you want to start running a similar project like this one - you will need to setup a newsletter from one of your favorite job-portals, in order for them to send you standardized emails that you can then collect and crawl. Otherwise, the project is not reproducible, since you cannot crawl your own email, if you don't have the exact same newsletter saved on your email-server!___
    - <ins>Short term solution</ins>: You can play around with my job-dataset. I left it in the "data"-subfolder for all those that want to reproduce the UI with some data.

## What is the `2-pre-render-the-ui` folder?

After having constructed your dataset, you can use it to build a UI. However - from a webdeveloper standpoint - since **the dataset contains more than 10'000 job-ads**, it is <ins>not</ins> optimal to render all those ads into the UI, since this would cause alot of performance issues on the website (the HTML-file would be too big in size, resulting in a low loading-time). To get around this problem, **the fastest solution is to separate the site's built-time into 2 parts**: 

- <ins>Step 1</ins>: In the first part, we use the **JavaScript-DOM** ( "DOM" stands for 'document object model') to inject all our job-ads into the HTML-file. Next, we render everything ___locally___ into the browser, which should take some time (since we display all the 10'000 into the UI). 
    - <ins>Note</ins>: In the `2-pre-render-the-ui`-folder, there is a `index.html`-file that seems rather empty, when you open it. This is correct, because **this `index.html` file will be populated with HTML-code via the JavaScript-code, that I wrote in the `app_card.js` file**! Hence, if you open the `index.html` in your code editor _Visual Studio Code_ and use the "Live Server" extension to run the file locally on your browser, you will see that the HTML-file gets populated with all the job-ads that were in the database. Hence, the `index.html` in the 
- <ins>Step 2</ins>: In the second part, we can download the newly created HTML-file (see "Step 1") from the browser. What this special about this download, is that - in contrast to the `index.html` that you will find in the `2-pre-render-the-ui` folder - the HTML-file is now full of actual HTML-code (the other `index.html` is almost empty). The reason behind this, is that - while reading the `index.html` file during "step 1" - the browser automatically run the JavaScript code in the `app_cards.js` file, in which I instructed - via the JavaScript-DOM - to create all the HTML-markup when reading the database (we read the database in JavaScript in the `app_cards.js` file as `.json`). Now, with this fully populated `index.html` file, we can delete some of the codes that were automatically added after downloading the `index.html` via the browser, as well as adding some new code to it:

```
<div class="db-sect-1">
    <div class="db-sec-titles">
        <h2 class="h2-dashboard">Aktuell offene Stellen für Hochschulpraktikanten? 🎯</h2>
        <h3 class="h3-dashboard">Das Resultat</h3>
    </div>

    <div class="jobs-main-wrap">
        <!-- !!! HERE is where your HTML-code (generated from "step 1") should go !!! -->
    </div> <!-- End of "jobs-main-wrap" -->
</div> <!-- End of "db-sect-1" -->
```

___With the above code, we have our "Step 2" completed. The new `index.html` that results from this step should be the exact version that you see in the `fontend-ui` folder / the one you should see on my website (starting at the "Current Openings for University Graduates? 🎯" section). Next, you can head to the `frontend-ui` folder for some further instructions.___

Congratulations! You have understood the basics on how to build a UI based on a database! 😊

## What is the `update.py` file?

_The `update.py` is a python-script that is meant to be used via the terminal for the **daily updates** of the job-database. It was generated by putting all the code within the `1-update-dataset.ipynb` file together - as one big function. This function in `update.py` is called as soon as we run the script in the terminal. The output of the `update.py` - if it runs successfully - represents the updated version of our job-database (in a `.json` format) and will be shown in the "data"-subfolder._

Note that - similarly to the notebooks `0-generate-initial-dataset.ipynb` and `1-update-dataset.ipynb` - the `updated.py` script needs some valid email and its corresponding password!

