# Agile Project Consultant

An interactive web application that helps teams determine the most suitable agile methodology and practices for their projects based on team composition, project requirements, and organizational context.

## Features

- **Interactive Chat Interface**: Engage with an AI-powered agile consultant that answers questions about agile methodologies
- **Structured Project Assessment**: Complete a guided assessment of your project needs and context
- **Personalized Recommendations**: Receive tailored methodology recommendations based on your specific project parameters
- **Best Practice Suggestions**: Get suggestions for team practices that align with your project constraints
- **Relevant Metrics**: Learn which metrics would be most valuable to track for your particular context
- **Conversation History**: Review and save your consultation for future reference

## Screenshot

*[Add a screenshot of the application interface here]*

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agile-project-consultant.git
   cd agile-project-consultant
   ```

2. Install the required dependencies:
   ```bash
   pip install flask
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage Guide

### Starting a Consultation

1. When you first open the application, the consultant will greet you and offer to help determine the best agile methodology for your project.

2. You can either:
   - Click the "Start Assessment" button to begin a structured assessment
   - Type questions directly in the chat input field to get immediate answers about specific agile topics

### Completing the Assessment

1. The assessment consists of 10 questions about your project context, including:
   - Team size and experience
   - Project complexity and duration
   - Requirements stability
   - Stakeholder involvement
   - Project constraints
   - Team distribution

2. Answer each question based on your specific project situation.

3. Click "Submit Assessment" when you've completed all questions.

### Viewing Recommendations

After submitting the assessment, you'll receive tailored recommendations that include:

- A recommended agile methodology (Scrum, Kanban, XP, or a hybrid approach)
- Justification for why the methodology was selected for your context
- Key team practices that would benefit your specific situation
- Important metrics to track for your project constraints

### Asking Additional Questions

You can continue the conversation by asking follow-up questions about:

- Comparing different methodologies
- Implementation details for specific practices
- How to adapt agile for your unique situation
- Common challenges and solutions
- Estimation techniques
- Remote/distributed team considerations
- Useful metrics and measurements

### Saving Your Consultation

1. Click the "Save Conversation" button to save the entire consultation.
2. Enter a filename when prompted.
3. The consultation will be saved as a JSON file that includes:
   - The full conversation history
   - Your project context information
   - The generated recommendations

## Project Structure

```
agile-project-consultant/
├── app.py                # Flask application with routes and web interface
├── agile_consultant.py   # Core logic for the agile consultant agent
└── templates/            # (Auto-generated) Contains the HTML template
    └── index.html        # Web interface template
```

## Customization
### Adding New Questions
To add new assessment questions, edit the `assessment_questions` list in the `__init__` method of the `AgileProjectConsultant` class in `agile_consultant.py`.

### Extending Recommendation Logic
The recommendation logic can be extended by modifying the `_recommend_methodology()`, `_recommend_practices()`, and `_recommend_metrics()` methods in the `AgileProjectConsultant` class.

### Enhancing the Knowledge Base
To improve the consultant's ability to answer free-text questions, add new keyword patterns and responses in the `process_free_text_query()` method.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- This project was inspired by the need for accessible agile guidance for teams new to agile methodologies
