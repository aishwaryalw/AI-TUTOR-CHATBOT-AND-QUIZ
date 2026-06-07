from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


LESSONS = {
    "photosynthesis": {
        "title": "Photosynthesis",
        "answer": "Photosynthesis is the process plants use to make food. Leaves take in carbon dioxide from air, roots absorb water, and sunlight provides energy. Chlorophyll helps convert these into glucose and oxygen.",
        "steps": [
            "Sunlight is captured by chlorophyll in leaves.",
            "Carbon dioxide and water are used as raw materials.",
            "The plant makes glucose for energy and releases oxygen.",
        ],
        "questions": [
            {
                "question": "What is the main source of energy for photosynthesis?",
                "options": ["Sunlight", "Soil", "Wind", "Moonlight"],
                "answer": "Sunlight",
            },
            {
                "question": "Which gas do plants release during photosynthesis?",
                "options": ["Oxygen", "Nitrogen", "Hydrogen", "Methane"],
                "answer": "Oxygen",
            },
            {
                "question": "Which green pigment helps plants absorb light?",
                "options": ["Chlorophyll", "Hemoglobin", "Melanin", "Keratin"],
                "answer": "Chlorophyll",
            },
        ],
    },
    "gravity": {
        "title": "Gravity",
        "answer": "Gravity is a force that pulls objects toward each other. On Earth, it pulls objects toward the ground and keeps the Moon moving around Earth.",
        "steps": [
            "Every object with mass has gravity.",
            "More mass means stronger gravity.",
            "Gravity gives objects weight and keeps planets in orbit.",
        ],
        "questions": [
            {
                "question": "What does gravity do to objects near Earth?",
                "options": ["Pulls them downward", "Makes them invisible", "Turns them hot", "Stops all motion"],
                "answer": "Pulls them downward",
            },
            {
                "question": "Which object has stronger gravity?",
                "options": ["An object with more mass", "An object with less color", "An object with no sound", "A smaller shadow"],
                "answer": "An object with more mass",
            },
            {
                "question": "Gravity helps keep the Moon moving around what?",
                "options": ["Earth", "Mars", "The ocean", "A cloud"],
                "answer": "Earth",
            },
        ],
    },
    "fractions": {
        "title": "Fractions",
        "answer": "A fraction shows part of a whole. The top number is the numerator, which tells how many parts you have. The bottom number is the denominator, which tells how many equal parts the whole is divided into.",
        "steps": [
            "In 3/4, 3 is the numerator.",
            "In 3/4, 4 is the denominator.",
            "Fractions can be added easily when denominators are the same.",
        ],
        "questions": [
            {
                "question": "In the fraction 2/5, what is the numerator?",
                "options": ["2", "5", "7", "10"],
                "answer": "2",
            },
            {
                "question": "What does the denominator show?",
                "options": ["Total equal parts", "Only shaded parts", "The final answer", "A unit of time"],
                "answer": "Total equal parts",
            },
            {
                "question": "Which fraction means one half?",
                "options": ["1/2", "2/1", "3/4", "4/3"],
                "answer": "1/2",
            },
        ],
    },
    "water cycle": {
        "title": "Water Cycle",
        "answer": "The water cycle is the continuous movement of water on Earth. Water evaporates into vapor, forms clouds by condensation, falls as precipitation, and returns to rivers, oceans, and groundwater.",
        "steps": [
            "Evaporation changes liquid water into vapor.",
            "Condensation forms clouds.",
            "Precipitation brings water back as rain, snow, or hail.",
        ],
        "questions": [
            {
                "question": "What is evaporation?",
                "options": ["Liquid water changing into vapor", "Clouds falling down", "Ice becoming rock", "Rain entering soil"],
                "answer": "Liquid water changing into vapor",
            },
            {
                "question": "What forms when water vapor condenses?",
                "options": ["Clouds", "Fire", "Sand", "Metal"],
                "answer": "Clouds",
            },
            {
                "question": "Rain and snow are examples of what?",
                "options": ["Precipitation", "Evaporation", "Friction", "Magnetism"],
                "answer": "Precipitation",
            },
        ],
    },
}


def normalize(text):
    return " ".join((text or "").strip().lower().split())


def find_lesson(text):
    normalized = normalize(text)
    for key, lesson in LESSONS.items():
        if key in normalized:
            return lesson
    return None


def make_general_answer(message):
    clean = (message or "").strip()
    if not clean:
        return {
            "title": "Ask a Question",
            "answer": "Type a topic or question, for example: What is photosynthesis?",
            "steps": ["You can ask about photosynthesis, gravity, fractions, or the water cycle."],
        }

    return {
        "title": "Study Helper",
        "answer": f"I can help you understand '{clean}'. Start by breaking the topic into meaning, key points, and one example. For a stronger answer, ask about photosynthesis, gravity, fractions, or the water cycle.",
        "steps": [
            "Write the main idea in one sentence.",
            "List two or three important facts.",
            "Test yourself with a short quiz.",
        ],
    }


def build_quiz(topic):
    lesson = find_lesson(topic)
    if lesson:
        return {
            "title": f"{lesson['title']} Quiz",
            "questions": lesson["questions"],
        }

    clean = (topic or "general study").strip()
    return {
        "title": f"{clean.title()} Quiz",
        "questions": [
            {
                "question": f"What is the first step when learning {clean}?",
                "options": ["Understand the basic meaning", "Memorize random words", "Skip examples", "Avoid practice"],
                "answer": "Understand the basic meaning",
            },
            {
                "question": f"What helps you remember {clean} better?",
                "options": ["Practice with examples", "Never revise", "Guess only", "Ignore mistakes"],
                "answer": "Practice with examples",
            },
            {
                "question": f"What should you do after studying {clean}?",
                "options": ["Take a short quiz", "Close the topic forever", "Remove notes", "Avoid questions"],
                "answer": "Take a short quiz",
            },
        ],
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    message = (request.json or {}).get("message", "")
    lesson = find_lesson(message)
    reply = lesson if lesson else make_general_answer(message)
    return jsonify(reply)


@app.route("/quiz", methods=["POST"])
def quiz():
    topic = (request.json or {}).get("topic", "")
    return jsonify(build_quiz(topic))


if __name__ == "__main__":
    app.run(debug=True)
