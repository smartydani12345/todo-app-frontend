from typing import Dict, List, Any
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GuidanceService:
    """
    Service to provide feature explanations, troubleshooting assistance,
    and step-by-step tutorials for the application.
    """
    
    def __init__(self):
        # Knowledge base for Phase 2 features
        self.knowledge_base = {
            "creating_tasks": {
                "keywords": ["create", "add", "new", "task", "make"],
                "explanation": "To create a new task, click the 'Add Task' button or press the '+' icon. Enter your task title and description, set priority and due date if needed, then click 'Save'.",
                "tutorial": "1. Click the 'Add Task' button\n2. Fill in the task details\n3. Set priority and due date if needed\n4. Click 'Save'",
                "troubleshooting": "If you can't create a task, make sure the title field is not empty and you have a stable internet connection."
            },
            "editing_tasks": {
                "keywords": ["edit", "update", "change", "modify", "task"],
                "explanation": "To edit a task, click on the task you want to modify. This will open the task details view where you can update the title, description, priority, due date, and other properties.",
                "tutorial": "1. Click on the task you want to edit\n2. Modify the task details\n3. Click 'Save' to apply changes",
                "troubleshooting": "If you can't edit a task, ensure you're clicking on the correct task and have the necessary permissions."
            },
            "completing_tasks": {
                "keywords": ["complete", "done", "finish", "mark", "task"],
                "explanation": "To mark a task as complete, click the checkbox next to the task title. You can also open the task details and toggle the 'Completed' switch.",
                "tutorial": "1. Find the task you want to complete\n2. Click the checkbox next to the task title\n3. The task will be marked as completed",
                "troubleshooting": "If you can't mark a task as complete, refresh the page and try again."
            },
            "deleting_tasks": {
                "keywords": ["delete", "remove", "trash", "cancel", "task"],
                "explanation": "To delete a task, open the task details and click the 'Delete' button. Confirm the deletion when prompted.",
                "tutorial": "1. Open the task you want to delete\n2. Click the 'Delete' button\n3. Confirm the deletion in the dialog box",
                "troubleshooting": "If you can't delete a task, make sure you have the necessary permissions."
            },
            "setting_priorities": {
                "keywords": ["priority", "high", "medium", "low", "important"],
                "explanation": "Tasks can have three priority levels: High, Medium, and Low. High priority tasks appear at the top of your list and are highlighted.",
                "tutorial": "1. Open a task\n2. Select the priority level from the dropdown\n3. Save the task",
                "troubleshooting": "If priority settings aren't saving, check your internet connection and try again."
            },
            "due_dates": {
                "keywords": ["due", "date", "calendar", "schedule", "deadline"],
                "explanation": "Set due dates for tasks to keep track of deadlines. Tasks with approaching due dates will be highlighted.",
                "tutorial": "1. Open a task\n2. Click on the calendar icon\n3. Select a date\n4. Save the task",
                "troubleshooting": "If due dates aren't appearing correctly, check that your device's date and time are set correctly."
            },
            "tags": {
                "keywords": ["tag", "label", "category", "organize", "group"],
                "explanation": "Use tags to categorize and organize your tasks. You can filter tasks by tags to quickly find related items.",
                "tutorial": "1. Open a task\n2. Click on the tags field\n3. Enter or select tags\n4. Save the task",
                "troubleshooting": "If tags aren't saving, make sure you're pressing Enter or clicking 'Add' after entering each tag."
            },
            "filtering_tasks": {
                "keywords": ["filter", "sort", "search", "find", "show"],
                "explanation": "Filter your tasks by priority, due date, tags, or completion status using the filter options.",
                "tutorial": "1. Click the filter icon\n2. Select your filter criteria\n3. Apply the filters",
                "troubleshooting": "If filters aren't working, try clearing all filters and applying them one at a time."
            }
        }
        
        # Developer information
        self.developer_info = {
            "name": "Daniyal Azhar",
            "role": "GIAIC Student",
            "project": "TODO EVOLUTION",
            "hackathon": "Panaversity Hackathon",
            "technologies": ["Next.js 16.1.6", "FastAPI", "Cohere AI", "SQLModel", "Web Speech API"],
            "values": "Islamic values integration",
            "about": "Daniyal Azhar is a student at GIAIC who participated in the Panaversity Hackathon. He developed the TODO EVOLUTION project, which includes advanced features like AI-powered chatbot assistance, multi-language support, and voice commands. His work emphasizes the integration of Islamic values in technology solutions."
        }
    
    def classify_query(self, query: str) -> str:
        """
        Classify the user's query to determine the appropriate response category.
        
        Args:
            query: The user's query string
            
        Returns:
            Category of the query (feature_explanation, troubleshooting, developer_info, etc.)
        """
        query_lower = query.lower()
        
        # Check for developer-related queries
        if any(word in query_lower for word in ["who", "created", "made", "developer", "author", "built", "programmer", "engineer", "creator", "person"]):
            return "developer_info"
        
        # Check for tutorial-related queries
        if any(word in query_lower for word in ["how", "step", "guide", "tutorial", "instruction", "show me", "help me", "way to"]):
            return "tutorial"
        
        # Check for troubleshooting-related queries
        if any(word in query_lower for word in ["problem", "issue", "error", "not working", "fix", "solution", "help", "doesn't work", "broken", "trouble"]):
            return "troubleshooting"
        
        # Check knowledge base for feature-related queries
        for feature, data in self.knowledge_base.items():
            if any(keyword in query_lower for keyword in data["keywords"]):
                return "feature_explanation"
        
        # Default to general guidance
        return "general_guidance"
    
    def get_feature_explanation(self, query: str) -> str:
        """
        Get an explanation for a specific feature based on the user's query.
        
        Args:
            query: The user's query about a feature
            
        Returns:
            Explanation of the requested feature
        """
        query_lower = query.lower()
        
        # Find the most relevant feature
        for feature, data in self.knowledge_base.items():
            if any(keyword in query_lower for keyword in data["keywords"]):
                return data["explanation"]
        
        # If no specific feature found, return general help
        return "I can help explain various features of the application. Try asking about specific features like creating tasks, editing tasks, setting priorities, or using tags."
    
    def get_troubleshooting_advice(self, query: str) -> str:
        """
        Get troubleshooting advice based on the user's query.
        
        Args:
            query: The user's query about an issue
            
        Returns:
            Troubleshooting advice for the issue
        """
        query_lower = query.lower()
        
        # Find the most relevant troubleshooting advice
        for feature, data in self.knowledge_base.items():
            if any(keyword in query_lower for keyword in data["keywords"]):
                return data["troubleshooting"]
        
        # Generic troubleshooting advice
        return "For general troubleshooting: 1. Refresh the page 2. Check your internet connection 3. Clear your browser cache 4. Try again. If the problem persists, contact support."
    
    def get_tutorial(self, query: str) -> str:
        """
        Get a step-by-step tutorial based on the user's query.
        
        Args:
            query: The user's query requesting a tutorial
            
        Returns:
            Step-by-step tutorial for the requested action
        """
        query_lower = query.lower()
        
        # Find the most relevant tutorial
        for feature, data in self.knowledge_base.items():
            if any(keyword in query_lower for keyword in data["keywords"]):
                return data["tutorial"]
        
        # Generic tutorial guidance
        return "I can provide step-by-step tutorials for various features. Try asking about specific actions like 'How to create a task?' or 'Show me how to edit a task.'"
    
    def get_developer_info(self) -> str:
        """
        Get information about the developer.
        
        Returns:
            Information about the developer with Islamic attribution
        """
        info = (
            f"This application was developed by {self.developer_info['name']}, a {self.developer_info['role']} "
            f"who participated in the {self.developer_info['hackathon']}. "
            f"He developed the {self.developer_info['project']} project using technologies like "
            f"{', '.join(self.developer_info['technologies'])}. "
            f"{self.developer_info['about']} "
            f"All praise and success is by ALLAH's will."
        )
        return info
    
    def get_general_guidance(self, query: str) -> str:
        """
        Provide general guidance when the query doesn't match specific categories.
        
        Args:
            query: The user's query
            
        Returns:
            General guidance response
        """
        return (
            "I'm here to help you with the TODO EVOLUTION application. "
            "You can ask me about specific features, troubleshooting issues, "
            "how-to guides, or information about the developer. "
            "What would you like to know?"
        )
    
    def process_guidance_request(self, query: str) -> Dict[str, str]:
        """
        Process a guidance request and return the appropriate response.
        
        Args:
            query: The user's query
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            # Check for signs of confusion in the query
            is_confused = self.detect_confusion(query)
            
            # Classify the query
            category = self.classify_query(query)
            
            # Generate response based on category
            if category == "feature_explanation":
                response = self.get_feature_explanation(query)
            elif category == "troubleshooting":
                response = self.get_troubleshooting_advice(query)
            elif category == "tutorial":
                response = self.get_tutorial(query)
            elif category == "developer_info":
                response = self.get_developer_info()
            else:
                response = self.get_general_guidance(query)
            
            # If user seems confused, add extra guidance
            if is_confused:
                response += " \n\nWould you like me to explain anything else in more detail? I'm here to help!"
            
            logger.info(f"Processed guidance request for category: {category}")
            
            return {
                "response": response,
                "category": category,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error processing guidance request: {str(e)}")
            return {
                "response": "I'm sorry, I encountered an error while processing your request. Please try again.",
                "category": "error",
                "success": False
            }
    
    def detect_confusion(self, query: str) -> bool:
        """
        Detect if the user seems confused based on their query.
        
        Args:
            query: The user's query
            
        Returns:
            Boolean indicating if the user seems confused
        """
        query_lower = query.lower()
        
        # Keywords that might indicate confusion
        confusion_indicators = [
            "confused", "don't understand", "unclear", "not sure", "how does this work",
            "what do I do", "help me", "explain", "what is", "how to", "where is",
            "why is", "can't find", "doesn't make sense", "lost", "stuck", "huh",
            "what", "pardon", "sorry", "repeat", "again", "please"
        ]
        
        # Check if any confusion indicators are in the query
        for indicator in confusion_indicators:
            if indicator in query_lower:
                return True
        
        # Check for question marks (multiple might indicate confusion)
        if query.count('?') > 1:
            return True
            
        # Check for repeated words which might indicate uncertainty
        words = query_lower.split()
        for i in range(len(words) - 1):
            if words[i] == words[i+1]:
                return True
        
        return False

# Global instance of the service
guidance_service = GuidanceService()

def get_guidance_service() -> GuidanceService:
    """
    Get the global instance of GuidanceService.
    
    Returns:
        GuidanceService instance
    """
    return guidance_service