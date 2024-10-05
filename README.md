# Auto Submission for toph.co

This repository contains python script for automating the submission of problems on the toph.co platform. Below are the demonstration GIFs of the functionality.

![1](https://github.com/greatzero728/241004-zero-Integration-of-auto-submission-for-Toph-in-Acade/blob/main/Final%20Result/gif/1.gif)
![2](https://github.com/greatzero728/241004-zero-Integration-of-auto-submission-for-Toph-in-Acade/blob/main/Final%20Result/gif/2.gif)
![3](https://github.com/greatzero728/241004-zero-Integration-of-auto-submission-for-Toph-in-Acade/blob/main/Final%20Result/gif/3.gif)
![4](https://github.com/greatzero728/241004-zero-Integration-of-auto-submission-for-Toph-in-Acade/blob/main/Final%20Result/gif/4.gif)
![5](https://github.com/greatzero728/241004-zero-Integration-of-auto-submission-for-Toph-in-Acade/blob/main/Final%20Result/gif/5.gif)
![6](https://github.com/greatzero728/241004-zero-Integration-of-auto-submission-for-Toph-in-Acade/blob/main/Final%20Result/gif/6.gif)

## Overview of the Code

### 1. `getProblemList.py`

This script scrapes all problem URLs from the toph.co site and saves them to a file named `problemList.txt`. It uses the `requests` library for HTTP requests and BeautifulSoup for parsing HTML content.

### 2. `autoSubmitToToph.py`

This script defines three main functions for automating the submission process:
- **`login()`**: Logs into toph.co using credentials stored in a `.env` file.
- **`submit(problem_id: str, code: str)`**: Submits the provided code to the corresponding problem URL and returns the submission ID.
- **`get_status(submission_id)`**: Retrieves the current status of the submission identified by the given submission ID.

### 3. `test.py`

This script tests the three functions defined in `autoSubmitToToph.py`. It first logs in and then opens a GUI window. Users can input the problem name and code to receive a submission ID. If a submission ID is provided, the script returns the status of that submission.

## Environment Setup

1. **Python Installation**: Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

2. **Pip Installation**: If `pip` is not installed, download the `get-pip.py` file from [here](https://bootstrap.pypa.io/get-pip.py) and execute it using:
   ```bash
   python get-pip.py
   ```

3. **Install Required Modules**: Use `pip` to install the necessary libraries:
   ```bash
   pip install requests beautifulsoup4 selenium python-dotenv
   ```

4. **Set Up Environment Variables**: Create a `.env` file in the root directory of the project with the following content:
   ```
   TOPH_USERNAME=your_username
   TOPH_PASSWORD=your_password
   WAIT_TIME=10
   ```

5. **Running the Scripts**: Execute the scripts as needed:
   ```bash
   python getProblemList.py
   python autoSubmitToToph.py
   python test.py
   ```

## Conclusion

This project aims to streamline the process of problem submission on toph.co, making it easier for users to participate in competitive programming challenges.