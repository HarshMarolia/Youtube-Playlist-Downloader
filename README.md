# YouTube Playlist Downloader
A web application that lets the user download
YouTube playlists in batch.

## Technologies Used
* HTML, CSS and JavaScript for public webpages.
* Bootstrap and jQuery for enhancing the front-end.
* Flask for the back-end server.
<br><br>
[Preview on Heroku](https://y-t-downloader.herokuapp.com/)
<br><br>

## Execution
1. Create a virtual environment and enter it.
   ```bash
   python -m venv env
   ```
   ```bash
   # *NIX
   ./env/bin/activate
   ```
   ```cmd
   REM Windows Command Prompt
   env\Scripts\activate
   ```
   ```powershell
   # Windows PowerShell
   .\env\Scripts\activate
   ```
2. Install the dependencies.
   ```bash
   pip install -r requirements.txt
   ```
3. Fire up the application!
   ```bash
   flask run -p 8080
   ```

# Execution (Docker)
Simply use Docker Compose.
```bash
docker compose up -d
```

The application runs on http://localhost:8080 by default.

![gallery](https://user-images.githubusercontent.com/53485461/123506862-f6867980-d683-11eb-8661-79ce6594acfa.jpg)
![gallery (2)](https://user-images.githubusercontent.com/53485461/123506863-f7b7a680-d683-11eb-985f-9c23fdec2c77.jpg)
![gallery (1)](https://user-images.githubusercontent.com/53485461/123506864-f8503d00-d683-11eb-9f0d-d4f9c7491bfb.jpg)


# Made with ❤ by Harsh and [Param](https://www.paramsid.com).
