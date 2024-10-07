Project Chewbaca - Advanced Process Automation and SQL Integration
Chewbaca is a Python-driven automation tool that merges various advanced techniques like process manipulation, image recognition, web scraping, and database management into a unified, flexible framework. The project demonstrates how these techniques can be applied across various software environments, focusing on adaptable and scalable solutions rather than binding users to specific platforms.

The core philosophy behind this project is "teach a man to fish, and you will feed him for a lifetime" — the tool provides a generalized approach to solving common automation problems, enabling you to apply these techniques to your own unique environments, whether that involves managing databases, automating web interactions, or integrating both into a seamless workflow.

Key Techniques and Features
Process Manipulation:

Direct interaction with running processes (like SSMS or other software) to perform automated tasks like logging in, executing commands, and saving results. The tool identifies and manipulates UI elements and controls in other applications, making it adaptable to many different software environments.
Image Recognition and GUI Automation:

Utilizes PyAutoGUI and image recognition to locate specific UI elements (e.g., buttons or input fields) and automate interactions. This approach eliminates the dependency on hardcoded coordinates and makes the tool resilient to UI layout changes.
Web Scraping and Interaction (Selenium):

Uses Selenium WebDriver to automate web-based tasks, such as logging into web applications, filling out forms, or extracting data from web pages. This capability allows the tool to interact with both desktop applications and web interfaces in the same workflow.
Database and Webfront End Integration:

The project seamlessly integrates database access and webfront-end automation, enabling automated workflows that involve both querying a database and interacting with a web service. Whether you use SQL Server Management Studio or another database platform, this tool allows you to customize your automation pipeline.
Modular Design and Customization:

The modular structure allows users to easily customize workflows. For example, you can replace the web service or database component with your own system, while maintaining the overall automation logic.
The tool is designed to be flexible, offering many customizable options to handle different platforms, login systems, or even project-specific steps without having to rewrite core functionality.
Purpose and Scope
The main objective of this project is to demonstrate techniques and approaches that are applicable to a wide range of tasks. Instead of being locked into a particular software stack, Chewbaca aims to showcase how:

You can manipulate processes and interact with applications at the OS level.
Image recognition can be used for UI automation in a robust and adaptive manner.
Web scraping can be integrated into a larger automation framework for handling both desktop and web-based workflows.
How combining database access with frontend automation can streamline your workflow, creating a bridge between querying data and applying it within a frontend system.
Getting Started
Prerequisites
Python 3.x installed on your machine.
PyAutoGUI, Selenium, Tkinter, and other libraries mentioned in requirements.txt.


**Installation**
Clone the repository:
git clone https://github.com/yourusername/Chewbaca.git
cd Chewbaca
**Install dependencies:**
pip install -r requirements.txt
**Optional: To create an executable file for distribution:**
pyinstaller Chewbaca.spec

Include Necessary Assets: Ensure that the following assets are bundled into the executable:
/docs/parsed_chewbaca.jsonl (used for data storage)
database platform images (used for GUI automation via image recognition).


--------------------------------------------------------------------


Usage
Main Interface
Project Management:

Manage multiple projects using a clean and simple GUI. Track your progress with the Current Step feature, allowing you to add notes or issues as you work through each project.
SQL Automation:

Automatically logs into databases, saves queries, and runs SQL commands using pre-configured scripts. This includes automatically saving queries using dynamic names (project name + random number).
Customizable Workflow:

The tool can be easily customized to work with different databases, web applications, and front-end systems. For example, you can modify the project to log into a different web service or automate different database queries depending on your use case.
Key Features
Process and Application Automation:

Automatic login into any supported database platform (SQL Server, etc.) using the configured credentials.
Image-based GUI automation to interact with UI components that don’t offer traditional API access.
Cross-Platform Workflow:

Connects both desktop and web-based systems into a single workflow. Automate login, query, and data retrieval from a database while simultaneously automating a web-based frontend to apply the results.
Flexible Note-Taking (Current Step):

Add custom notes to track your progress on each project. The notes are stored in the parsed_chewbaca.jsonl file, and will persist across sessions, ensuring continuity of work.
Customizable Query Execution:

Predefined SQL queries, such as:
Searching for system objects or tables
Looking for specific columns
Updating paths or parameters in the database.
Key Lessons
The key takeaway from this project is not to rely on a specific tool or software for automation but rather to master the techniques of automation — learning how to interact with UIs, scrape web data, and manipulate processes. This approach gives you the flexibility to adapt the tool to any environment or software stack you may encounter.
