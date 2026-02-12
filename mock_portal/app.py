from flask import Flask, render_template

app = Flask(__name__)

JOBS = [
    {"id": 1, "title": "Senior Python Developer", "company": "TechGlobal Solutions", "location": "Remote", "salary": "₹12 - 18 LPA", "skills": "Python, FastAPI, SQL, Docker"},
    {"id": 2, "title": "Generative AI Engineer", "company": "FutureAI Labs", "location": "Hyderabad", "salary": "₹15 - 25 LPA", "skills": "Python, LangChain, LLM, OpenAI"},
    {"id": 3, "title": "Frontend Developer (React)", "company": "Creative Web Studio", "location": "Mumbai", "salary": "₹8 - 12 LPA", "skills": "React, CSS, HTML, JavaScript"},
    {"id": 4, "title": "Data Analyst", "company": "Insight Data Corp", "location": "Bangalore", "salary": "₹10 - 15 LPA", "skills": "Python, Pandas, Tableau, Excel"},
    {"id": 5, "title": "DevOps Engineer", "company": "CloudScale Systems", "location": "Remote", "salary": "₹14 - 20 LPA", "skills": "Docker, Kubernetes, AWS, Terraform"},
    {"id": 6, "title": "Java Backend Developer", "company": "Enterprise Software Inc", "location": "Chennai", "salary": "₹12 - 16 LPA", "skills": "Java, Spring Boot, Microservices, PostgreSQL"},
    {"id": 7, "title": "Full Stack Developer", "company": "MERN Stack Hub", "location": "Remote", "salary": "₹15 - 22 LPA", "skills": "Node.js, Express.js, React, MongoDB, JavaScript"}
]

@app.get("/")
def home():
    return render_template('index.html', jobs=JOBS)

@app.get("/apply/<int:job_id>")
def apply_form(job_id):
    job = next((j for j in JOBS if j['id'] == job_id), None)
    return render_template('form.html', job=job)

@app.post("/submit")
def submit():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(port=5001)