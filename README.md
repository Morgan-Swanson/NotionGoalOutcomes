# NotionGoalOutcomes

## Mission
The mission of this project is to help people achieve their goals using Notion. 

## User Story
As a Notion user, I want to track key metrics to montior progress towards my goals without having to manually calculate them after each change to the data.

### Example
Goal Outcome: "Have at daily score of more than 3/5 in emotional wellbeing for 60 days this quarter"

Daily Tracking: Wellbeing (number 1-5)

## Strategy
1. Create an Objective database that includes parameters necessary to compute the key metric.
2. Create a Data Tracking database where metrics are recorded each day.
3. Create a script which pulls the Tracking data and computes the metrics according to the parameters in the Objective database, then updates the Objective database with the most recent metric.

## How to Use
First, you need to update your data model in the objective database. 

Required Objective Properties:
* Name (text),
* Status (status), <- indicate that the objective is 'Underway' if you'd like it to be updated by the script
* Tracker (text), <- name of field used to calculate metrics in tracker db
* Metric (text), <- how to aggregate data (current options are 'Count', 'Sum', & 'Count Greater Than'
* Argument (number), <- necessary for the 'Count Greater Than' feature,
* Last Update (date), <- necessary to track when the script has changed the progress
* Completed (number), <- this is where the key metric is stored after it's calculated,
* End Date (date), <- necessary to window the daily tracking for only when that objective is active


Required Tracking Properties:
* Date (date), <- date that the data is being tracked for 

After you've updated these databases, here is some sample code to run the program:
```python
from notion_client import Client
from tracking import get_tracking
from outcome import Outcome

secret_key = "insert secret here"
goal_outcomes_db = "objective database id"
daily_tracking_db = "daily tracking database id"

# 1. Initialize the Notion Client
notion = Client(auth=secret_key)

# 2. Pull data from the Daily Tracking database
tracking_db = notion.databases.query(database_id=daily_tracking_db)

# 3. Transform data to a Pandas DataFrame
data = get_tracking(tracking_db)

# 4. Pull data from the Goal Outcomes Database
outcomes_db = notion.databases.query(database_id=goal_outcomes_db)

# 5. Extract necessary parameters into object store
outcomes_objs = [Outcome(o) for o in outcomes_db['results']]

# 6. Calculate outcome progress using data and parameters
outcomes_updated = [o.calculate(data) for o in outcomes_objs]

# 7. Push updates to Goal Outcomes table
outcomes_pushed = [o.push(notion) for o in outcomes_updated]
```

I hope you enjoy this tool!
