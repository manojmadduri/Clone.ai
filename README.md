# **Clone.AI - Phase 1 (Text-Based AI)**  
A local AI system that **learns everything about you** and **responds exactly as you would**, using stored personal facts. This is **Phase 1**, where the AI is trained on text input and can recall **only what you’ve explicitly added**. The system retrieves relevant data and **reformats responses naturally** using a **local LLM (Mistral GGUF)**.

---

## **📂 Project Structure**  

```
Clone.AI/
│── backend/                   # FastAPI backend
│   ├── models/                # Stores local AI model (GGUF format)
│   ├── db_manager.py          # Manages SQLite database
│   ├── retrieval.py           # FAISS index for efficient fact retrieval
│   ├── model_manager.py       # Local LLM for reformatting responses
│   ├── main.py                # FastAPI app (handles API endpoints)
│   ├── schemas.py             # Defines API request/response data models
│   ├── requirements.txt       # Dependencies for backend
│── frontend/                  # React frontend
│   ├── src/                   # React app source files
│   ├── public/                # Static assets
│   ├── package.json           # React dependencies
│── README.md                  # Documentation
│── .gitignore                 # Ignores unnecessary files in git
```

---

## **🚀 Features**  

✅ **Personal Memory AI:** Stores personal facts and retrieves them on demand.  
✅ **FAISS Vector Search:** Finds the most relevant stored facts efficiently.  
✅ **Natural Responses:** Uses **Mistral GGUF** to reformat responses **into first-person style**.  
✅ **FastAPI Backend:** Provides RESTful APIs for data storage & querying.  
✅ **React Frontend:** Simple UI for adding/querying data.  
✅ **Fully Offline:** No external API calls, **everything runs locally**.  

---

## **🛠️ Libraries Used**  

### **Backend (FastAPI)**
| Library                   | Purpose |
|---------------------------|---------|
| `fastapi==0.95.2`         | API framework |
| `uvicorn==0.22.0`         | ASGI server |
| `sqlite-utils==3.30`      | SQLite database management |
| `pydantic==1.10.7`        | Data validation |
| `faiss-cpu==1.7.4`        | Efficient similarity search |
| `sentence-transformers==2.2.2` | Text embeddings for FAISS |
| `transformers==4.28.0`    | LLM model loading |
| `torch==2.0.0`            | Required for model inference |
| `ctransformers==0.2.27`   | Loads GGUF models optimized for **CPU** |
pip install torch transformers peft accelerate datasets bitsandbytes sentencepiece

---

### **Frontend (React)**
| Library                  | Purpose |
|--------------------------|---------|
| `react`                 | Core React library |
| `react-dom`             | React rendering |
| `axios`                 | API requests |
| `vite`                  | Fast React development |

---

## **🔧 Installation & Setup**  

### **1️⃣ Install Dependencies**  

#### **📌 Backend Setup (FastAPI + FAISS)**
```bash
# Navigate to backend
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Upgrade pip & install dependencies
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

#### **📌 Frontend Setup (React)**
```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Start React app
npm run dev
```

---

## **📥 Download & Load Local LLM Model (GGUF - Mistral 7B)**  

Clone.AI **does not use cloud AI**. You must **download and store a local AI model** in `backend/models/`.

```bash
# Create model directory
mkdir -p backend/models/mistral-gguf

# Download GGUF model
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf -P backend/models/mistral-gguf/
```

---

## **▶️ Running the Project**  

### **1️⃣ Start Backend (FastAPI)**
```bash
cd backend
uvicorn main:app --reload
```
🚀 **Backend will run on:** `http://127.0.0.1:8000`

### **2️⃣ Start Frontend (React)**
```bash
cd frontend
npm run dev
```
🌍 **Frontend will run on:** `http://localhost:3000`

---

## **💡 How It Works**

### **1️⃣ Add Personal Facts**
You can **add** stored facts like:
- **Title:** `"Mother's Name"`  
- **Content:** `"Vidya Annapurna"`

> **API Endpoint:** `POST /add_text`  
> **Example Request:**
> ```json
> {
>   "title": "Mother's Name",
>   "content": "Vidya Annapurna"
> }
> ```

---

### **2️⃣ Query AI (Ask Personal Questions)**
When you ask:
> `"What is my mother’s name?"`

> **API Endpoint:** `POST /query_ai`  
> **Example Request:**
> ```json
> {
>   "query": "What is my mother's name?"
> }
> ```

### **📌 How Response is Generated**
- The AI **retrieves stored facts** from FAISS.  
- It **reformats** them into a **natural response** using the **Mistral GGUF model**.  

#### **Before (Raw DB Result)**  
```
Stored Fact: Mother's Name | Vidya Annapurna
User Question: What is my mother's name?
```

#### **After (Final AI Answer)**
```
"Your mother's name is Vidya Annapurna."
```

---

## **📜 API Endpoints**

### **1️⃣ Add Personal Data**
> `POST /add_text`  
Stores new personal facts.

| Field  | Type   | Description |
|--------|--------|-------------|
| `title`  | `string` | A label for the fact (e.g., `"Mother's Name"`) |
| `content` | `string` | The actual fact (e.g., `"Vidya Annapurna"`) |

**Example Request**
```json
{
  "title": "Mother's Name",
  "content": "Vidya Annapurna"
}
```

**Example Response**
```json
{
  "status": "success",
  "message": "Text added and FAISS index updated."
}
```

---

### **2️⃣ Query AI**
> `POST /query_ai`  
Retrieves relevant stored facts and returns a **first-person natural response**.

| Field   | Type   | Description |
|---------|--------|-------------|
| `query` | `string` | The user’s question |

**Example Request**
```json
{
  "query": "What is my mother's name?"
}
```

**Example Response**
```json
{
  "answer": "Your mother's name is Vidya Annapurna."
}
```

---

## **🛠️ Debugging & Troubleshooting**

### **🚨 Backend Issues**
**1️⃣ FastAPI not starting?**  
Run:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**2️⃣ FAISS not retrieving the correct data?**  
Try resetting the index:
```bash
rm backend/personal_faiss.index
```
Then restart:
```bash
uvicorn main:app --reload
```

**3️⃣ Model taking too long to respond?**  
- Reduce `max_new_tokens=50` in `model_manager.py`.  
- Lower `temperature=0.3` for **faster responses**.  

---

## **📌 Next Steps: Phase 2**
In **Phase 2**, we will:
✅ Add **Voice Integration** (Speech-to-Text + Text-to-Speech).  
✅ Store **spoken conversations** as additional memory.  
✅ AI **replies in your voice** using **Coqui TTS**.  

🚀 **Clone.AI is evolving to become your true digital self!**  

---

## **📜 Final Notes**
- This **Phase 1 AI only knows what you tell it**.  
- It will **never make up information**.  
- Everything runs **fully offline**, keeping **your data private**.  

Enjoy your personal AI! 🎉🚀  
Let me know if you need more enhancements!



# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)


