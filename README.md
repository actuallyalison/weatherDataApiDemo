# Code Challenge

## Use:

1) run import_data.py to initialize or update database
2) run analyze_data.py to populate aggregate data
3) run server.py
4) browse to (ex): 
   - localhost:(port listed by server)/api/weather?sid=USC00338552
   - localhost:(port listed by server)/api/weather

List of routes and their parameters:

   - /api/weather
     - sid=\[station ID\]
     - date=\[date as YYYY-MM-DD\]
     - page=\[page number\]
     - pagesize=\[results per page \(default 25\)\]
   - /api/yield
     - year=\[four digit year\]
   - /api/weather/stats
     - sid=\[station ID\]
     - year=\[four digit year\]
     - page=\[page number\]
     - pagesize=\[results per page \(default 25\)\]
 
## Dependencies (all installable via pip)

- flask 
- sqlalchemy
- sqlalchemy.orm
