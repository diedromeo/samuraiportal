from flask import Flask, render_template_string, request

app = Flask(__name__)

# Samurai name hidden in /robots.txt
SAMURAI_NAME = "Shingen"
FLAG = "FLAG{Samurai_Has_Sliced_Through_SQLi}"

# HTML Template with background, blossoms, katana cursor
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Samurai SQL Injection Challenge</title>
    <style>
        body {
            background: url('https://www.shutterstock.com/image-vector/illustration-vector-graphic-ninja-assassin-260nw-2374878967.jpg') no-repeat center center fixed;
            background-size: cover;
            color: white;
            font-family: "Cinzel", serif;
            text-align: center;
            padding-top: 80px;
            margin: 0;
            cursor: url('https://cur.cursors-4u.net/swords/swo-1/swo42.cur'), auto;
            overflow: hidden;
        }
        .container {
            background: rgba(0, 0, 0, 0.7);
            display: inline-block;
            padding: 30px;
            border: 2px solid red;
            border-radius: 10px;
            z-index: 10;
            position: relative;
        }
        input {
            padding: 10px;
            margin: 10px;
            width: 250px;
            border: 2px solid red;
            border-radius: 5px;
            background: black;
            color: white;
        }
        button {
            padding: 10px 20px;
            background: red;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
            border-radius: 5px;
        }
        .quote {
            margin-top: 20px;
            font-size: 1.2em;
            font-style: italic;
        }
        .gif {
            margin-top: 30px;
        }
        .gif img {
            max-width: 400px;
            border: 3px solid white;
            border-radius: 12px;
            box-shadow: 0 0 20px black;
        }
        .flag {
            position: absolute;
            top: 15px;
            width: 100%;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            background: rgba(0,0,0,0.6);
            padding: 10px;
            border-top: 3px solid crimson;
            border-bottom: 3px solid crimson;
        }
        /* Cherry blossom animation */
        .petal {
            position: fixed;
            top: -10%;
            width: 20px;
            height: 20px;
            background: pink;
            border-radius: 50%;
            opacity: 0.8;
            animation: fall linear infinite;
        }
        @keyframes fall {
            0% { transform: translateY(-10%) rotate(0deg); }
            100% { transform: translateY(110vh) rotate(360deg); }
        }
    </style>
</head>
<body>
    {% if success %}
        <div class="flag">🏴 CTF FLAG: {{ flag }} 🏴</div>
        <div class="gif">
            <img src="https://c.tenor.com/1A5GJQGUQcIAAAAd/tenor.gif" alt="Samurai Victory">
            <div class="quote">
                "You have entered the gate, warrior.<br>
                Shingen guides your blade. The illusions fall before you."
            </div>
        </div>
    {% else %}
        <div class="container">
            <h1>⚔️ Samurai Gate ⚔️</h1>
            <p>Are you ready to fight, samurai?</p>
            <p>"To enter the gate, you must defeat illusions of security."</p>
            <form method="POST">
                <input type="text" name="username" placeholder="Enter Samurai Name"><br>
                <input type="password" name="password" placeholder="Enter Password"><br>
                <button type="submit">Enter the Dojo</button>
            </form>
            {% if message %}
                <div class="quote">{{ message }}</div>
            {% endif %}
        </div>
    {% endif %}

    <!-- Cherry Blossom JS -->
    <script>
        function createPetal() {
            const petal = document.createElement("div");
            petal.classList.add("petal");
            document.body.appendChild(petal);

            // Random position and animation duration
            petal.style.left = Math.random() * 100 + "vw";
            petal.style.animationDuration = (5 + Math.random() * 5) + "s";
            petal.style.opacity = Math.random();
            petal.style.transform = "rotate(" + Math.random() * 360 + "deg)";

            setTimeout(() => { petal.remove(); }, 10000);
        }
        setInterval(createPetal, 300);
    </script>

    <!-- Extra cursor style + attribution -->
    <style type="text/css">
        * {cursor: url(https://cur.cursors-4u.net/mechanics/mec-4/mec321.cur), auto !important;}
    </style>
    <a href="https://www.cursors-4u.com/cursor/2009/09/10/katana-class.html" target="_blank" title="Katana Class">
        <img src="https://cur.cursors-4u.net/cursor.png" border="0" alt="Katana Class" style="position:absolute; top:0px; right:0px;" />
    </a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    success = False

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Vulnerable SQL simulation (CTF only)
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        if username == SAMURAI_NAME and (password == "' OR '1'='1" or password == "samurai"):
            message = "💥 You have defeated the illusions. Welcome, Samurai Shingen!"
            success = True
        else:
            message = "❌ The gate remains closed. Train harder, warrior."

    return render_template_string(HTML_TEMPLATE, message=message, success=success, flag=FLAG if success else None)

@app.route("/robots.txt")
def robots():
    return "Disallow: /ninja_path\n# The hidden samurai name is: Shingen", 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    app.run(debug=True)
