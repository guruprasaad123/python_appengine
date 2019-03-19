# Caselets-search-app

This app is more like minized version of custom google web search based on the Dataset . Support by google's 

[app engine](https://cloud.google.com/appengine/)

Requirements :

- Google-app-engine 

- python 2.7

- React.js ( 16.x)

This app is built with Materialize-UI on the front end and python 2.7 on the backend .

## Running Locally :

### Installation:

For the front-end that is [Materialize-UI](https://material-ui.com) to work , use [parcel.js](https://parceljs.org/) to convert es6 js files to web js files.
Install all of the depencies using this command.
```
npm i
npm run install
npm run build
```
First you'll need to install all the requirements that are needed to run the app.using the installation command,

```
 pip install -t lib -r requirements.txt
```

After installling google-app-engine in ur system . you can run this app locally via this command ,

### Run the app:

```
"C:\python_2.7\python.exe" "C:\Program Files (x86)\Google\google_appengine\dev_appserver.py" "./app.yaml"
```
