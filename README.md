# 🤖 AI Code Reviewer

An intelligent, multi-agent code review assistant powered by **LangGraph**, **Python AST**, and **Groq Cloud LLMs** (`llama-3.3-70b-versatile`).

## 🚀 Features
- **Multi-Agent Pipeline**: 4 specialized agents (AST Analyzer, Bug Detector, Quality Reviewer, Report Generator).
- **Multi-Language Support**: Review code in **Python**, **JavaScript**, **Java**, **C**, and **C++**.
- **File Upload**: Drag and drop code files for instant analysis with auto-language detection.
- **Static & Dynamic Analysis**: Combines Python's AST module and Radon cyclomatic complexity with high-end LLM reasoning.

## 🛠️ Local Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd ai_reviewer
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## ☁️ Deployment (Streamlit Cloud)
1. Push this project to a **GitHub** repository.
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/).
3. Select your repository and the `app.py` file.
4. **Crucial**: Add your `GROQ_API_KEY` to the **Secrets** section in the Streamlit Cloud dashboard.

## 📁 Project Structure
- `app.py`: Streamlit frontend.
- `agents/`: Core logic for the 4 agents.
- `graph/`: LangGraph workflow and state definitions.
- `utils/`: Groq client configuration.
