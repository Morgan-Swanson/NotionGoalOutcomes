# NotionGoalOutcomes

## Mission
The mission of this project is to help people achieve their goals using Notion. 

## User Story
As a Notion user, I want to track key metrics to montior progress towards my goals without having to manually calculate them after each change to the data.

## Strategy
Create an Objective database that includes parameters necessary to compute the key metric
Create a Data Tracking database where metrics are recorded each day
Create a script which pulls the Tracking data and computes the metrics according to the parameters in the Objective database, then updates the Objective database with the most recent metric.

## How to Use

```
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
