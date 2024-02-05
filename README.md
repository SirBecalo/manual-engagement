# Claps-All-Hands
For Automating all things All-Hands at Thndr.

This is a github repository for automating all things related to all hands.
*Read below for how to use*

Completed projects: 
Automation of the engagement graphs

TODO:
-automate pulling data directly from braze using their API, to get rid of downloading the csv's
-automate hero metrics
-make script versions for the new claps

### Engagement metrics
## how to create the engagement graphs

prerequisites: 
-you need to have alread downloaded the needed segment files from braze, one file for each day of the week. refer to braze handoff document for how.

-if doing the graphs for more than one week, be sure to not mix the files of weeks together. keep each week's csv's langages and files separate. (so ar sheets should not mix with en sheet, and the previous week's sheets must not mix with the current week's sheet.)

### Step One: Organize you files into folders 
1- create 3 folders on your laptop. name one "weeks_saudi", name the other "ar", the other "en".

2- inside the "ar" folder, drop the 5 files relating to the previous week's arabic campaigns.

3- inside the "en" folder, drop the 5 files relating to the previous week's english campaigns

4- inside the "weeks_saudi" folder, drop the files relating to the previous week's saudi campaigns.
- note: you will have less files when there are vacations


### Step Two: open the [github "ar" weeks folder](https://github.com/SirBecalo/Claps-All-Hands/tree/main/weeks). 

towards in the interface above, where it shows you folders and files, click on the file called All_engagment_graphs.py you can alternatively open it from this [link](All_engagment_graphs.py)

Step Two: the top of the text file should have a set of buttons to click, with labels such as "code" "blame" "raw" and more. towards the right you will find a pen icon. click it to start editing the file.

Step Three: you need to scroll down to the very bottom of the file. you will find 3 lists called "en_week_folders, "ar_week_folders", saudi_week_folders like this:
>en_week_folders = [
    "weeks/en/dec24",
    "weeks/en/dec31",
    "weeks/en/jan8",
    "weeks/en/jan14",
    "weeks/en/jan21"
    "weeks/en/jan28"
]

>ar_week_folders = [
    "weeks/ar/dec24",
    "weeks/ar/dec31",
    "weeks/ar/jan8",
    "weeks/ar/jan14",
    "weeks/ar/jan21"
    "weeks/ar/jan28"

]


>saudi_week_folders = [
    "weeks_saudi/jan8",
    "weeks_saudi/jan14",
    "weeks_saudi/jan21",
    "weeks_saudi/jan28",
]

