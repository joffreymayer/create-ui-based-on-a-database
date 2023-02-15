# Load all the libraries you need to update your dataset with the newest emails
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import re # I need this package to filter particular text-patterns in my emails. --> Note: it is already built-in!
from datetime import datetime # I need this package to give the updated(!) dataset a good name, e.g. with to "today's" date in it
import pandas as pd

def update_df():
    ### Step 1: Load the existing file that I need (= 'jobs-url.csv')
    testo = pd.read_csv(
        "../data/job-urls.csv" # Note: for the relative path to work, make sure that the "backend"-folder is the root of this project. If not, `cd` into it with your terminal OR you could use an absolut path...
    )

    ### Step 2: Set-Up our Email-Crawler (in order to scrape the latest emails)

    # account credentials
    username = "your_email@example_email.com" # <- THIS is where you should put your email-account. Obviously, I removed my email adress from this line, otherwise everyone could have copied it from there...
    password = "YOUR_PASSWORD_XYZ" # <- THIS is where you need to put your password for your email-account, otherwise you won't be able to log in.
    # use your email provider's IMAP server, you can look for your provider's IMAP server on Google
    # or check this page: https://www.systoolsgroup.com/imap/
    # for hotmail, it's this:
    imap_server = "imap-mail.outlook.com" # checkout this link for other email-servers: https://www.systoolsgroup.com/imap/

    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    ### Step 3: Establish a connection to the Email-Server:
    # !Important: you need an internet-connection to run the next pieces of code!!!

    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)

    ### Step 4: Get the NEWEST Emails from the server (= the ones I currently don't have in my dataset)

    status, messages = imap.select("Jobs") # select the email folder, we want to scrape (you probably will need to change this...)

    # To update our DF, we need to know how many additional emails came into our 'Jobs'-folder: 
    todays_date = datetime.now() # what is today's date?
    todays_date = pd.to_datetime(todays_date, infer_datetime_format=True, utc= None) # we need a 'datetime'-object
    latest_date_in_df = pd.to_datetime(testo.Date[0], utc = None, infer_datetime_format=True) # next, select the latest date from our current DDs (that we want to update)
    latest_date_in_df = latest_date_in_df.replace(tzinfo=None) # we need to remove the time-zone, otherwise we CANNOT calculate how many new days we need to scrape in our email...
    dates_to_scrape = todays_date - latest_date_in_df # the number of days we 
    N = int(str(dates_to_scrape).split()[0])# <-- THIS is Key to understand: with this, we get the correct UPDATED total of emails in my inbox! --> formula: "N" = "today's date" - "latest date in our dataset"
    print("To update our DF, we need to scrape {0} additional Mails".format(N))

    # "messages" will contain the total number of emails in the folder "Jobs"
    messages = int(messages[0])
    print("We see that we currently have {0} emails in the folder 'Jobs'".format(messages)) # check, if it worked? --> we see that we currently have 232 emails in the folder "Jobs"


    ### Step 5: # Now, read the Emails that I currently miss in my DF (update it)

    dict_for_df = dict() # this empty dictionary will be transformed into the final time series ds later...
    dates_array = [] # this will be my column "Date" in my later ds
    total_jobs_available_today_array = [] # will be my column "Total Jobs available Today" 
    new_jobs_today_array = [] # will be my column "New Jobs published Today"

    ### For 2nd DF:
    dict_for_df2 = dict()
    urls_array = [] # will be a list of lists (with an index of 5 --> this is KEY, because we need it to have the same length as the dates, since the dates will be our "observations"-unit in the DF2!)
    job_titles_array = [] # same as "urls_array"...
    companies_array = [] # same as "urls_array"...

    for i in range(messages, messages-N, -1): # Why do we do this weird "backward"-loop? --> we want to iterate from the top to the bottom 
        # Key: in order to go "forward in time" (starting in the distant past), we need to iterate by typing in the 
        # following parameters: `messages-N, messages+1` and leave out "-1"(!!) at the end as the 3rd // last argument...
        # Backwards would be: `range(messages, messages-N, -1)`
        # fetch the email message by ID
        print("Currently reading {0}-th Email...".format(i))
        res, msg = imap.fetch(str(i), "(RFC822)") # `RFC822` is a special format that we can use to fetch the emails from the server: https://www.rfc-editor.org/rfc/rfc822
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1]) # parse the bytes returned by the `fetch()`-method to a proper "Message"-object
                subject, encoding = decode_header(msg["Subject"])[0] # decode the "subject" of the email-address to human-readable Unicode.
                if isinstance(subject, bytes): # if the "subject" is from the data-type "bytes", decode to str
                    subject = subject.decode(encoding)
                From, encoding = decode_header(msg.get("From"))[0] # decode email-sender (= "From") of the email-address to human-readable Unicode.
                if isinstance(From, bytes): # if the sender (= "From") is from the data-type "bytes", decode to str
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                print(msg['Date'])
                todays_email_date = msg['Date']
                dates_array.append(todays_email_date) # append the dates to my empty array
                # if the email message is "multipart":  for instance, an email message can contain the "text/html"-content AND "text/plain"-parts, e.g. it has the HTML and(!) plain text versions of the message.
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                            lines = body.split('\n')
                            job_titles = []
                            companies = []
                            for line in lines:
                                if "https://www.jobs.ch/de/stellenangebote/detail/" in line:
                                    job_titles.append(lines[lines.index(line) - 2])
                                    companies.append(lines[lines.index(line) - 1])
                            matches_plural = re.findall(r".*neue Jobs.*", body)
                            matches_singular = re.findall(r".*neuer Job.*", body)
                            matches = matches_singular + matches_plural # concatenate the 2 lists into 1 (bigger) list
                            new_jobs_per_day = list(map(lambda string: int(string[0:2]), matches)) # take only the first element of each string (= which is the "number" - currently given as a `string` - that we are interested in, in order to calculate the total number of new open job position that opened "today")
                            total_new_jobs_today = sum(new_jobs_per_day)
                            urls = re.findall(r"https://www.jobs.ch/de/stellenangebote/detail/\S+", body)
                            currently_open_job_positions = len(urls)
                            total_jobs_available_today_array.append(currently_open_job_positions) 
                            new_jobs_today_array.append(total_new_jobs_today)
                            urls_array.append(urls)
                            job_titles_array.append(job_titles)
                            companies_array.append(companies)
                        except:
                            pass
                        if "attachment" in content_disposition: # vorher: `elif` (statt `if`!)
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                print("="*100)
    dict_for_df['Date'] = dates_array
    dict_for_df['Total of open Job-Positions up until today'] = total_jobs_available_today_array
    dict_for_df['New Jobs published Today'] = new_jobs_today_array

    ### 2nd DF:
    for (date, url, title, company) in zip(dates_array, urls_array,  job_titles_array, companies_array):
        dict_for_df2[date] = [url, title, company] # this will add new keys to the dictionary, where the 'dates' are the keys and a list (of sublists, containing the URLs, Job-Titles and Company-Names) as the values...

    
    ### Step 6: # create the 2nd DF --> for this, we need to create 3 separate DFs first...

    rows = []
    for key, values in dict_for_df2.items():
        for value in values:
            row = {key: value}
            rows.append(row)

    list_of_df = []
    for i in rows:
        df2 = pd.DataFrame(i)
        list_of_df.append(df2)

    # Problem in all the DFs? --> we have the Date as 1 column, instead of rows... --> Solution: transform the DF into "long-format"...
    print(list_of_df)
    test = list_of_df[1]
    test.stack().droplevel(level=0).to_frame().rename({0: 'Job Title'}, axis='columns') # Key: 'droplevel'-method, because I had an unnecessary multi-index...  

    url_series = pd.Series()
    # Transform all the DFs for the column 'URL':
    for i in list_of_df[0::3]: # Key: we start with the 1st list-element of 'list_of_df' and then only iterate over every 3rd elements
        url_series = pd.concat([url_series, i.stack().droplevel(level=0)])
        
    title_series = pd.Series()
    # Transform all the DFs for the column 'URL':
    for i in list_of_df[1::3]: # Key: we start with the 1st list-element of 'list_of_df' and then only iterate over every 3rd elements
        title_series = pd.concat([title_series, i.stack().droplevel(level=0)])
        
    company_series = pd.Series()
    # Transform all the DFs for the column 'URL':
    for i in list_of_df[2::3]: # Key: we start with the 1st list-element of 'list_of_df' and then only iterate over every 3rd elements
        company_series = pd.concat([company_series, i.stack().droplevel(level=0)])

    url_df = url_series.to_frame().rename({0: 'url'}, axis='columns').reset_index().rename({'index': 'Date'}, axis='columns')
    title_df = title_series.to_frame().rename({0: 'Job Title'}, axis='columns').reset_index().rename({'index': 'Date'}, axis='columns')
    company_df = company_series.to_frame().rename({0: 'Employer Company'}, axis='columns').reset_index().rename({'index': 'Date'}, axis='columns')

    url_df['Date'] = pd.to_datetime(url_df['Date'])
    title_df['Date'] = pd.to_datetime(title_df['Date'])
    company_df['Date'] = pd.to_datetime(company_df['Date'])

    ### Step 7:  Now, we can truly create our 2nd DF --> Prepare to merge Merging...
    noob = pd.merge(
        url_df,
        title_df,
        how="left",
        on=url_df.index, # Key: we merge via the Index, which are only numbers from 0-184 --> merging via index. Note that I needed to put the "Date" as a column (and NOT as an index!)
    ).drop(['key_0', 'Date_y'], axis = 1) # we only need one of the "Date"-Columns. Also, we can drop the automatically generated column "key_0", which is a leftover-column that gets generated, because we merged via the "index". 

    # second merge, since we need to combine 3 DFs into 1 "big" DF --> we currently only merged 2 (out of 3) DFs, that's why we need this 2nd merging...
    noob = pd.merge(
        noob,
        company_df,
        how="left",
        on=noob.index, # Key: Again, we merge via the Index, which are ALL our observations...
    ).drop(['key_0', 'Date_x'], axis = 1) # same as first merging: we drop one of the "Date"-Columns, as well as the automatically generated "index"-column (= 'key_0')... 

    df2 = noob.sort_values(by="Date", ascending = False)
    df2 = df2.reindex(columns=['Date', 'url', 'Job Title', 'Employer Company']) # change the order of columns: i want "date"-col to be the first one...

    df2['Job Title'] = [el.replace("\r", "") for el in df2['Job Title']] # we need to remove the "\r" behind all the elements of the col of "Job Title" & "Employer Company", otherwise saving the ds correctly will not be possible! xD
    df2['Employer Company'] = [el.replace("\r", "") for el in df2['Employer Company']] # same as above
    df2 = df2.reset_index().drop(['index'], axis = 1)

    df_update = df2.append(testo)

    ### Step 8: # Save the updated dataset
    today = datetime.now().strftime('%Y-%m-%d') # we need to convert it into a string (in order to do string concatenation)
    df_update.to_csv(f"../data/job-urls.csv", index=False)
    df_update = df_update.reset_index().drop(['index'], axis = 1) # we need to reset the index after we stacked the two 
    # DFs together --> if you don't do this, you CANNOT save it as a `.json`-object...
    df_update.to_json(f"../data/job-urls-{today}.json")

    ### Step 9: close the connection and logout from your email-account
    imap.close()
    imap.logout()

update_df()