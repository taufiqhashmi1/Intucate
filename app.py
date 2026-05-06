import os
import asyncio
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --- Database Setup ---
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["ai_education_db"]
prompts_collection = db["prompts"]
history_collection = db["history"]

# --- OpenAI Client Setup ---
# Using Async client to satisfy Step 6 asynchronous requirements
aclient = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://models.inference.ai.azure.com"
)

# --- Step 2: Database Seeding ---
# Ensure the prompt template exists in the DB on startup
if not prompts_collection.find_one({"_id": "Education_Prompt"}):
    prompts_collection.insert_one({
        "_id": "Education_Prompt",
        "template": "You are an expert in education domain. Answer the following: {{userInput}}"
    })

# --- Frontend Route ---
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# --- Steps 1, 3, 4, 5: Single Input Endpoint ---
@app.route('/api/ask', methods=['POST'])
async def ask_single():
    data = request.get_json()
    
    # Step 1: Extract userInput
    user_input = data.get('userInput')
    if not user_input:
        return jsonify({"error": "Missing 'userInput' in request body"}), 400

    # Step 3: Fetch template and replace placeholder
    prompt_doc = prompts_collection.find_one({"_id": "Education_Prompt"})
    final_prompt = prompt_doc['template'].replace("{{userInput}}", user_input)

    try:
        # Step 3: ChatGPT API Call
        chat_completion = await aclient.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt}],
            model="gpt-4o-mini", # Switch to gpt-4o if preferred
        )
        ai_response = chat_completion.choices[0].message.content

        # Step 4: Store Request/Response in history collection
        history_collection.insert_one({
            "userInput": user_input,
            "final_prompt": final_prompt,
            "response": ai_response
        })

        # Step 5: Return Response in JSON format
        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Step 6: Asynchronous Batch Endpoint ---
@app.route('/api/ask-batch', methods=['POST'])
async def ask_batch():
    data = request.get_json()
    user_inputs = data.get('userInputs')

    if not user_inputs or not isinstance(user_inputs, list):
        return jsonify({"error": "Request body must contain a 'userInputs' list"}), 400

    # Fetch the prompt from NoSQL
    prompt_doc = prompts_collection.find_one({"_id": "Education_Prompt"})
    template = prompt_doc['template']

    # Helper function to process a single string asynchronously
    async def process_string(u_input):
        final_prompt = template.replace("{{userInput}}", u_input)
        try:
            completion = await aclient.chat.completions.create(
                messages=[{"role": "user", "content": final_prompt}],
                model="gpt-4o-mini",
            )
            res_text = completion.choices[0].message.content
            return {
                "userInput": u_input, 
                "final_prompt": final_prompt, 
                "response": res_text
            }
        except Exception as e:
            return {
                "userInput": u_input, 
                "final_prompt": final_prompt, 
                "error": str(e)
            }

    # Process each string independently and run calls asynchronously without blocking
    tasks = [process_string(ui) for ui in user_inputs]
    results = await asyncio.gather(*tasks)

    final_responses = []
    history_docs = []

    # Extract responses in the same order and prep history documents
    for res in results:
        history_docs.append(res)
        if "response" in res:
            final_responses.append(res["response"])
        else:
            final_responses.append(f"Error: {res.get('error')}")

    # Save batch history
    if history_docs:
        history_collection.insert_many(history_docs)

    # Return list of AI responses in the same order
    return jsonify({"responses": final_responses})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5000)