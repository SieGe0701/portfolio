# Define the templates directory
$templateDir = "templates"

# Ensure the templates directory exists
if (-Not (Test-Path -Path $templateDir)) {
    Write-Host "The directory '$templateDir' does not exist. Please create it first." -ForegroundColor Red
    exit
}

# index.html - Home Page
Set-Content -Path "$templateDir/index.html" -Value @"
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio - Home</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>Welcome to My Portfolio!</h1>
    <nav>
        <a href="/">Home</a>
        <a href="/projects">Projects</a>
        <a href="/skills">Skills</a>
        <a href="/contact">Contact</a>
    </nav>
    <section>
        <h2>About Me</h2>
        <p>Hi, I'm R Srinivas Prabhu. I'm a Data Science and Engineering student at Manipal Institute of Technology with a strong organizational background and technical skills. I aim to contribute my fullest potential to organizational growth while seeking personal and professional development opportunities.</p>
    </section>
</body>
</html>
"@

# projects.html - Projects Page
Set-Content -Path "$templateDir/projects.html" -Value @"
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio - Projects</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>My Projects</h1>
    <nav>
        <a href="/">Home</a>
        <a href="/projects">Projects</a>
        <a href="/skills">Skills</a>
        <a href="/contact">Contact</a>
    </nav>
    <ul>
        <li><strong>VTune:</strong> Built a Flask web application that recognizes hummed tunes using ACRCloud's API for audio recognition. This project allows users to hum a tune, and the system identifies the matching song.</li>
        <li><strong>Research Project on SMOTE Implementation:</strong> Compared the performance of ensemble models using SMOTE. Classified traffic crashes using the Chicago Data Portal. Presented at Microsoft CMT conference (June 2023).</li>
        <li><strong>Fake News Detection:</strong> Used Kaggle's open-source dataset to detect fake news using models like Logistic Regression, Decision Tree, Random Forest, and XGBoost (April 2023).</li>
    </ul>
</body>
</html>
"@

# skills.html - Skills Page
Set-Content -Path "$templateDir/skills.html" -Value @"
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio - Skills</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>My Skills</h1>
    <nav>
        <a href="/">Home</a>
        <a href="/projects">Projects</a>
        <a href="/skills">Skills</a>
        <a href="/contact">Contact</a>
    </nav>
    <ul>
        <li>Programming: Java, Python, SQL, Scala, C/C++, HTML, CSS, JavaScript</li>
        <li>Libraries/Frameworks: Scikit Learn, TensorFlow, Gymnasium, Matplotlib, Numpy, Pandas</li>
        <li>Databases: Oracle, PostgreSQL</li>
        <li>Soft Skills: Communication, Adaptability, Productivity, Time Management</li>
        <li>Other Skills: Machine Learning, Statistics, Operations Research</li>
    </ul>
</body>
</html>
"@

# contact.html - Contact Page
Set-Content -Path "$templateDir/contact.html" -Value @"
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio - Contact</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>Contact Me</h1>
    <nav>
        <a href="/">Home</a>
        <a href="/projects">Projects</a>
        <a href="/skills">Skills</a>
        <a href="/contact">Contact</a>
    </nav>
    <p>Email: sprabhur0@gmail.com</p>
    <p>Phone: 8867593111</p>
    <p>Location: Manipal, Karnataka, India</p>
    <p>Languages: English, Hindi, Kannada, Konkani</p>
</body>
</html>
"@

# Output completion message
Write-Host "Templates populated successfully with VTune and other project details in '$templateDir'." -ForegroundColor Green
