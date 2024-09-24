# Youtube analytics

#### Project Installation: 
- Create virtual enviroment inside project directory ```python -m venv env```
- Activate the virtual enviroment ```source env/Scripts/activate```
- Install dependencies ```pip install -r requirements.txt```

#### Database configuration
- You might need to change the absolute path of the db in ```database.py``` inside the ```database``` folder , based on the drive you clone this code.

#### Run the application
- In the project root, open the terminal and run command ```uvicorn app.main:app --reload```.

#### Feeding data to database
- The ```analytics_db.db``` available inside the ```data``` folder already contains the data of videos.
- To manually insert data to  ```analytics_db.db```, in the project root, run command ```python -m app.scripts.fetch_data```.

#### Checking the response
- To check the response, in your browser, open ```localhost:8000/docs``` to open the swagger ui.

#### Project Structure
<pre>
|----- app
|       |---- database
|       |     |---- database.py
|       |---- dependencies
|       |     |---- video_dependencies.py
|       |---- interfaces
|       |     |---- video_repository_interface.py   
|       |---- models
|       |     |---- video.py
|       |---- repositories
|       |     |---- video_repository.py
|       |---- routers
|       |     |---- video_router.py
|       |---- schemas
|       |     |---- video_schemas.py
|       |---- scripts
|       |     |---- fetch_data.py
|       |---- main.py
|----- data
|       |---- analytics_db.db
|       |---- trending_videos.csv
|----- requirements.txt
|----- README.md
|----- .gitignore

<pre>
