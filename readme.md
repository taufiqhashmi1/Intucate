# Intucate | Asynchronous AI Prompt Engine

A high-performance middleware architecture designed to resolve LLM latency issues through concurrent request processing. Built with **Flask**, **MongoDB Atlas**, and **Python's `asyncio`**, this engine allows for the simultaneous execution of multiple AI prompts, significantly reducing the total turnaround time for batch operations.

---

## 🚀 Features

*   **Asynchronous Batch Processing:** Utilizes `asyncio.gather` to fire multiple LLM requests in parallel, ensuring the total processing time is only as long as the single slowest request.
*   **Dynamic Prompt Management:** Fetch and inject "Expert Persona" templates stored in NoSQL collections rather than hard-coding system instructions.
*   **Automated Persistence:** Every interaction (userInput, final prompt, and AI response) is logged into a MongoDB `history` collection for auditability.
*   **SaaS-Ready UI:** A responsive, dark-themed Single Page Application (SPA) built with Tailwind CSS, supporting both single-query and multi-line batch processing.
*   **GitHub Student Developer Integration:** Configured to utilize free-tier `gpt-4o-mini` access via GitHub Models.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.10+, Flask
*   **Database:** MongoDB Atlas (NoSQL)
*   **AI Integration:** OpenAI SDK via GitHub Models
*   **Concurrency:** `asyncio`
*   **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
*   **Deployment:** Vercel (Serverless)

---

## 📂 Project Structure

```text
Intucate/
├── app.py              # Main Flask application & API routes
├── vercel.json         # Vercel deployment configuration
├── requirements.txt    # Project dependencies
├── .env                # Sensitive credentials (API keys/URI)
├── templates/
│   └── index.html      # Professional UI template
└── .venv/              # Local virtual environment
```

---

## ⚙️ Setup & Installation

**1. Clone the Repository:**
```bash
git clone https://github.com/taufiqhashmi1/Intucate.git
cd Intucate
```

**2. Configure Virtual Environment:**
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Environment Configuration:**
Create a `.env` file in the root directory and add your credentials:
```env
OPENAI_API_KEY=your_github_token
MONGO_URI=mongodb+srv://admin:password@cluster.mongodb.net/
```

**5. Run Locally:**
```bash
python app.py
```

---

## 📡 API Endpoints

### Single Prompt
*   **URL:** `/api/ask`
*   **Method:** `POST`
*   **Body:** `{"userInput": "string"}`
*   **Action:** Fetches the `Education_Prompt` template, replaces the placeholder, and returns a single AI response.

### Async Batch
*   **URL:** `/api/ask-batch`
*   **Method:** `POST`
*   **Body:** `{"userInputs": ["string1", "string2", ...]}`
*   **Action:** Processes all strings independently and concurrently using an async worker pool.

---

## 🏗️ Architecture Rationale



*   **Why Async?** LLM API calls are I/O bound. Synchronous processing would block the server, causing significant delays and potential timeouts for other users. Async logic allows for high-concurrency handling within a single thread.
*   **Why MongoDB?** The flexible BSON structure of MongoDB is ideal for logging diverse AI responses and varying prompt templates without the need for rigid schema migrations.
*   **Why Serverless (Vercel)?** Utilizing Vercel allows the application to scale horizontally, spinning up Lambda instances only when traffic is received, making it a cost-effective and reliable deployment strategy.

---

## 👨‍💻 Developed By

**Taufiq Hashmi**  
*Computer Science Engineering Student @ DJSCE*
*   [GitHub](https://github.com/taufiqhashmi1)
*   [LinkedIn](https://linkedin.com/in/taufiq-hashmi)