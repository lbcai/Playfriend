from flask import Flask, render_template

app = Flask(__name__)

index = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Redirecting...</title>
</head>
<body>
<script>
try { window.location.replace("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot"); }
catch(e) { window.location = "https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot"; }
</script>
</body>
</html>
"""


@app.route('/')
def index():
    return index


if __name__ == '__main__':
    app.run()
