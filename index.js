// Agile Project Consultant - Vibing AI Agent
const { AgentBuilder, Card, Panel } = require('@vibing-ai/sdk');

// Initialize the Agile Consultant Agent
const agent = new AgentBuilder()
  .setName('Agile Project Consultant')
  .setDescription('Expert guidance on agile development processes, tailored to your team.')
  .setIcon('https://example.com/agile-icon.png') // Replace with actual icon URL
  .setVersion('1.0.0')
  .build();

// Store consultant state for each user session
const sessionState = new Map();

// Knowledge base of agile methodologies (simplified from Python implementation)
const knowledgeBase = {
  methodologies: {
    scrum: {
      description: "Framework that helps teams work together through regular cadences of work and structured artifacts.",
      best_for: ["teams of 3-9 members", "complex products", "environments with changing requirements"],
      ceremonies: ["Sprint Planning", "Daily Standup", "Sprint Review", "Sprint Retrospective"],
      roles: ["Product Owner", "Scrum Master", "Development Team"],
      artifacts: ["Product Backlog", "Sprint Backlog", "Increment"]
    },
    kanban: {
      description: "Visual workflow management method focused on delivering value continuously without overloading the team.",
      best_for: ["support teams", "operations work", "projects with unpredictable requests"],
      principles: ["Visualize workflow", "Limit work in progress", "Manage flow", "Make process policies explicit"],
      practices: ["Kanban board", "WIP limits", "Continuous delivery", "Feedback loops"]
    },
    xp: {
      description: "Software development methodology focused on engineering practices to ensure high-quality code.",
      best_for: ["small co-located teams", "complex code bases", "environments requiring high quality"],
      practices: ["Pair Programming", "Test-Driven Development", "Continuous Integration", "Simple Design", "Refactoring"]
    },
    lean: {
      description: "Approach focused on maximizing value while minimizing waste.",
      best_for: ["any size team", "organizations seeking efficiency", "process improvement"],
      principles: ["Eliminate waste", "Build quality in", "Create knowledge", "Defer commitment", "Deliver fast"]
    }
  },
  // Additional knowledge base sections would be added here
};

// Assessment questions
const assessmentQuestions = [
  {
    id: "team_size",
    question: "How large is your team?",
    type: "select",
    options: ["1-5 members", "6-12 members", "13+ members"]
  },
  {
    id: "industry",
    question: "What industry are you in?",
    type: "text"
  },
  {
    id: "current_methodology",
    question: "Are you currently using any agile methodology?",
    type: "select",
    options: ["None/Traditional", "Scrum", "Kanban", "XP", "Lean", "Hybrid", "Other"]
  },
  {
    id: "experience_level",
    question: "What is your team's experience level with agile practices?",
    type: "select",
    options: ["Beginner", "Intermediate", "Advanced"]
  },
  {
    id: "challenges",
    question: "What challenges are you facing?",
    type: "multi-select",
    options: [
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
    id: "goals",
    question: "What are your primary goals for improving your process?",
    type: "multi-select",
    options: [
      "Faster delivery",
      "Higher quality",
      "Better predictability",
      "Team satisfaction",
      "Reduced costs",
      "Better customer collaboration",
      "More innovation"
    ]
  }
];

// Helper function to get methodology recommendation based on context
function getMethodologyRecommendation(context) {
  // Simple recommendation logic
  let recommendedMethodology = null;
  
  if (context.challenges && context.challenges.includes("Scope creep") && 
      context.challenges.includes("Meeting deadlines")) {
    recommendedMethodology = "scrum";
  } else if ((context.challenges && context.challenges.includes("Unpredictable workflow")) || 
             context.team_size === "1-5 members") {
    recommendedMethodology = "kanban";
  } else if (context.challenges && context.challenges.includes("Quality issues")) {
    recommendedMethodology = "xp";
  } else if (context.goals && context.goals.includes("Reduced costs")) {
    recommendedMethodology = "lean";
  } else {
    // Default recommendation
    recommendedMethodology = context.team_size !== "1-5 members" ? "scrum" : "kanban";
  }
  
  return {
    name: recommendedMethodology.toUpperCase(),
    description: knowledgeBase.methodologies[recommendedMethodology].description,
    why_recommended: `Based on your ${context.team_size} team size and challenges, ${recommendedMethodology.toUpperCase()} would be a good fit.`,
    details: knowledgeBase.methodologies[recommendedMethodology]
  };
}

// Welcome message handler
agent.onMessage("welcome", async (ctx) => {
  // Start a new session
  const sessionId = ctx.session.id;
  sessionState.set(sessionId, {
    assessmentComplete: false,
    projectContext: {},
    conversation: []
  });
  
  const welcomeMessage = 
    "Welcome! I'm your Agile Project Consultant. I can help you implement or improve " +
    "agile practices for your team. To provide tailored recommendations, I'll need " +
    "to understand your current situation.";
  
  await ctx.sendText(welcomeMessage);
  
  // Add buttons for next steps
  const actionCard = new Card()
    .setTitle("How would you like to proceed?")
    .addButton("Start Assessment", "start_assessment")
    .addButton("Ask a Question", "ask_question");
  
  await ctx.send(actionCard);
  
  // Store in conversation history
  const session = sessionState.get(sessionId);
  session.conversation.push({ role: "agent", content: welcomeMessage });
});

// Start assessment handler
agent.onAction("start_assessment", async (ctx) => {
  await ctx.sendText("Great! Let's start with understanding your team and project context.");
  
  // Create an assessment panel with the questions
  const assessmentPanel = new Panel()
    .setTitle("Agile Project Assessment")
    .setDescription("Please answer the following questions to help me understand your situation.");
  
  // Add form fields for each question
  assessmentQuestions.forEach(question => {
    if (question.type === "text") {
      assessmentPanel.addTextField(question.id, question.question);
    } else if (question.type === "select") {
      assessmentPanel.addDropdown(question.id, question.question, question.options);
    } else if (question.type === "multi-select") {
      assessmentPanel.addCheckboxGroup(question.id, question.question, question.options);
    }
  });
  
  // Add submit button
  assessmentPanel.addButton("Submit Assessment", "submit_assessment");
  
  await ctx.send(assessmentPanel);
});

// Handle assessment submission
agent.onAction("submit_assessment", async (ctx) => {
  const sessionId = ctx.session.id;
  const session = sessionState.get(sessionId);
  const formData = ctx.event.data;
  
  // Store assessment answers
  session.projectContext = formData;
  session.assessmentComplete = true;
  
  await ctx.sendText("Thanks for completing the assessment. I'm analyzing your responses...");
  
  // Generate recommendations based on the assessment
  const methodologyRec = getMethodologyRecommendation(session.projectContext);
  
  // Create a recommendation card
  const recCard = new Card()
    .setTitle(`Recommended: ${methodologyRec.name}`)
    .setDescription(methodologyRec.description)
    .addSection("Why This Fits Your Team", methodologyRec.why_recommended);
  
  // Add key elements of the methodology
  if (methodologyRec.details.practices) {
    recCard.addSection("Key Practices", methodologyRec.details.practices.join(", "));
  } else if (methodologyRec.details.ceremonies) {
    recCard.addSection("Key Ceremonies", methodologyRec.details.ceremonies.join(", "));
  }
  
  if (methodologyRec.details.roles) {
    recCard.addSection("Key Roles", methodologyRec.details.roles.join(", "));
  }
  
  recCard.addButton("Implementation Steps", "show_implementation_steps");
  recCard.addButton("Ask Follow-up Question", "ask_question");
  
  await ctx.send(recCard);
  
  // Add a text summary as well
  const summaryText = `Based on your inputs, I recommend ${methodologyRec.name} methodology. ` +
    `This is particularly well-suited for ${methodologyRec.details.best_for.join(", ")}. ` +
    `Would you like more specific advice on implementing this approach?`;
  
  await ctx.sendText(summaryText);
  
  // Store in conversation history
  session.conversation.push({ role: "agent", content: summaryText });
});

// Handle showing implementation steps
agent.onAction("show_implementation_steps", async (ctx) => {
  const sessionId = ctx.session.id;
  const session = sessionState.get(sessionId);
  
  if (!session.assessmentComplete) {
    await ctx.sendText("Please complete the assessment first so I can provide personalized implementation steps.");
    return;
  }
  
  const methodology = getMethodologyRecommendation(session.projectContext).name.toLowerCase();
  const currentMethodology = session.projectContext.current_methodology || "None/Traditional";
  
  let steps;
  if (currentMethodology.toLowerCase() === methodology) {
    // Improvement steps
    steps = [
      {
        step: "Conduct a facilitated retrospective",
        description: "Review what's working and what's not with your current process."
      },
      {
        step: "Identify 2-3 improvement areas",
        description: "Based on retrospective results, select a few focus areas."
      },
      {
        step: "Create an experiment for each area",
        description: "Design small experiments to address each improvement area."
      },
      {
        step: "Implement and measure",
        description: "Run experiments for 2-3 iterations and collect feedback."
      }
    ];
  } else {
    // New implementation steps
    steps = [
      {
        step: "Education and training",
        description: `Provide training on ${methodology.toUpperCase()} for the entire team.`
      },
      {
        step: "Start small",
        description: "Begin with a pilot project or team to test the approach."
      },
      {
        step: "Define roles and responsibilities",
        description: "Clearly establish who will take on which roles in the new process."
      },
      {
        step: "Create necessary artifacts",
        description: `Set up the tools and artifacts needed for ${methodology.toUpperCase()}.`
      },
      {
        step: "Regular inspection and adaptation",
        description: "Schedule regular reviews of the process to make adjustments."
      }
    ];
    
    // Add methodology-specific steps
    if (methodology === "scrum") {
      steps.splice(2, 0, {
        step: "Establish sprint length",
        description: "Decide on an appropriate sprint length (typically 1-4 weeks)."
      });
    } else if (methodology === "kanban") {
      steps.splice(2, 0, {
        step: "Create Kanban board",
        description: "Design a board that visualizes your specific workflow."
      });
    }
  }
  
  // Create an implementation steps panel
  const stepsPanel = new Panel()
    .setTitle(`${methodology.toUpperCase()} Implementation Steps`)
    .setDescription("Follow these steps to successfully implement or improve your agile process:");
  
  // Add each step
  steps.forEach((item, index) => {
    stepsPanel.addSection(`Step ${index + 1}: ${item.step}`, item.description);
  });
  
  stepsPanel.addButton("Ask Follow-up Question", "ask_question");
  
  await ctx.send(stepsPanel);
});

// Handle ask question action
agent.onAction("ask_question", async (ctx) => {
  await ctx.sendText("What specific question do you have about agile methodologies or your implementation?");
});

// Process free text queries
agent.onMessage(async (ctx) => {
  const sessionId = ctx.session.id;
  const query = ctx.event.text;
  
  // Initialize session if it doesn't exist
  if (!sessionState.has(sessionId)) {
    sessionState.set(sessionId, {
      assessmentComplete: false,
      projectContext: {},
      conversation: []
    });
  }
  
  const session = sessionState.get(sessionId);
  
  // Store user message in history
  session.conversation.push({ role: "user", content: query });
  
  // Simple keyword-based response logic
  const queryLower = query.toLowerCase();
  let response = "";
  
  if (queryLower.includes("estimation")) {
    response = 
      "For better estimations, consider these techniques:\n" +
      "1. Use relative sizing (story points) instead of time\n" +
      "2. Implement Planning Poker for collaborative estimation\n" +
      "3. Break down larger items into smaller, more predictable pieces\n" +
      "4. Maintain an estimation guide with reference stories\n" +
      "5. Regularly review your estimation accuracy to improve over time";
  } else if (queryLower.includes("retrospective")) {
    response = 
      "To improve your retrospectives:\n" +
      "1. Use varied formats to keep them engaging (e.g., Start-Stop-Continue, 4Ls)\n" +
      "2. Focus on actionable improvements, not just venting\n" +
      "3. Follow up on action items from previous retrospectives\n" +
      "4. Create a safe space for honest feedback\n" +
      "5. Timebox discussions to stay productive";
  } else if (queryLower.includes("remote") || queryLower.includes("distributed")) {
    response = 
      "For effective remote/distributed agile teams:\n" +
      "1. Use video for all ceremonies to improve engagement\n" +
      "2. Invest in digital collaboration tools (digital boards, documentation)\n" +
      "3. Schedule regular social interactions to build team cohesion\n" +
      "4. Be explicit about working agreements and communication norms\n" +
      "5. Consider asynchronous updates to accommodate different time zones";
  } else if (queryLower.includes("start") && queryLower.includes("assessment")) {
    // Trigger the assessment flow
    await ctx.sendAction("start_assessment");
    return;
  } else {
    // Default response
    if (!session.assessmentComplete) {
      response = 
        `I understand you're asking about "${query}". To provide more specific guidance, ` +
        `I'd need more context about your team and project situation. Would you like to complete ` +
        `a quick assessment so I can give you personalized recommendations?`;
        
      // Add assessment button
      const actionCard = new Card()
        .setTitle("Would you like to:")
        .addButton("Start Assessment", "start_assessment")
        .addButton("Just Answer My Question", "continue_chat");
        
      await ctx.send(actionCard);
    } else {
      // They've completed an assessment, so provide a more personalized response
      const methodology = getMethodologyRecommendation(session.projectContext).name;
      response = 
        `Based on what you've shared about your team using ${methodology}, I think addressing ` +
        `"${query}" requires a tailored approach. Would you like specific advice on this topic ` +
        `in the context of ${methodology}, or general best practices?`;
        
      // Add context buttons
      const contextCard = new Card()
        .setTitle("Would you like advice on:")
        .addButton(`${methodology}-specific approach`, "methodology_specific")
        .addButton("General best practices", "general_practices");
        
      await ctx.send(contextCard);
    }
  }
  
  // Send the text response
  await ctx.sendText(response);
  
  // Store agent response in history
  session.conversation.push({ role: "agent", content: response });
});

// Handle continue chat action
agent.onAction("continue_chat", async (ctx) => {
  await ctx.sendText("I'll do my best to answer your question with the information available. For more personalized advice, you can always start the assessment later.");
});

// Handle methodology specific action
agent.onAction("methodology_specific", async (ctx) => {
  const sessionId = ctx.session.id;
  const session = sessionState.get(sessionId);
  const methodology = getMethodologyRecommendation(session.projectContext).name;
  
  await ctx.sendText(`Let me provide some ${methodology}-specific advice for your question...`);
  
  // Here you would add more specific content based on the methodology
  // This is a placeholder for implementation
  await ctx.sendText(`When implementing ${methodology}, it's important to focus on its core principles while adapting to your specific team context. Would you like me to elaborate on any particular aspect?`);
});

// Handle general practices action
agent.onAction("general_practices", async (ctx) => {
  await ctx.sendText("Here are some general agile best practices that apply across methodologies:");
  
  const practicesCard = new Card()
    .setTitle("Agile Best Practices")
    .addSection("Customer Collaboration", "Involve customers throughout the development process")
    .addSection("Embrace Change", "Be flexible and adapt to changing requirements")
    .addSection("Deliver Frequently", "Release working software in short cycles")
    .addSection("Sustainable Pace", "Maintain a pace the team can sustain indefinitely")
    .addSection("Technical Excellence", "Focus on good design and clean code");
    
  await ctx.send(practicesCard);
});

// Export the agent
module.exports = agent;