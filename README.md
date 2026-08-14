# 🤖 AI Code Reviewer CLI

A lightweight, automated Python command-line interface (CLI) tool that performs static code reviews, flags potential bugs, and suggests performance optimizations using the Google Gemini API.

---

## 💡 Overview

Stepping through code line-by-line to find edge cases, anti-patterns, or subtle bugs can be time-consuming. **AI Code Reviewer CLI** reads local Python files, passes the contents securely to Google's `gemini-3.6-flash` model, and returns a structured markdown report right in your terminal.

### Key Features
* **Automated Static Analysis:** Detects common runtime errors, unhandled edge cases, and PEP 8 style issues.
* **Quality Scoring:** Rates code readability and efficiency on a 1–10 scale with clear justifications.
* **Secure Credential Management:** Utilizes `python-dotenv` to keep private API keys isolated from source code.
* **Defensive Exception Handling:** Built-in safeguards for missing local files, network timeouts, and invalid CLI arguments.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **AI Model:** Google Gemini API (`google-genai` SDK)
* **Environment Management:** `python-dotenv`

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher installed.
* A Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ajayasauden/ai-code-reviewer.git](https://github.com/ajayasauden/ai-code-reviewer.git)
   cd ai-code-reviewer
