import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- Mock Data ---
JOBS_DB = [
    {
        "id": 1,
        "title": "Software Engineer (Python)",
        "company": "Tech Corp Local",
        "location": "Bangalore, India",
        "description": "We are looking for a Python developer with FastAPI experience.",
        "url": "http://localhost:8001/job/1"
    },
    {
        "id": 2,
        "title": "Data Scientist",
        "company": "DataViz Inc",
        "location": "Remote",
        "description": "Experience with Pandas and AI agents required.",
        "url": "http://localhost:8001/job/2"
    },
    {
        "id": 3,
        "title": "Frontend Developer",
        "company": "WebFlow Layouts",
        "location": "Mumbai, India",
        "description": "React and TypeScript expert needed.",
        "url": "http://localhost:8001/job/3"
    }
]

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>LocalHost Jobs</title></head>
        <body style="font-family: sans-serif; padding: 2rem; text-align: center;">
            <h1>Welcome to LocalHost Jobs</h1>
            <p>The #1 place to test your scrapers.</p>
            <a href="/login" id="login-btn" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Login</a>
        </body>
    </html>
    """

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return """
    <html>
        <head><title>Login - LocalHost Jobs</title></head>
        <body style="font-family: sans-serif; padding: 2rem; max-width: 400px; margin: auto;">
            <h2>Sign In</h2>
            <form action="/jobs" method="get">
                <label>Email</label><br>
                <input type="text" name="email" id="email" value="test@example.com" style="width: 100%; margin-bottom: 10px;"><br>
                <label>Password</label><br>
                <input type="password" name="password" id="password" value="123456" style="width: 100%; margin-bottom: 20px;"><br>
                <button type="submit" id="submit-login" style="width: 100%; background: #28a745; color: white; padding: 10px; border: none; cursor: pointer;">Sign In</button>
            </form>
        </body>
    </html>
    """

@app.get("/jobs", response_class=HTMLResponse)
async def jobs_page(q: str = ""):
    filtered_jobs = [j for j in JOBS_DB if q.lower() in j['title'].lower()] if q else JOBS_DB
    
    jobs_html = ""
    for job in filtered_jobs:
        jobs_html += f"""
        <div class="job-card" style="border: 1px solid #ccc; padding: 15px; margin-bottom: 10px; border-radius: 5px;">
            <h3 class="job-title"><a href="{job['url']}">{job['title']}</a></h3>
            <p class="company-name" style="font-weight: bold; color: #555;">{job['company']}</p>
            <p class="job-location" style="color: #777;">📍 {job['location']}</p>
            <p class="job-desc">{job['description']}</p>
        </div>
        """

    return f"""
    <html>
        <head><title>Job Listings</title></head>
        <body style="font-family: sans-serif; padding: 2rem;">
            <h2>Job Listings</h2>
            <form action="/jobs" method="get" style="margin-bottom: 20px;">
                <input type="text" name="q" id="search-box" placeholder="Search job titles..." value="{q}" style="padding: 5px; width: 300px;">
                <button type="submit" id="search-btn" style="padding: 5px 15px;">Search</button>
            </form>
            <div id="job-container">
                {jobs_html if jobs_html else "<p>No jobs found.</p>"}
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    # RUNNING ON PORT 8001 TO AVOID CONFLICT
    uvicorn.run(app, host="127.0.0.1", port=8001)