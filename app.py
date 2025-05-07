from flask import Flask, request, jsonify, render_template, session
import os
import json
import logging  # Added for debug logging
from agile_consultant import AgileProjectConsultant  # Import the updated agent class

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure key for session management

# Initialize the consultant with error handling
try:
    consultant = AgileProjectConsultant()
    logging.info("AgileProjectConsultant initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize AgileProjectConsultant: {str(e)}")
    raise

@app.route('/')
def index():
    """Render the main web interface with initial context."""
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
        session['context'] = {}  # Store project context in session
    return render_template('index.html')

@app.route('/api/start', methods=['GET'])
def start_conversation():
    """Start a new conversation with a tailored greeting."""
    session_id = session.get('session_id', os.urandom(16).hex())
    session['session_id'] = session_id
    session['context'] = {}  # Reset context on new conversation
    consultant.project_context = {}  # Sync consultant context
    try:
        greeting = consultant.start_conversation()
        logging.info("Conversation started successfully")
    except Exception as e:
        logging.error(f"Failed to start conversation: {str(e)}")
        return jsonify({'error': f'Failed to start conversation: {str(e)}'}), 500
    return jsonify({
        'session_id': session_id,
        'message': greeting,
        'next_step': 'assessment',
        'context': session['context']
    })

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Retrieve assessment questions, ensuring all are returned."""
    try:
        questions = consultant.collect_project_context()
        logging.debug(f"Retrieved {len(questions)} questions")
        if not questions:
            logging.warning("No questions returned from collect_project_context")
            return jsonify({
                'error': 'No questions available. Please try restarting the conversation.'
            }), 500
        return jsonify({
            'questions': questions,
            'message': 'Please answer the following questions to receive tailored recommendations.'
        })
    except Exception as e:
        logging.error(f"Failed to load questions: {str(e)}")
        return jsonify({
            'error': f'Failed to load questions: {str(e)}'
        }), 500

@app.route('/api/submit_assessment', methods=['POST'])
def submit_assessment():
    """Process assessment answers and return detailed recommendations."""
    try:
        data = request.json
        if not data or not isinstance(data, dict):
            logging.warning("Invalid or empty assessment data")
            return jsonify({
                'error': 'Invalid or empty assessment data provided.'
            }), 400

        # Validate and process answers
        for question_id, answer in data.items():
            if answer is None or (isinstance(answer, list) and not answer):
                logging.warning(f"Empty answer for {question_id}")
                return jsonify({
                    'error': f'Answer for {question_id} cannot be empty.'
                }), 400
            consultant.process_user_input(question_id, answer)
            session['context'][question_id] = answer  # Store in session

        # Sync consultant.project_context with session['context']
        consultant.project_context = session['context'].copy()
        logging.debug(f"Updated project_context: {consultant.project_context}")

        # Generate recommendations
        recommendations = consultant.generate_full_recommendations()
        
        # Format a detailed summary
        methodology = recommendations['methodology']['name']
        team_size = session['context'].get('team_size', 'your team')
        challenges = session['context'].get('challenges', [])
        summary = (
            f"For {team_size}, I recommend {methodology} to address {', '.join(challenges[:2] if challenges else ['your needs'])}. "
            f"Focus on practices like {', '.join([p['practice'] for p in recommendations['team_practices'][:2]])} "
            f"and track metrics like {', '.join([m['metric'] for m in recommendations['metrics'][:2]])}."
        )

        return jsonify({
            'recommendations': recommendations,
            'message': summary,
            'next_step': 'Ask specific questions about practices or challenges for further guidance.'
        })
    except Exception as e:
        logging.error(f"Failed to process assessment: {str(e)}")
        return jsonify({
            'error': f'Failed to process assessment: {str(e)}'
        }), 500

@app.route('/api/query', methods=['POST'])
def process_query():
    """Handle free-text queries with context-specific responses."""
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            logging.warning("Empty query received")
            return jsonify({
                'error': 'Query cannot be empty.',
                'suggestions': [
                    'How do I set up a Kanban board for my team?',
                    'How can I improve team engagement?',
                    'What metrics should I track for Kanban?'
                ]
            }), 400
        
        response = consultant.process_free_text_query(query)
        logging.debug(f"Processed query: {query}")
        
        # Add context-aware suggestions
        suggestions = []
        if 'challenges' in session['context']:
            challenges = session['context']['challenges']
            if 'Resistance to change' in challenges:
                suggestions.append('How can I reduce resistance to Kanban practices?')
            if 'Lack of engagement' in challenges:
                suggestions.append('How can I improve team engagement with daily standups?')
        if session['context'].get('current_methodology', '').lower() == 'kanban':
            suggestions.extend([
                'How do I set up a Kanban board?',
                'What are best practices for WIP limits?'
            ])
        
        return jsonify({
            'response': response,
            'suggestions': suggestions,
            'message': 'Here’s my advice. Try these follow-up questions for more details.'
        })
    except Exception as e:
        logging.error(f"Failed to process query: {str(e)}")
        return jsonify({
            'error': f'Failed to process query: {str(e)}'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Return conversation history with formatted summary."""
    try:
        history = consultant.get_conversation_history()
        context_summary = (
            f"Team: {session['context'].get('team_size', 'unknown')}\n"
            f"Methodology: {session['context'].get('current_methodology', 'unknown')}\n"
            f"Challenges: {', '.join(session['context'].get('challenges', ['none']))}\n"
            f"Goals: {', '.join(session['context'].get('goals', ['none']))}"
        )
        formatted_history = [
            {'role': msg['role'], 'content': msg['content'].replace('\n', '; ')}
            for msg in history
        ]
        logging.debug(f"Retrieved history with {len(formatted_history)} messages")
        return jsonify({
            'history': formatted_history,
            'context': context_summary,
            'message': 'Conversation history retrieved. Ask a question or review your assessment.'
        })
    except Exception as e:
        logging.error(f"Failed to retrieve history: {str(e)}")
        return jsonify({
            'error': f'Failed to retrieve history: {str(e)}'
        }), 500

@app.route('/api/save_conversation', methods=['POST'])
def save_conversation():
    """Save conversation to a file with validation."""
    try:
        data = request.json
        file_path = data.get('file_path', 'conversation.json').strip()
        
        if not file_path.endswith('.json'):
            file_path += '.json'
        if not file_path:
            logging.warning("Empty file path provided")
            return jsonify({
                'error': 'File path cannot be empty.'
            }), 400
        
        consultant.save_conversation(file_path)
        logging.info(f"Conversation saved to {file_path}")
        
        return jsonify({
            'success': True,
            'message': f'Conversation successfully saved to {file_path}.',
            'file_path': file_path
        })
    except Exception as e:
        logging.error(f"Failed to save conversation: {str(e)}")
        return jsonify({
            'error': f'Failed to save conversation: {str(e)}'
        }), 500

@app.route('/api/context', methods=['GET'])
def get_context():
    """Debug route to inspect session and consultant context."""
    try:
        logging.debug("Fetching context for debugging")
        return jsonify({
            'session_context': session.get('context', {}),
            'consultant_context': consultant.project_context
        })
    except Exception as e:
        logging.error(f"Failed to fetch context: {str(e)}")
        return jsonify({
            'error': f'Failed to fetch context: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Create templates directory and write index.html
    templates_dir = 'templates'
    try:
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        
        index_path = os.path.join(templates_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Agile Project Consultant</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .chat-container {
            height: 500px;
            overflow-y: auto;
            border: 1px solid #dee2e6;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 8px;
            background-color: #fff;
        }
        .agent-message {
            background-color: #e9f5ff;
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 10px;
            max-width: 85%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .user-message {
            background-color: #d4edda;
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 10px;
            max-width: 85%;
            margin-left: auto;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .assessment-container {
            margin-top: 20px;
            border: 1px solid #dee2e6;
            padding: 20px;
            border-radius: 8px;
            background-color: #fff;
        }
        .suggestions {
            margin-top: 10px;
            font-style: italic;
            color: #6c757d;
        }
        .recommendation-box {
            background-color: #f1f3f5;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Agile Project Consultant</h1>
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="chat-container" id="chatContainer"></div>
                <div class="input-group mb-4">
                    <input type="text" id="userInput" class="form-control" placeholder="Ask about Kanban practices, challenges, or metrics...">
                    <button class="btn btn-primary" id="sendBtn">Send</button>
                </div>
                <div id="assessmentContainer" class="assessment-container d-none">
                    <h3>Project Assessment</h3>
                    <p>Answer these questions to receive tailored agile recommendations.</p>
                    <div id="questionsContainer"></div>
                    <button class="btn btn-success mt-3" id="submitAssessmentBtn">Submit Assessment</button>
                </div>
                <div class="d-flex justify-content-between mt-4">
                    <button class="btn btn-secondary" id="startAssessmentBtn">Start Assessment</button>
                    <button class="btn btn-info" id="saveConversationBtn">Save Conversation</button>
                    <button class="btn btn-outline-secondary" id="viewHistoryBtn">View History</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let sessionId = null;
        let questionsData = null;
        let assessmentAnswers = {};

        // DOM elements
        const chatContainer = document.getElementById('chatContainer');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const assessmentContainer = document.getElementById('assessmentContainer');
        const questionsContainer = document.getElementById('questionsContainer');
        const submitAssessmentBtn = document.getElementById('submitAssessmentBtn');
        const startAssessmentBtn = document.getElementById('startAssessmentBtn');
        const saveConversationBtn = document.getElementById('saveConversationBtn');
        const viewHistoryBtn = document.getElementById('viewHistoryBtn');

        // Initialize conversation
        window.addEventListener('load', startConversation);

        // Start a new conversation
        function startConversation() {
            fetch('/api/start')
                .then(response => response.json())
                .then(data => {
                    sessionId = data.session_id;
                    addMessage('agent', data.message);
                })
                .catch(error => {
                    console.error('Error starting conversation:', error);
                    addMessage('agent', 'Failed to start conversation. Please refresh the page.');
                });
        }

        // Add a message to the chat container
        function addMessage(role, content, suggestions = []) {
            const messageDiv = document.createElement('div');
            messageDiv.className = role === 'user' ? 'user-message' : 'agent-message';
            messageDiv.innerHTML = content.replace(/\n/g, '<br>');
            chatContainer.appendChild(messageDiv);
            if (suggestions.length) {
                const suggDiv = document.createElement('div');
                suggDiv.className = 'suggestions';
                suggDiv.textContent = 'Suggestions: ' + suggestions.join(' | ');
                messageDiv.appendChild(suggDiv);
            }
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Load assessment questions
        function loadQuestions() {
            fetch('/api/questions')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        addMessage('agent', data.error);
                        return;
                    }
                    questionsData = data.questions;
                    addMessage('agent', data.message);
                    renderQuestions();
                    assessmentContainer.classList.remove('d-none');
                })
                .catch(error => {
                    console.error('Error loading questions:', error);
                    addMessage('agent', 'Failed to load questions. Please try again.');
                });
        }

        // Render questions
        function renderQuestions() {
            questionsContainer.innerHTML = '';
            questionsData.forEach(question => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'mb-4';
                
                const label = document.createElement('label');
                label.className = 'form-label fw-bold';
                label.textContent = question.question;
                questionDiv.appendChild(label);
                
                if (question.type === 'text') {
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.className = 'form-control';
                    input.id = question.id;
                    input.required = true;
                    input.addEventListener('input', (e) => {
                        assessmentAnswers[question.id] = e.target.value.trim();
                    });
                    questionDiv.appendChild(input);
                } else if (question.type === 'select') {
                    const select = document.createElement('select');
                    select.className = 'form-select';
                    select.id = question.id;
                    select.required = true;
                    const defaultOption = document.createElement('option');
                    defaultOption.value = '';
                    defaultOption.textContent = 'Select an option';
                    defaultOption.disabled = true;
                    defaultOption.selected = true;
                    select.appendChild(defaultOption);
                    question.options.forEach(option => {
                        const optionEl = document.createElement('option');
                        optionEl.value = option;
                        optionEl.textContent = option;
                        select.appendChild(optionEl);
                    });
                    select.addEventListener('change', (e) => {
                        assessmentAnswers[question.id] = e.target.value;
                    });
                    questionDiv.appendChild(select);
                } else if (question.type === 'multi-select') {
                    const checkContainer = document.createElement('div');
                    checkContainer.className = 'mt-2';
                    question.options.forEach(option => {
                        const checkDiv = document.createElement('div');
                        checkDiv.className = 'form-check';
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.className = 'form-check-input';
                        checkbox.id = `${question.id}_${option.replace(/\s/g, '_')}`;
                        checkbox.value = option;
                        checkbox.addEventListener('change', (e) => {
                            assessmentAnswers[question.id] = assessmentAnswers[question.id] || [];
                            if (e.target.checked) {
                                assessmentAnswers[question.id].push(option);
                            } else {
                                assessmentAnswers[question.id] = assessmentAnswers[question.id].filter(item => item !== option);
                            }
                        });
                        const checkLabel = document.createElement('label');
                        checkLabel.className = 'form-check-label';
                        checkLabel.htmlFor = checkbox.id;
                        checkLabel.textContent = option;
                        checkDiv.appendChild(checkbox);
                        checkDiv.appendChild(checkLabel);
                        checkContainer.appendChild(checkDiv);
                    });
                    questionDiv.appendChild(checkContainer);
                }
                
                questionsContainer.appendChild(questionDiv);
            });
        }

        // Submit assessment
        function submitAssessment() {
            if (Object.keys(assessmentAnswers).length !== questionsData.length) {
                addMessage('agent', 'Please answer all questions before submitting.');
                return;
            }
            fetch('/api/submit_assessment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(assessmentAnswers)
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    addMessage('agent', data.error);
                    return;
                }
                addMessage('agent', data.message);
                const rec = data.recommendations;
                const recHtml = `
                    <div class="recommendation-box">
                        <h4>${rec.methodology.name} Recommendation</h4>
                        <p><strong>Why:</strong> ${rec.methodology.why_recommended}</p>
                        <p><strong>Key Practices:</strong> ${rec.team_practices.map(p => p.practice).join(', ')}</p>
                        <p><strong>Metrics:</strong> ${rec.metrics.map(m => m.metric).join(', ')}</p>
                        <p><strong>Challenges Addressed:</strong> ${rec.challenges.map(c => `${c.challenge}: ${c.recommendations[0]}`).join('; ')}</p>
                        <p><strong>Tools:</strong> ${rec.tools.map(t => t.recommendation).join(', ')}</p>
                    </div>
                `;
                addMessage('agent', recHtml);
                assessmentContainer.classList.add('d-none');
                addMessage('agent', data.next_step);
            })
            .catch(error => {
                console.error('Error submitting assessment:', error);
                addMessage('agent', 'Failed to submit assessment. Please try again.');
            });
        }

        // Send a query
        function sendQuery(query) {
            addMessage('user', query);
            fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    addMessage('agent', data.error, data.suggestions || []);
                    return;
                }
                addMessage('agent', data.response, data.suggestions);
                addMessage('agent', data.message);
            })
            .catch(error => {
                console.error('Error sending query:', error);
                addMessage('agent', 'Failed to process query. Please try again.');
            });
        }

        // Save conversation
        function saveConversation() {
            const filename = prompt('Enter a filename (e.g., kanban_advice.json):', 'agile_consultation.json');
            if (filename) {
                fetch('/api/save_conversation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ file_path: filename })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        addMessage('agent', data.error);
                    } else {
                        addMessage('agent', data.message);
                    }
                })
                .catch(error => {
                    console.error('Error saving conversation:', error);
                    addMessage('agent', 'Failed to save conversation. Please try again.');
                });
            }
        }

        // View conversation history
        function viewHistory() {
            fetch('/api/history')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        addMessage('agent', data.error);
                        return;
                    }
                    addMessage('agent', `Context:\n${data.context}`);
                    data.history.forEach(msg => {
                        addMessage(msg.role, msg.content.replace('; ', '\n'));
                    });
                    addMessage('agent', data.message);
                })
                .catch(error => {
                    console.error('Error retrieving history:', error);
                    addMessage('agent', 'Failed to retrieve history. Please try again.');
                });
        }

        // Event listeners
        sendBtn.addEventListener('click', () => {
            const query = userInput.value.trim();
            if (query) {
                sendQuery(query);
                userInput.value = '';
            }
        });

        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendBtn.click();
            }
        });

        startAssessmentBtn.addEventListener('click', loadQuestions);
        submitAssessmentBtn.addEventListener('click', submitAssessment);
        saveConversationBtn.addEventListener('click', saveConversation);
        viewHistoryBtn.addEventListener('click', viewHistory);
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
            ''')
    except Exception as e:
        logging.error(f"Error creating templates/index.html: {str(e)}")
        raise

    # Run the app
    app.run(debug=True, port=5001)