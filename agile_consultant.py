import json
from typing import Dict, List, Optional, Union
import random

class AgileProjectConsultant:
    """
    Main class for the Agile Project Consultant AI agent, providing tailored agile recommendations.
    """
    
    def __init__(self):
        """Initialize the agent with expanded knowledge bases and conversation history."""
        self.conversation_history = []
        self.project_context = {}
        self.knowledge_base = self._load_knowledge_base()
        
    def _load_knowledge_base(self) -> Dict:
        """Load an expanded knowledge base with detailed agile methodologies, practices, and metrics."""
        return {
            "methodologies": {
                "scrum": {
                    "description": "A framework for iterative development with fixed sprints and defined roles.",
                    "best_for": ["teams of 3-9 members", "complex products", "dynamic requirements"],
                    "ceremonies": ["Sprint Planning", "Daily Standup", "Sprint Review", "Sprint Retrospective"],
                    "roles": ["Product Owner", "Scrum Master", "Development Team"],
                    "artifacts": ["Product Backlog", "Sprint Backlog", "Increment"],
                    "challenges_addressed": ["scope creep", "meeting deadlines", "poor communication"],
                    "implementation_tips": [
                        "Start with 2-week sprints for balance.",
                        "Train the Scrum Master to facilitate effectively.",
                        "Use a digital tool like Jira for backlog management."
                    ]
                },
                "kanban": {
                    "description": "A visual workflow method emphasizing continuous delivery and flow.",
                    "best_for": ["small teams", "support/operations", "unpredictable workflows"],
                    "principles": ["Visualize workflow", "Limit work in progress", "Manage flow", "Explicit policies"],
                    "practices": ["Kanban board", "WIP limits", "Continuous delivery", "Feedback loops"],
                    "challenges_addressed": ["poor communication", "lack of engagement", "inconsistent estimation"],
                    "implementation_tips": [
                        "Design a Kanban board with 3-5 columns reflecting your workflow.",
                        "Set WIP limits to 2-3 tasks per column initially.",
                        "Review flow weekly to optimize throughput."
                    ]
                },
                "xp": {
                    "description": "A methodology focused on engineering practices for high-quality software.",
                    "best_for": ["medium teams", "complex code bases", "quality-driven projects"],
                    "practices": ["Pair Programming", "Test-Driven Development", "Continuous Integration", "Simple Design", "Refactoring"],
                    "challenges_addressed": ["quality issues", "resistance to change", "lack of engagement"],
                    "implementation_tips": [
                        "Start TDD with a single module to demonstrate value.",
                        "Rotate pairs weekly to spread knowledge.",
                        "Automate CI pipelines with tools like Jenkins."
                    ]
                },
                "lean": {
                    "description": "A method to maximize value by minimizing waste and optimizing processes.",
                    "best_for": ["any team size", "efficiency-focused organizations", "process improvement"],
                    "principles": ["Eliminate waste", "Build quality in", "Create knowledge", "Defer commitment", "Deliver fast"],
                    "challenges_addressed": ["reduced costs", "inconsistent estimation", "stakeholder management"],
                    "implementation_tips": [
                        "Map your value stream to identify waste.",
                        "Implement pull systems to avoid overproduction.",
                        "Use A/B testing for process experiments."
                    ]
                }
            },
            "common_challenges": {
                "resistance_to_change": {
                    "strategies": [
                        "Demonstrate small wins with pilot projects.",
                        "Educate on benefits with real-world examples.",
                        "Involve team in process design for ownership.",
                        "Address concerns in retrospectives with action plans."
                    ],
                    "xp_specific": [
                        "Use Pair Programming to build trust and reduce resistance.",
                        "Show TDD’s impact on reducing defects early."
                    ],
                    "kanban_specific": [
                        "Use a Kanban board to visualize progress, easing transition concerns.",
                        "Start with low WIP limits to show quick wins."
                    ]
                },
                "lack_of_engagement": {
                    "strategies": [
                        "Connect tasks to the product vision for purpose.",
                        "Rotate roles to maintain interest.",
                        "Celebrate milestones with team recognition.",
                        "Encourage innovation through hackathons or experiments."
                    ],
                    "xp_specific": [
                        "Rotate pairs in Pair Programming to foster collaboration.",
                        "Use TDD to give developers immediate feedback, boosting engagement."
                    ],
                    "kanban_specific": [
                        "Involve the team in designing the Kanban board for ownership.",
                        "Use daily standups to encourage participation."
                    ]
                },
                "poor_communication": {
                    "strategies": [
                        "Establish clear team agreements on communication channels.",
                        "Use visual tools like Kanban boards or burndown charts.",
                        "Timebox ceremonies to keep discussions focused.",
                        "Implement daily check-ins for alignment."
                    ],
                    "xp_specific": [
                        "Leverage Pair Programming for real-time communication.",
                        "Use Continuous Integration feedback to align on code quality."
                    ],
                    "kanban_specific": [
                        "Use the Kanban board as an information radiator for transparency.",
                        "Review board updates in daily standups to align the team."
                    ]
                },
                "inconsistent_estimation": {
                    "strategies": [
                        "Use story points and Planning Poker for consensus.",
                        "Maintain a reference backlog for sizing consistency.",
                        "Review past estimates in retrospectives.",
                        "Break tasks into smaller, estimable units."
                    ],
                    "xp_specific": [
                        "Estimate tasks collaboratively during TDD planning.",
                        "Use Simple Design to keep tasks small and predictable."
                    ]
                },
                "scope_creep": {
                    "strategies": [
                        "Prioritize backlog items with stakeholders regularly.",
                        "Define strict 'Done' criteria for each task.",
                        "Implement a change request process.",
                        "Educate stakeholders on trade-offs of adding scope."
                    ],
                    "xp_specific": [
                        "Use TDD to ensure new features meet quality standards.",
                        "Refactor code to accommodate changes without technical debt."
                    ]
                },
                "quality_issues": {
                    "strategies": [
                        "Implement automated testing suites.",
                        "Conduct code reviews before merging.",
                        "Define quality metrics like defect rates.",
                        "Train team on best practices."
                    ],
                    "xp_specific": [
                        "Adopt TDD to catch defects early.",
                        "Use Continuous Integration to ensure code stability."
                    ]
                },
                "meeting_deadlines": {
                    "strategies": [
                        "Break work into smaller iterations.",
                        "Track velocity to predict delivery.",
                        "Remove blockers promptly in daily standups.",
                        "Negotiate scope with stakeholders."
                    ],
                    "xp_specific": [
                        "Use TDD to reduce rework, speeding up delivery.",
                        "Implement Continuous Integration for faster feedback."
                    ],
                    "kanban_specific": [
                        "Optimize flow with WIP limits to meet deadlines.",
                        "Track Cycle Time to identify delays early."
                    ]
                },
                "stakeholder_management": {
                    "strategies": [
                        "Schedule regular stakeholder reviews.",
                        "Use demos to align on expectations.",
                        "Create transparent progress dashboards.",
                        "Train team on stakeholder communication."
                    ],
                    "xp_specific": [
                        "Show TDD test results to stakeholders for quality assurance.",
                        "Use Simple Design to explain technical decisions clearly."
                    ]
                }
            },
            "metrics": {
                "velocity": {
                    "description": "Measures work completed per iteration, useful for predicting capacity.",
                    "how_to_measure": "Sum story points completed per sprint.",
                    "best_for": ["scrum"],
                    "implementation_tips": [
                        "Track over 3-5 sprints for stability.",
                        "Adjust estimates if velocity fluctuates widely."
                    ]
                },
                "cycle_time": {
                    "description": "Time from starting a task to its completion, indicating efficiency.",
                    "how_to_measure": "Average time from 'In Progress' to 'Done' in days/hours.",
                    "best_for": ["kanban", "xp", "lean"],
                    "implementation_tips": [
                        "Use tools like Jira for automatic tracking.",
                        "Aim for consistent Cycle Times (e.g., 1-3 days)."
                    ]
                },
                "lead_time": {
                    "description": "Time from task request to delivery, showing responsiveness.",
                    "how_to_measure": "Average time from backlog entry to completion.",
                    "best_for": ["kanban", "xp", "lean"],
                    "implementation_tips": [
                        "Break tasks into smaller units to reduce Lead Time.",
                        "Review weekly to identify delays."
                    ]
                },
                "defect_rate": {
                    "description": "Number of bugs found post-release, indicating quality.",
                    "how_to_measure": "Bugs per feature or per sprint, tracked in a bug system.",
                    "best_for": ["xp", "quality focus"],
                    "implementation_tips": [
                        "Use automated tests to catch defects early.",
                        "Target <1 bug per feature."
                    ]
                },
                "team_happiness": {
                    "description": "Team satisfaction and engagement, critical for retention.",
                    "how_to_measure": "Survey team (1-5 scale) biweekly or monthly.",
                    "best_for": ["all methodologies"],
                    "implementation_tips": [
                        "Use anonymous surveys for honest feedback.",
                        "Act on results in retrospectives."
                    ]
                }
            },
            "team_sizes": {
                "small": {
                    "range": "1-5 members",
                    "recommendations": [
                        "Use Kanban or simplified Scrum for flexibility.",
                        "Combine roles (e.g., Product Owner/Scrum Master).",
                        "Keep ceremonies short (10-15 minutes).",
                        "Encourage generalist skills."
                    ],
                    "xp_tips": [
                        "Pair Programming can double as mentoring.",
                        "TDD suits small teams for quick quality checks."
                    ]
                },
                "medium": {
                    "range": "6-12 members",
                    "recommendations": [
                        "Adopt Scrum or XP with dedicated roles.",
                        "Balance specialists and generalists.",
                        "Use regular ceremonies for alignment.",
                        "Track metrics like velocity or defect rate."
                    ],
                    "xp_tips": [
                        "Rotate pairs to spread expertise.",
                        "Use CI tools to manage larger codebases."
                    ]
                },
                "large": {
                    "range": "13+ members",
                    "recommendations": [
                        "Scale with Scrum of Scrums or SAFe.",
                        "Define clear inter-team dependencies.",
                        "Standardize processes across teams.",
                        "Foster communities of practice."
                    ],
                    "xp_tips": [
                        "Apply TDD at the module level.",
                        "Use CI/CD for cross-team integration."
                    ]
                }
            }
        }
    
    def start_conversation(self) -> str:
        """Initiate a conversation with a tailored greeting based on context."""
        if self.project_context:
            team_size = self.project_context.get("team_size", "your team")
            methodology = self.project_context.get("current_methodology", "agile practices")
            greeting = (
                f"Welcome back! I'm here to help {team_size} optimize {methodology}. "
                f"Based on your context, I can suggest specific practices or answer questions. "
                f"Try asking about a challenge or practice, or click 'Start Assessment' for new recommendations."
            )
        else:
            greeting = (
                "Welcome to your Agile Project Consultant! I’ll help you implement or improve agile practices. "
                "To get started, click 'Start Assessment' to share your team’s context, or ask a specific question "
                "about agile methodologies, practices, or challenges."
            )
        self.conversation_history.append({"role": "agent", "content": greeting})
        return greeting
    
    def collect_project_context(self) -> List[Dict]:
        """Return a comprehensive set of questions to gather detailed project context."""
        questions = [
            {
                "id": "team_size",
                "question": "How large is your team?",
                "type": "select",
                "options": ["1-5 members", "6-12 members", "13+ members"]
            },
            {
                "id": "industry",
                "question": "What industry are you in? (e.g., IT, Finance, Healthcare)",
                "type": "text"
            },
            {
                "id": "current_methodology",
                "question": "Which agile methodology are you currently using?",
                "type": "select",
                "options": ["None/Traditional", "Scrum", "Kanban", "XP", "Lean", "Hybrid", "Other"]
            },
            {
                "id": "experience_level",
                "question": "What is your team's experience level with agile practices?",
                "type": "select",
                "options": ["Beginner", "Intermediate", "Advanced"]
            },
            {
                "id": "challenges",
                "question": "What challenges are you facing? (Select all that apply)",
                "type": "multi-select",
                "options": [
                    "Resistance to change",
                    "Inconsistent estimation",
                    "Scope creep",
                    "Poor communication",
                    "Lack of engagement",
                    "Meeting deadlines",
                    "Quality issues",
                    "Stakeholder management"
                ]
            },
            {
                "id": "goals",
                "question": "What are your primary goals for improving your process? (Select all that apply)",
                "type": "multi-select",
                "options": [
                    "Faster delivery",
                    "Higher quality",
                    "Better predictability",
                    "Team satisfaction",
                    "Reduced costs",
                    "Better customer collaboration",
                    "More innovation"
                ]
            },
            {
                "id": "project_complexity",
                "question": "How complex is your project? (e.g., simple, moderate, complex)",
                "type": "select",
                "options": ["Simple", "Moderate", "Complex"]
            }
        ]
        return questions
    
    def process_user_input(self, question_id: str, answer: Union[str, List[str]]) -> None:
        """Store user responses and validate them for completeness."""
        if not answer or (isinstance(answer, list) and not answer):
            answer = "Not specified"
        self.project_context[question_id] = answer
        self.conversation_history.append({"role": "user", "content": f"{question_id}: {answer}"})
    
    def get_methodology_recommendation(self) -> Dict:
        """Recommend a methodology using weighted context analysis."""
        team_size = self.project_context.get("team_size", "6-12 members")
        challenges = self.project_context.get("challenges", [])
        goals = self.project_context.get("goals", [])
        current_methodology = self.project_context.get("current_methodology", "None/Traditional").lower()
        experience_level = self.project_context.get("experience_level", "Intermediate")
        project_complexity = self.project_context.get("project_complexity", "Moderate")

        # Scoring system for methodology selection
        scores = {"scrum": 0, "kanban": 0, "xp": 0, "lean": 0}
        
        # Team size scoring
        if team_size == "1-5 members":
            scores["kanban"] += 30
            scores["xp"] += 20
            scores["scrum"] += 10
        elif team_size == "6-12 members":
            scores["scrum"] += 30
            scores["xp"] += 20
            scores["kanban"] += 10
        else:  # 13+ members
            scores["scrum"] += 20
            scores["lean"] += 20
            scores["xp"] += 10

        # Challenge scoring
        for challenge in challenges:
            for methodology, info in self.knowledge_base["methodologies"].items():
                if challenge.lower() in info["challenges_addressed"]:
                    scores[methodology] += 15

        # Goal scoring
        goal_weights = {
            "Faster delivery": {"kanban": 15, "lean": 15, "xp": 10},
            "Higher quality": {"xp": 20, "lean": 10},
            "Better predictability": {"scrum": 15, "kanban": 10},
            "Team satisfaction": {"xp": 15, "kanban": 10},
            "Reduced costs": {"lean": 20},
            "Better customer collaboration": {"scrum": 15, "xp": 10},
            "More innovation": {"lean": 15, "xp": 10}
        }
        for goal in goals:
            for methodology, weight in goal_weights.get(goal, {}).items():
                scores[methodology] += weight

        # Experience level adjustment
        if experience_level == "Beginner":
            scores["kanban"] += 10  # Simpler to adopt
            scores["xp"] -= 5  # Complex practices
        elif experience_level == "Advanced":
            scores["xp"] += 10  # Benefits from technical expertise
            scores["lean"] += 5

        # Complexity adjustment
        if project_complexity == "Complex":
            scores["scrum"] += 10
            scores["xp"] += 10
        elif project_complexity == "Simple":
            scores["kanban"] += 10
            scores["lean"] += 5

        # Select the highest-scoring methodology
        recommended_methodology = max(scores, key=scores.get)
        methodology_info = self.knowledge_base["methodologies"].get(recommended_methodology, {})
        
        # Generate detailed reasoning
        reasons = []
        if team_size in methodology_info.get("best_for", []):
            reasons.append(f"Your {team_size} team aligns with {recommended_methodology.upper()}'s ideal team size.")
        for challenge in challenges[:2]:
            if challenge.lower() in methodology_info.get("challenges_addressed", []):
                reasons.append(f"It addresses your challenge of {challenge.lower()} effectively.")
        for goal in goals[:2]:
            if goal in goal_weights and recommended_methodology in goal_weights[goal]:
                reasons.append(f"It supports your goal of {goal.lower()}.")

        return {
            "name": recommended_methodology.upper(),
            "description": methodology_info.get("description", ""),
            "why_recommended": f"Recommended {recommended_methodology.upper()} because: {' '.join(reasons)}",
            "details": methodology_info,
            "implementation_steps": self.generate_implementation_steps(recommended_methodology, current_methodology)
        }
    
    def generate_implementation_steps(self, methodology: str, current_methodology: str) -> List[Dict]:
        """Generate tailored implementation steps with context-specific tips."""
        methodology_info = self.knowledge_base["methodologies"].get(methodology.lower(), {})
        team_size = self.project_context.get("team_size", "6-12 members")
        challenges = self.project_context.get("challenges", [])

        steps = []
        if current_methodology.lower() == methodology.lower():
            steps = [
                {
                    "step": "Assess current practices",
                    "description": f"Conduct a retrospective to identify strengths and gaps in your {methodology.upper()} implementation."
                },
                {
                    "step": "Prioritize improvements",
                    "description": "Select 2-3 practices to enhance based on team feedback and challenges."
                },
                {
                    "step": "Experiment and measure",
                    "description": "Run experiments for 1-2 iterations, tracking metrics like Cycle Time or Team Happiness."
                },
                {
                    "step": "Refine processes",
                    "description": "Adjust practices based on experiment outcomes, focusing on your goals."
                }
            ]
        else:
            steps = [
                {
                    "step": "Train the team",
                    "description": f"Provide a workshop on {methodology.upper()} principles and practices."
                },
                {
                    "step": "Pilot a project",
                    "description": f"Apply {methodology.upper()} to a small project to test its fit."
                },
                {
                    "step": "Set up tools",
                    "description": f"Configure tools like Jira or Trello for {methodology.upper()} artifacts."
                },
                {
                    "step": "Define roles",
                    "description": "Assign roles based on team size and expertise."
                },
                {
                    "step": "Monitor and adapt",
                    "description": "Review progress biweekly to refine the process."
                }
            ]
            # Methodology-specific steps
            if methodology == "scrum":
                steps.insert(2, {
                    "step": "Set sprint length",
                    "description": f"Choose a {2 if team_size == '1-5 members' else 3}-week sprint for {team_size} teams."
                })
            elif methodology == "kanban":
                steps.insert(2, {
                    "step": "Design Kanban board",
                    "description": "Create a board with columns like 'To Do,' 'In Progress,' 'Done' tailored to your workflow."
                })
            elif methodology == "xp":
                steps.insert(2, {
                    "step": "Start TDD",
                    "description": "Begin Test-Driven Development on a single module to build confidence."
                })
                steps.insert(3, {
                    "step": "Implement Pair Programming",
                    "description": "Pair developers to enhance collaboration and code quality."
                })
            elif methodology == "lean":
                steps.insert(2, {
                    "step": "Map value stream",
                    "description": "Identify and eliminate waste in your current process."
                })

        # Add challenge-specific tips
        for step in steps:
            for challenge in challenges[:2]:
                challenge_key = challenge.lower().replace(" ", "_")
                if challenge_key in self.knowledge_base["common_challenges"]:
                    step["description"] += f" For {challenge.lower()}, {self.knowledge_base['common_challenges'][challenge_key]['strategies'][0].lower()}"

        return steps
    
    def get_challenge_advice(self, challenge: str) -> List[str]:
        """Provide detailed, methodology-specific advice for a challenge."""
        challenge_key = challenge.lower().replace(" ", "_")
        methodology = self.project_context.get("current_methodology", "xp").lower()
        challenge_info = self.knowledge_base["common_challenges"].get(challenge_key, {})
        
        advice = challenge_info.get("strategies", [
            "Discuss this challenge in a retrospective to identify root causes.",
            "Experiment with small changes to address it.",
            "Review outcomes after 1-2 iterations."
        ])
        
        # Add methodology-specific advice
        if methodology in self.knowledge_base["methodologies"]:
            specific_advice = challenge_info.get(f"{methodology}_specific", [])
            advice.extend(specific_advice)
        
        return advice
    
    def generate_full_recommendations(self) -> Dict:
        """Generate comprehensive, context-driven recommendations."""
        recommendations = {
            "methodology": self.get_methodology_recommendation(),
            "team_practices": self.get_team_practices_recommendations(),
            "challenges": self.get_challenges_recommendations(),
            "tools": self.recommend_tools(),
            "metrics": self.recommend_metrics()
        }
        
        methodology = recommendations["methodology"]["name"]
        team_size = self.project_context.get("team_size", "6-12 members")
        summary = (
            f"For your {team_size} team, I recommend {methodology} to address your challenges and goals. "
            f"Focus on practices like {', '.join([p['practice'] for p in recommendations['team_practices'][:2]])}. "
            f"Track metrics like {', '.join([m['metric'] for m in recommendations['metrics'][:2]])} to measure progress."
        )
        self.conversation_history.append({"role": "agent", "content": summary})
        
        return recommendations
    
    def get_team_practices_recommendations(self) -> List[Dict]:
        """Recommend practices tailored to context and methodology."""
        challenges = self.project_context.get("challenges", [])
        methodology = self.project_context.get("current_methodology", "xp").lower()
        team_size = self.project_context.get("team_size", "6-12 members")
        
        practices = []
        
        # Methodology-specific practices
        if methodology == "xp":
            if "quality_issues" in challenges or "Higher quality" in self.project_context.get("goals", []):
                practices.append({
                    "practice": "Test-Driven Development",
                    "description": "Write tests before code to ensure quality and reduce defects.",
                    "implementation_tips": [
                        f"For {team_size}, start TDD on a critical module.",
                        "Use a testing framework like pytest.",
                        "Train team in a 2-hour workshop."
                    ]
                })
            if "lack_of_engagement" in challenges or "Team satisfaction" in self.project_context.get("goals", []):
                practices.append({
                    "practice": "Pair Programming",
                    "description": "Two developers work together to improve code and collaboration.",
                    "implementation_tips": [
                        f"Rotate pairs weekly for {team_size} to share knowledge.",
                        "Use tools like VS Code Live Share.",
                        "Set clear pairing guidelines."
                    ]
                })
        elif methodology == "kanban":
            if "poor_communication" in challenges:
                practices.append({
                    "practice": "Information Radiators",
                    "description": "Visual boards to enhance transparency.",
                    "implementation_tips": [
                        f"Create a digital board for {team_size} using Trello.",
                        "Update daily in standups.",
                        "Include WIP limits."
                    ]
                })
        elif methodology == "scrum":
            if "scope_creep" in challenges:
                practices.append({
                    "practice": "Backlog Refinement",
                    "description": "Regularly prioritize and refine the backlog.",
                    "implementation_tips": [
                        f"For {team_size}, hold 1-hour sessions biweekly.",
                        "Involve stakeholders for alignment.",
                        "Use story points for sizing."
                    ]
                })
        
        # Always include key practices from recommendations
        default_practices = [
            {
                "practice": "Regular Retrospectives",
                "description": "Reflect on processes to drive improvement.",
                "implementation_tips": [
                    f"Hold biweekly for {team_size}.",
                    "Use formats like Start-Stop-Continue.",
                    "Track action items."
                ]
            },
            {
                "practice": "Definition of Done",
                "description": "Criteria for task completion to ensure quality.",
                "implementation_tips": [
                    f"Define collaboratively with {team_size}.",
                    "Post visibly in your workspace.",
                    "Review monthly."
                ]
            }
        ]
        
        for practice in default_practices:
            if len(practices) < 3 and practice["practice"] not in [p["practice"] for p in practices]:
                practices.append(practice)
        
        return practices
    
    def get_challenges_recommendations(self) -> List[Dict]:
        """Generate tailored recommendations for each challenge."""
        challenges = self.project_context.get("challenges", [])
        recommendations = []
        
        for challenge in challenges:
            advice = self.get_challenge_advice(challenge)
            recommendations.append({
                "challenge": challenge,
                "recommendations": advice
            })
        
        return recommendations
    
    def recommend_tools(self) -> List[Dict]:
        """Recommend tools aligned with methodology and team needs."""
        methodology = self.project_context.get("current_methodology", "xp").lower()
        team_size = self.project_context.get("team_size", "6-12 members")
        
        tools = [
            {
                "category": "Project Management",
                "options": [
                    {"name": "Jira", "best_for": ["scrum", "kanban", "xp"], "description": f"Manages tasks and metrics for {team_size}."},
                    {"name": "Trello", "best_for": ["kanban"], "description": f"Simple visual boards for {team_size}."},
                    {"name": "Azure DevOps", "best_for": ["scrum", "xp"], "description": f"Supports CI/CD for {team_size}."}
                ]
            },
            {
                "category": "Collaboration",
                "options": [
                    {"name": "Slack", "best_for": ["all methodologies"], "description": f"Real-time chat for {team_size}."},
                    {"name": "Microsoft Teams", "best_for": ["all methodologies"], "description": f"Integrated collaboration for {team_size}."}
                ]
            },
            {
                "category": "Testing/CI",
                "options": [
                    {"name": "Jenkins", "best_for": ["xp"], "description": f"Automates CI for {team_size}."},
                    {"name": "GitHub Actions", "best_for": ["xp", "scrum"], "description": f"CI/CD workflows for {team_size}."}
                ]
            }
        ]
        
        recommended_tools = []
        for category in tools:
            for tool in category["options"]:
                if methodology in [m.lower() for m in tool["best_for"]] or "all methodologies" in [m.lower() for m in tool["best_for"]]:
                    recommended_tools.append({
                        "category": category["category"],
                        "recommendation": tool["name"],
                        "description": tool["description"]
                    })
                    break
            else:
                recommended_tools.append({
                    "category": category["category"],
                    "recommendation": category["options"][0]["name"],
                    "description": category["options"][0]["description"]
                })
        
        return recommended_tools
    
    def recommend_metrics(self) -> List[Dict]:
        """Recommend metrics tailored to methodology and goals."""
        methodology = self.project_context.get("current_methodology", "xp").lower()
        goals = self.project_context.get("goals", [])
        challenges = self.project_context.get("challenges", [])
        
        metrics = []
        for metric, info in self.knowledge_base["metrics"].items():
            methodology_match = methodology in [m.lower() for m in info["best_for"]] or "all methodologies" in [m.lower() for m in info["best_for"]]
            goal_match = False
            if "Faster delivery" in goals and metric in ["Cycle Time", "Lead Time"]:
                goal_match = True
            elif "Higher quality" in goals and metric == "Defect Rate":
                goal_match = True
            elif "Team satisfaction" in goals and metric == "Team Happiness":
                goal_match = True
            elif "Better predictability" in goals and metric == "Velocity":
                goal_match = True
            if "quality_issues" in challenges and metric == "Defect Rate":
                goal_match = True
            if methodology_match or goal_match:
                metrics.append({
                    "metric": metric,
                    "description": info["description"],
                    "how_to_measure": info["how_to_measure"],
                    "tips": info["implementation_tips"]
                })
        
        # Ensure at least 3 metrics
        available_metrics = list(self.knowledge_base["metrics"].keys())
        while len(metrics) < 3:
            for metric in available_metrics:
                if metric not in [m["metric"] for m in metrics]:
                    info = self.knowledge_base["metrics"][metric]
                    metrics.append({
                        "metric": metric,
                        "description": info["description"],
                        "how_to_measure": info["how_to_measure"],
                        "tips": info["implementation_tips"]
                    })
                    break
        
        return metrics
    
    def process_free_text_query(self, query: str) -> str:
        """Process free-text queries with detailed, context-specific responses."""
        query_lower = query.lower().strip()
        self.conversation_history.append({"role": "user", "content": query})
        
        # Extract context
        team_size = self.project_context.get("team_size", "6-12 members")
        challenges = self.project_context.get("challenges", [])
        industry = self.project_context.get("industry", "unknown")
        goals = self.project_context.get("goals", [])
        methodology = self.project_context.get("current_methodology", "xp").lower()
        
        # Synonym mapping for challenges
        challenge_synonyms = {
            "resistance_to_change": ["resistance", "opposition", "change reluctance"],
            "lack_of_engagement": ["engagement", "low participation", "disengagement", "motivation"],
            "poor_communication": ["communication", "misalignment", "clarity"],
            "inconsistent_estimation": ["estimation", "planning accuracy"],
            "scope_creep": ["scope", "feature creep"],
            "quality_issues": ["quality", "bugs", "defects"],
            "meeting_deadlines": ["deadlines", "delivery", "timeliness"],
            "stakeholder_management": ["stakeholder", "client management"]
        }
        
        # Helper function to find matching challenge
        def find_challenge(query_lower: str) -> Optional[str]:
            for challenge_key, synonyms in challenge_synonyms.items():
                if challenge_key.replace("_", " ") in query_lower or any(s in query_lower for s in synonyms):
                    return challenge_key
            return None
        
        # Kanban-specific queries
        if "kanban board" in query_lower:
            response = (
                f"To set up a Kanban board for your {team_size} team in {industry}, follow these steps:\n"
                "1. Identify your workflow stages (e.g., To Do, In Progress, Review, Done).\n"
                "2. Create a digital board using Trello or Jira with 3-5 columns reflecting these stages.\n"
                "3. Add tasks as cards, including descriptions and due dates.\n"
                "4. Set Work-in-Progress (WIP) limits (e.g., 2-3 tasks per column) to prevent overloading.\n"
                "5. Review and update the board daily in standups.\n"
                f"Implementation tips for {team_size}:\n"
                "- Keep columns simple to match your small team’s capacity.\n"
                "- Use visual cues (e.g., color labels) for task types.\n"
                "- Adjust WIP limits weekly based on flow.\n"
            )
            if "poor_communication" in challenges:
                response += "To address poor communication, use the board as an information radiator, ensuring all team members stay aligned.\n"
            if "lack_of_engagement" in challenges:
                response += "To improve engagement, involve the team in designing the board to foster ownership.\n"
            if "Faster delivery" in goals:
                response += "Since faster delivery is a goal, optimize flow to reduce Cycle Time.\n"
        
        # XP-specific queries
        elif "test-driven" in query_lower or "tdd" in query_lower:
            response = (
                f"To implement Test-Driven Development (TDD) for your {team_size} team in {industry}, follow these steps:\n"
                "1. Write a failing unit test for a small feature using a framework like pytest.\n"
                "2. Run the test to confirm it fails (red phase).\n"
                "3. Write minimal code to pass the test (green phase).\n"
                "4. Refactor to improve code quality, ensuring tests still pass.\n"
                "5. Repeat for each feature or bug fix.\n"
                f"Implementation tips for {team_size}:\n"
                "- Start with a critical module to show value.\n"
                "- Train developers in a 2-hour TDD workshop.\n"
                "- Use pair programming to reinforce TDD.\n"
            )
            if "resistance_to_change" in challenges:
                response += "To address resistance to change, demonstrate TDD’s defect reduction with a pilot, showing tangible results.\n"
            if "lack_of_engagement" in challenges:
                response += "To boost engagement, let developers see immediate test feedback, making work more rewarding.\n"
            if "Higher quality" in goals:
                response += "Since quality is a goal, TDD will help ensure robust code with fewer bugs.\n"
        
        elif "pair programming" in query_lower:
            response = (
                f"Pair Programming is an XP practice where two developers work together at one workstation to write code. "
                f"For your {team_size} team in {industry}, here’s how to use it:\n"
                "1. Pair developers with complementary skills (e.g., senior/junior).\n"
                "2. Set up a shared coding environment (e.g., VS Code Live Share).\n"
                "3. Rotate pairs weekly to spread knowledge and avoid fatigue.\n"
                "4. Define roles: one writes code (driver), the other reviews and suggests (navigator).\n"
                "5. Schedule 2-4 hour pairing sessions with breaks.\n"
                f"Implementation tips for {team_size}:\n"
                "- Use pairing for complex tasks to improve quality.\n"
                "- Monitor team feedback to adjust pair frequency.\n"
                "- Celebrate successful pair outcomes to build buy-in.\n"
            )
            if "lack_of_engagement" in challenges:
                response += "To improve engagement, rotate pairs to foster collaboration and make work interactive.\n"
            if "resistance_to_change" in challenges:
                response += "To reduce resistance, start pairing on small tasks and highlight improved code quality.\n"
            if "Team satisfaction" in goals:
                response += "Since team satisfaction is a goal, pairing can build stronger team bonds and shared ownership.\n"
        
        # Challenge-related queries
        elif (challenge_key := find_challenge(query_lower)):
            challenge_info = self.knowledge_base["common_challenges"].get(challenge_key, {})
            response = (
                f"To address {challenge_key.replace('_', ' ')} for your {team_size} team in {industry}, try these strategies:\n"
                + "\n".join([f"- {s}" for s in challenge_info.get("strategies", [])]) + "\n"
            )
            if methodology in self.knowledge_base["methodologies"]:
                specific_key = f"{methodology}_specific"
                if specific_key in challenge_info:
                    response += f"In {methodology.upper()}, specifically:\n" + "\n".join([f"- {s}" for s in challenge_info[specific_key]]) + "\n"
            if "Team satisfaction" in goals and challenge_key == "lack_of_engagement":
                response += "Since team satisfaction is a goal, use retrospectives to act on engagement feedback.\n"
            if "Faster delivery" in goals and challenge_key == "meeting_deadlines":
                response += "Since faster delivery is a goal, optimize flow with smaller tasks and frequent reviews.\n"
        
        # Metric-related queries
        elif "defect rate" in query_lower:
            metric_info = self.knowledge_base["metrics"]["defect_rate"]
            response = (
                f"Defect Rate measures bugs found after release, critical for quality in XP. "
                f"For your {team_size} team in {industry}:\n"
                "1. Track bugs in a tool like Jira post-release.\n"
                "2. Calculate as bugs per feature, sprint, or 1,000 lines of code.\n"
                "3. Use TDD to catch defects early, reducing the rate.\n"
                "4. Review weekly in retrospectives to identify trends.\n"
                f"Implementation tips for {team_size}:\n"
                + "\n".join([f"- {t}" for t in metric_info["implementation_tips"]]) + "\n"
            )
            if "Higher quality" in goals:
                response += "Since quality is a goal, aim for a Defect Rate below 1 bug per feature.\n"
            if "quality_issues" in challenges:
                response += "To address quality issues, combine TDD with automated testing to lower defects.\n"
        
        elif "team happiness" in query_lower:
            metric_info = self.knowledge_base["metrics"]["team_happiness"]
            response = (
                f"Team Happiness measures satisfaction and engagement. For your {team_size} team in {industry}:\n"
                "1. Conduct biweekly surveys with a 1-5 scale (e.g., via Google Forms).\n"
                "2. Ask questions like 'Do you feel valued?' or 'Are you satisfied with our process?'\n"
                "3. Discuss results in retrospectives to plan improvements.\n"
                "4. Track trends over 2-3 months to assess impact.\n"
                f"Implementation tips for {team_size}:\n"
                + "\n".join([f"- {t}" for t in metric_info["implementation_tips"]]) + "\n"
            )
            if "lack_of_engagement" in challenges:
                response += "To address low engagement, act on survey feedback with visible changes.\n"
            if "Team satisfaction" in goals:
                response += "Since team satisfaction is a goal, prioritize actions that boost morale, like celebrating wins.\n"
        
        # Methodology queries
        elif any(m in query_lower for m in self.knowledge_base["methodologies"]):
            for methodology_name, info in self.knowledge_base["methodologies"].items():
                if methodology_name in query_lower:
                    response = (
                        f"{methodology_name.upper()} is {info['description']} It’s best for {', '.join(info['best_for'])}.\n"
                        f"Key practices include: {', '.join(info['practices'] if 'practices' in info else info.get('ceremonies', info['principles']))}.\n"
                        f"Implementation tips for {team_size}:\n"
                        + "\n".join([f"- {t}" for t in info["implementation_tips"]]) + "\n"
                    )
                    if methodology_name == methodology:
                        response += f"Since you’re using {methodology_name.upper()}, focus on these practices to address {', '.join(challenges[:2])}.\n"
                    break
            else:
                response = f"Please specify a methodology like Scrum, Kanban, XP, or Lean for detailed advice."
        
        # General agile queries
        elif "agile" in query_lower or "methodology" in query_lower:
            response = (
                f"For your {team_size} team in {industry}, {methodology.upper()} is recommended based on your context. "
                f"It addresses {', '.join(challenges[:2] if challenges else ['your needs'])} and supports {', '.join(goals[:2] if goals else ['your goals'])}.\n"
                f"Key practices: {', '.join(self.knowledge_base['methodologies'][methodology]['practices'] if 'practices' in self.knowledge_base['methodologies'][methodology] else self.knowledge_base['methodologies'][methodology].get('ceremonies', self.knowledge_base['methodologies'][methodology]['principles']))}.\n"
                f"Ask about specific practices or challenges for detailed guidance."
            )
        
        # Fallback for unrecognized queries
        else:
            # Suggest practices based on context
            suggested_practices = self.get_team_practices_recommendations()
            response = (
                f"Your question about '{query}' is noted, but I need more specificity to provide tailored advice for your {team_size} team in {industry}. "
                f"Based on your context, consider these practices to address {', '.join(challenges[:2] if challenges else ['your needs'])}:\n"
                + "\n".join([f"- {p['practice']}: {p['description']}" for p in suggested_practices[:2]]) + "\n"
                f"Try asking about a specific practice (e.g., Kanban board), challenge (e.g., poor communication), or metric (e.g., Cycle Time) for detailed guidance."
            )
        
        self.conversation_history.append({"role": "agent", "content": response})
        return response

    def save_conversation(self, file_path: str) -> None:
        """Save the conversation history to a file with error handling."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            self.conversation_history.append({"role": "agent", "content": f"Conversation saved to {file_path}."})
        except Exception as e:
            self.conversation_history.append({"role": "agent", "content": f"Failed to save conversation: {str(e)}."})
            raise
    
    def get_conversation_history(self) -> List[Dict]:
        """Return the full conversation history with context summary."""
        if not self.conversation_history:
            return [{"role": "agent", "content": "No conversation history yet. Start by asking a question or running an assessment."}]
        return self.conversation_history