# Socket_systematic_random_excel

Asynchronously send questions to a WebSocket server, read from an Excel file, and log responses.

This project uses **AsyncIO** and **SocketIO** to create an efficient question sender integrated with an Excel reader, allowing asynchronous query capabilities and response logging.

---

## 🚀 Features

- Asynchronously send questions using **AsyncIO** and **SocketIO**.
- Read questions from an Excel file using **Pandas**.
- Log responses and errors using **logging**.
- Calculate the total cost based on the number of requests.

---

## 🛠 Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Peeradech-Phola/Socket_systematic_random_excel.git
    cd Socket_systematic_random_excel
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

---

## 🔧 Configuration

Ensure you have the following configuration set up:

- `BASE_WEBSOCKET_URL`: The URL of the WebSocket server.
- `USERNAME`: The username to use for sending questions.
- `PROJECT`: The project name associated with the questions.
- `excel_file`: Path to the Excel file containing the questions.

---

## 🏃 Usage

1. Place your **Excel file** containing questions in the specified path.
2. Run the script:

    ```bash
    python async_question_sender.py
    ```

---

## 📚 API Endpoints

### 1. Send Question

- **Endpoint:** `/send_question`
- **Method:** `POST`
- **Request Body:**

    ```json
    {
      "question": "Your question here",
      "ref": "Reference ID"
    }
    ```

- **Response:**

    ```json
    {
      "status": "success",
      "message": "Question sent successfully"
    }
    ```

---

### 2. Get Status

- **Endpoint:** `/status`
- **Method:** `GET`
- **Response:**

    ```json
    {
      "status": "running",
      "total_questions_sent": 100,
      "total_cost": 5.00
    }
    ```

---

## 🛡 Logging

All responses and errors are logged using the **logging** module. Check the log files for detailed information on the question sending process.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/Peeradech-Phola/Socket_systematic_random_excel/issues).

---

## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **AsyncIO**
- **SocketIO**
- **Pandas**
- **readme-md-generator**
