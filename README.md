# Newspaper Categorization 



## Installation

Follow these steps to install the required Python dependencies and set up the XAMPP Control Panel:

```bash
# Install Python dependencies
pip install -r requirements.txt
```
# Start the XAMPP Control Panel
xampp-control.exe

start Apache and MySql




# For create Database 

Create a new database in XAMPP and name it "newspaper."

Run the following SQL command in the "newspaper" database:

```bash
CREATE TABLE Crime (
    Location VARCHAR(200),
    Type_of_Crime VARCHAR(200),
    Suspects VARCHAR(200),
    Victims VARCHAR(200),
    Date_and_Time VARCHAR(200),
    Authorities_Involved VARCHAR(200),
    Motive VARCHAR(200),
    Status VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Politics (
    Region VARCHAR(200),
    Government_Policies VARCHAR(200),
    Elections VARCHAR(200),
    Political_Parties VARCHAR(200),
    Officials VARCHAR(200),
    Meetings_and_Summits VARCHAR(200),
    Reforms VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Business (
    Industry VARCHAR(200),
    Companies VARCHAR(200),
    Markets VARCHAR(200),
    Economic_Policies VARCHAR(200),
    Financial_Results VARCHAR(200),
    Investments VARCHAR(200),
    Startups VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Health (
    Medical VARCHAR(200),
    Public_Health VARCHAR(200),
    Fitness_and_Wellness VARCHAR(200),
    Medical_Institutions VARCHAR(200),
    Health_Policies VARCHAR(200),
    Epidemics_and_Pandemics VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Technology (
    Industry VARCHAR(200),
    Companies VARCHAR(200),
    Products_and_Gadgets VARCHAR(200),
    Innovation VARCHAR(200),
    Cybersecurity VARCHAR(200),
    Emerging_Technologies VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Sport (
    Level VARCHAR(200),
    Sport_Type VARCHAR(200),
    Players VARCHAR(200),
    Match_Details VARCHAR(200),
    Events VARCHAR(200),
    Records VARCHAR(200),
    Controversies VARCHAR(200),
    Event_Type VARCHAR(200),
    Event_Level VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Entertainment (
    Industry VARCHAR(200),
    Celebrities VARCHAR(200),
    Events VARCHAR(200),
    Movies_Shows VARCHAR(200),
    Music VARCHAR(200),
    Gossip VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Economics (
    Indicators VARCHAR(200),
    Market_Trends VARCHAR(200),
    Government_Policies VARCHAR(200),
    Financial_Institutions VARCHAR(200),
    International_Trade VARCHAR(200),
    Economic_Challenges VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE World_News (
    Region VARCHAR(200),
    Events VARCHAR(200),
    Leaders VARCHAR(200),
    Agreements VARCHAR(200),
    Conflicts VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Local_News (
    Community_Events VARCHAR(200),
    Development VARCHAR(200),
    Public_Issues VARCHAR(200),
    Education VARCHAR(200),
    Crime VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Science (
    Field VARCHAR(200),
    Discoveries VARCHAR(200),
    Institutions VARCHAR(200),
    Space_Exploration VARCHAR(200),
    Environmental_Science VARCHAR(200),
    Technological_Applications VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Lifestyle (
    Category VARCHAR(200),
    Trends VARCHAR(200),
    Tips VARCHAR(200),
    Personal_Stories VARCHAR(200),
    Luxury VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);

CREATE TABLE Education (
    Institutions VARCHAR(200),
    Programs VARCHAR(200),
    Exams VARCHAR(200),
    Scholarships VARCHAR(200),
    Reforms VARCHAR(200),
    Achievements VARCHAR(200),
    Published_Date VARCHAR(200),
    Published_Day VARCHAR(200),
    Event_Date VARCHAR(200),
    Gist VARCHAR(2000)
);
```
# Execute the code

```bash
streamlit run ui.py
