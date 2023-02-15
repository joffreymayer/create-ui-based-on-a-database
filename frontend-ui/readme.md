# Frontend of the Project 

The goal of this sub-repo is:

- To **build the UI with HTML, CSS and JavaScript**.

_If you are using Visual Studio Code as your code editor, you can open the `index.html` via in the "Live Server" extension and you should already see the final result / UI in your browser._

## HTML-Part

Assuming that you completed the `readme.md` in the "backend" subfolder, you should now have an `index.html` file with all the job-opening listed as separate HTML-components (= blocks of codes). 

Here, we will simply add some further boiler-code <ins>around</ins> the already existing HTML-code. Simply add the following HTML to your downloaded `index.html`:

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

Last but not least, we need to get rid of some job-ads. Over 10'000 job-ads visualized into our UI is way too much information for a user. **So let's just keep around the most recent past 5 days**. This should be more than enough job-ads for our UI (around 300-400 HTML-cards). So **simply manually delete the rest of the HTML code that contain information on jobs that are older than the last 5 days**!

Now, our `index.html` should have significantly decreased in size, which is what we wanted to achieve from the beginning (remember: the problem was that our HTML was very slow in loading the page, because of the sheer number of job-ads in our database...) 😁

## CSS-Part

Now that we have our full HTML, we can start styling it with CSS:

- Let's start by creating a `static-styles.css` file in the root of the `frontend-ui` foolder.
- Next, you need to add the following code inside your `index.html` file, in order to connect the HTML to our CSS (similarly as we `import` stuff in Python). Note that the below HTML-codesnipped should be placed <ins>inside</ins> the `<head> ... </head>` part of the HTML-file:

```
<link rel="stylesheet" href="/frontend-ui/static-styles.css">
```

Finally, we can start to style the document as we want. I recommend you to simply copy the CSS that is in the `static-styles.css` inside `frontend-ui` folder on my Github.

## JavaScript-Part

- Let's start by creating a `app.js` file in the root of the `frontend-ui` foolder.
- Next, you need to add the following code inside your `index.html` file, in order to connect the HTML to our JavaScript (the same as we did for the CSS already). Again, note that the below HTML-codesnipped should be placed <ins>inside</ins> the `<head> ... </head>` part of the HTML-file:

```
<script src="/frontend-ui/app.js" defer></script>
```

Now, we can start adding some basic functionality to our UI:

As you have probably noted, we have the jobs displayed into our UI, but there are no images yet... Since it would be humanly impossible to add an `<img>` with a corrsponding source to an actual image, I went onto the following website:

https://unsplash.com/de

There, you can download beautiful images for free and you can use them in your projects, without worrying about copy-right issues. I choose 8 pictures, put them into an "img"-subfolder inside the "frontend-ui"-folder and wrote some JavaScript code inside the `app.js` which will randomly allocate one of these 8 pictures to one of the job-ads.

Finally, in order to make our UI feel more "smooth", we can implement an animation technique, which will make the cards magically appear once they enter the screen. I also wrote some JavaScript-Code for this in the `app.js`.

Congratulation! You have now build the frontend to visualize the database! 🤩