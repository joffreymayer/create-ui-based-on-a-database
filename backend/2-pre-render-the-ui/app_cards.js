// Load the csv file
let today = '2023-02-14'
let url = '../../data/job-urls-' + today + '.json';
main_wrapper = document.querySelectorAll('.main-wrapper');
// console.log(main_wrapper)
let response = fetch(url)
    .then(response => response.json())
    .then(data => {
        // Get an array of keys
        var keys = Object.keys(data);
        //console.log(keys) // this is a list that stores all the keys.
        // Loop through the keys
        var date_list = Object.values(data[keys[0]]) // 'data[keys[0]]' is an Object --> the 'Object.values()' transforms it into an array --> It becomes iterable!
        var url_list = Object.values(data[keys[1]])
        var job_list = Object.values(data[keys[2]])
        var employer_list = Object.values(data[keys[3]])
        let all_values_list = date_list.map((x, i) => [x, url_list[i], job_list[i], employer_list[i]]); // this is the equivalent of the `.zip()` method in Python
        for (let tuple of all_values_list){ // "all_values_list" = list of arrays that each contain 4 elements; "tuples" = an array of 4 elements: [0: "2021-11-01 07:04:45+00:00", 1: "https://www.jobs.ch/de/stellenangebote/detail/xyz", 2:   "Internship - HR Recruiting", 3: "ISS Schweiz AG, Zürich-Altstetten"]

            // 1) Create the component of the Card:
            var div = document.createElement('div');
            div.className = 'jobs-item';
            var link = document.createElement('a');
            link.href = tuple[1]; // append the specific link to the "href"-attribute
            link.setAttribute('target', '_blank'); // I want the link to open up in the
            link.setAttribute('rel', 'noreferrer');
            var div_img_wrap = document.createElement('div');
            div_img_wrap.className = 'img-wrap';
            var img = document.createElement('img');
            img.setAttribute('alt', 'A random Job-Image')
            img.className = 'job-img';
            var div_transp = document.createElement('div');
            div_transp.className = 'transparency';
            var div_info_wrap = document.createElement('div');
            div_info_wrap.className = 'info-wrap';
            var p_job = document.createElement('p');
            p_job.className = 'job-title';
            p_job.innerHTML = tuple[2]; // let's get the Job-Title
            var div_job_infos = document.createElement('div');
            div_job_infos.className = 'job-infos';
            var div_employer = document.createElement('div');
            div_employer.className = 'employer-info';
            div_employer.innerHTML = tuple[3]; // let's get the Job's Employer-Information (& Location)
            var div_date = document.createElement('div');
            div_date.className = 'date-info';
            div_date.innerHTML = new Date(tuple[0]).toLocaleString('de-CH'); // let's get the Date that the Job was posted --> Additional problem here: when the `.json`-file loaded, the date was in "ms" (statt zB. 19.03.2023) --> that's why, I needed to use the `Date()` class and convert the dates into the Swiss-time format ("de-CH")...

            // 2) Put all the pieces of the Card together to make the "HTML-Skeletton":
            div.appendChild(link);
            link.appendChild(div_img_wrap); // !Achtung hier: We append to "link" (NOT to "div"!): we need to append to the <a>-element, since everything inside the card should redirect to the main when clicking on the card!!!
            div_img_wrap.appendChild(img);
            div_img_wrap.appendChild(div_transp);
            div_transp.appendChild(div_info_wrap);
            div_info_wrap.appendChild(p_job);
            link.appendChild(div_job_infos);
            div_job_infos.appendChild(div_employer);
            div_job_infos.appendChild(div_date);


            // 3) Lastly, we need to  add the "HTML-Skeleton" to the page, by appending the highest parent-div to the <body>:
            document.body.appendChild(div);
        };
    });