# Project Chewbaca - Advanced Process Automation and SQL Integration

**Chewbaca** is a Python-driven automation tool that merges advanced techniques such as process manipulation, image recognition, web scraping, and database management into a unified, flexible framework. The project demonstrates how these techniques can be applied across various software environments, focusing on adaptable and scalable solutions rather than binding users to specific platforms.

The core philosophy behind this project is *"teach a man to fish, and you will feed him for a lifetime"* — the tool provides a generalized approach to solving common automation problems, enabling you to apply these techniques in your own unique environments, whether that involves managing databases, automating web interactions, or integrating both into a seamless workflow.

---

## Key Techniques and Features

### Process Manipulation
- Direct interaction with running processes (like SSMS or other software) to perform automated tasks such as logging in, executing commands, and saving results.
- Identifies and manipulates UI elements and controls in various applications, making it adaptable to many different software environments.

### Image Recognition and GUI Automation
- Utilizes **PyAutoGUI** and image recognition to locate specific UI elements (e.g., buttons, input fields) and automate interactions.
- This eliminates dependency on hardcoded coordinates and makes the tool resilient to UI layout changes.

### Web Scraping and Interaction (Selenium)
- Uses **Selenium WebDriver** to automate web-based tasks such as logging into web applications, filling out forms, and extracting data from web pages.
- Enables the tool to interact with both desktop applications and web interfaces in the same workflow.

### Database and Webfront End Integration
- Seamlessly integrates database access and web front-end automation, enabling workflows that involve both querying a database and interacting with a web service.
- Whether you use SQL Server Management Studio or another database platform, this tool allows you to customize your automation pipeline.

### Modular Design and Customization
- The modular structure allows users to easily customize workflows. You can replace the web service or database component with your own system, while maintaining the overall automation logic.
- The tool offers many customizable options to handle different platforms, login systems, or project-specific steps without having to rewrite core functionality.

---

## Purpose and Scope

The main objective of this project is to demonstrate techniques and approaches that are applicable to a wide range of tasks. Instead of being locked into a particular software stack, Chewbaca aims to showcase how to:

- Manipulate processes and interact with applications at the OS level.
- Use image recognition for robust and adaptive UI automation.
- Integrate web scraping into a larger automation framework to handle both desktop and web-based workflows.
- Combine database access with frontend automation to streamline workflows, creating a bridge between querying data and applying it within a frontend system.

---

## Getting Started

### Prerequisites
- Python 3.x installed on your machine.
- Required Python libraries: **PyAutoGUI**, **Selenium**, **Tkinter**, and others listed in `requirements.txt`.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Chewbaca.git
    cd Chewbaca
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Optional: To create an executable for distribution**:
    ```bash
    pyinstaller Chewbaca.spec
    ```

4. **Include Necessary Assets**:
    Ensure the following assets are bundled into the executable:
    - `/docs/parsed_chewbaca.jsonl` (used for data storage)
    - Database platform images (used for GUI automation via image recognition).

---

## Usage

### Main Interface

- **Project Management**: Manage multiple projects using a clean and simple GUI. Track your progress with the *Current Step* feature, allowing you to add notes or issues as you work through each project.
- **SQL Automation**: Automatically logs into databases, saves queries, and runs SQL commands using pre-configured scripts. This includes saving queries using dynamic names (project name + random number).
- **Customizable Workflow**: Easily customize the tool to work with different databases, web applications, and front-end systems. You can modify it to log into a different web service or automate different database queries depending on your use case.

### Key Features

- **Process and Application Automation**:
  - Automatic login into any supported database platform (SQL Server, etc.) using pre-configured credentials.
  - Image-based GUI automation to interact with UI components that don’t offer traditional API access.

- **Cross-Platform Workflow**:
  - Connects both desktop and web-based systems into a single workflow.
  - Automate login, query, and data retrieval from a database while simultaneously automating a web-based frontend to apply the results.

- **Flexible Note-Taking (Current Step)**:
  - Add custom notes to track your progress on each project. Notes are stored in the `parsed_chewbaca.jsonl` file and persist across sessions, ensuring continuity of work.

- **Customizable Query Execution**:
  - Predefined SQL queries, such as:
    - Searching for system objects or tables.
    - Looking for specific columns.
    - Updating paths or parameters in the database.

---

## Key Lessons

The key takeaway from this project is not to rely on a specific tool or software for automation, but rather to master automation techniques. Learn how to interact with UIs, scrape web data, and manipulate processes. This approach gives you the flexibility to adapt the tool to any environment or software stack you may encounter.

---

Feel free to contribute, customize, and extend Chewbaca to meet your needs!
