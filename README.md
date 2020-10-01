# ScheduleTool
A simple tool to create a Timetable based on a CSS Grid System. Mobile friendly, easy to extend and free.
## Example
<img src="example.png" height=300></img> -----  <img src="example_mobile.png" height=300></img>
## Usage 
- Install the necessary requirements via pip:
    ```bash
    pip3 install --user -r requirements.txt
    ```

- Create a Google Docs API key so this application can access your documents. 
See [this URL](https://developers.google.com/sheets/api/quickstart/python) on how to create said API key.

- Create a Google Spreadsheet with a table named `timetable`
- Fill in the first line:


| id                   | day            | start_time                           | end_time                           | class                             | track                               | title            | chair            | speaker            | hidden              | short              |
| -------------------- | -------------- | ------------------------------------ | ---------------------------------- | --------------------------------- | ----------------------------------- | ---------------- | ---------------- | ------------------ | ------------------- | ------------------ |
| Unique ID of session | Day of Session | Start time in 24h format without `:` | End time in 24h format without `:` | Special css class (eg. for color) | Track of session (eg. VCBM / joint) | Title of Session | Chair of Session | Speaker of Session | hidden (true/false) | short (true/false) |											
- Save the file `credentials.json` from the previous step into `~/.config/gspread/credentials.json`. Under Windows systems, place the file under `%APPDATA%\gspread\credentials.json`.
    > Note: The `gspread` folder does not exist automatically once gspread is installed, you have to create it manually.
(Refer to the [gspread documentation](https://gspread.readthedocs.io/en/latest/) for further info.)

- Run the whole thing: `python3 main.py`

## Explanation
### ID
- String
- A uniqe id for the session. This id can be used as html anchor for a detailed preview. The whole session a a link reffering to this anchor.
### Day
- String
- Group every entry by day. The days will be created in order of appearance.
- Example: `Monday`,  `Tuesday`, `Last Day`

### start_time
- int
- Start time for the session
- 24 hour format without any special chars
- in 30 minutes steps
- Example: `0800`, `1230`, `1600`

### end_time
- int
- End time for the session
- as start_time

### class
- String
- CSS class for this session
- See style.css for more information
- Example: `VCBM`, `joint`

### track
- String
- CSS grid-column: for this session
- See style.css for more information
- Example: `VCBM`, `joint`, `gcpr-start / vcbm-end`

### chair 
- String
- Name of Session-Chair
- See main.py to turn this globally on/off

### speaker 
- String
- Name of Session-Speaker
- See main.py to turn this globally on/off
### hidden
- bool (actually a string: `true` , `false`)
- Determines if whole session is hidden.

### hidden
- bool (actually a string: `true` , `false`)
- Determines if its a short session. This will add another css class to it.
- Session will be displayed in one line.

## CSS
To view this timetable in a nice way the css file (style.css) must be included into the header.
just include the files content into a `<style> ... </style>` tag.

## Wordpress
Wordpress does some intressting stuff to the styling.
A (not so nice) way to include custom css is to click on the ` customize` button on the upper left side. This works only if you are an admin. Now there is a menue for additional css. Please make shure that you dont replace everything.