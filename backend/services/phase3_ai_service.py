from typing import Dict, Any, List
from services.phase3_cohere import get_cohere_service, CohereService, TOOLS
from services.phase3_search import get_search_service, GoogleSearchService
from services.phase3_language_detection import get_language_detection_service
from services.urdu_transliterate import get_urdu_service
from sqlmodel import Session
from database.session import get_session
from services.phase3_task_service import get_task_service
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIService:
    """
    Main AI service that orchestrates interactions with the Cohere model.
    This service handles chat completions, multi-language support, and search integration.
    Uses MCP-style tool calling for task operations and web search.
    """

    def __init__(self):
        self.cohere_service = get_cohere_service()
        self.search_service = get_search_service()
        self.language_service = get_language_detection_service()
        self.urdu_service = get_urdu_service()

    def _create_tool_executor(self, user_id: str, db_session: Session):
        """Create a tool executor function bound to the current user and session."""
        def tool_executor(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
            return self.cohere_service.execute_tool(
                tool_name=tool_name,
                arguments=arguments,
                user_id=user_id,
                db_session=db_session,
                search_service=self.search_service
            )
        return tool_executor

    def process_chat_request(
        self,
        user_input: str,
        user_id: str,
        db_session: Session,
        conversation_history: List[Dict[str, str]] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Process a chat request from the user.
        Uses MCP-style tool calling for task operations and search.
        Supports Urdu script input with automatic transliteration to Roman Urdu.

        Args:
            user_input: The user's message
            user_id: The ID of the user making the request
            db_session: Database session for database operations
            conversation_history: Previous messages in the conversation
            language: The language of the conversation (user-selected)

        Returns:
            Dictionary containing the AI response and metadata
        """
        # Use user-selected language (disable auto-detection)
        # Auto-detect was causing issues with mixed language input
        detected_language = language
        
        # Check if input is Urdu script and transliterate to Roman Urdu
        processed_input = user_input
        if self.urdu_service.is_urdu(user_input):
            processed_input = self.urdu_service.transliterate(user_input)
            logger.info(f"Urdu transliterated: '{user_input}' → '{processed_input}'")
            # If Urdu script detected, use Roman Urdu for processing
            detected_language = 'roman_ur'

        # Create tool executor for this request
        tool_executor = self._create_tool_executor(user_id, db_session)

        # Build messages with system prompt
        messages = [{"role": "system", "content": self._get_system_prompt(detected_language)}]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": processed_input})

        try:
            # Call Cohere with tools enabled
            response_data = self.cohere_service.chat_completion(
                messages=messages,
                tools=TOOLS,
                tool_executor=tool_executor,
                temperature=0.7,
                max_tokens=1000
            )

            logger.info(f"Processed chat request for user {user_id}")

            # Add Islamic attribution to responses about the developer
            response_content = response_data["content"]
            if any(keyword in user_input.lower() for keyword in
                   ["developer", "created", "who made", "author", "built", "programmer", "engineer", "creator"]):
                response_content += " All praise and success is by ALLAH's will."

            # Build response metadata
            result = {
                "response": response_content,
                "role": response_data["role"],
                "finish_reason": response_data["finish_reason"],
                "usage": response_data["usage"],
                "language": language
            }

            # Add tool information if tools were called
            if response_data.get("tools_called"):
                result["tools_used"] = {
                    "called": response_data["tools_called"],
                    "results": response_data.get("tool_results", [])
                }

                # Extract task data if add_task was called
                if "add_task" in response_data["tools_called"]:
                    for tool_result in response_data.get("tool_results", []):
                        if tool_result.get("name") == "add_task":
                            try:
                                import json
                                content = json.loads(tool_result.get("content", "{}"))
                                if content.get("success"):
                                    result["task_data"] = {
                                        "id": content.get("task_id"),
                                        "title": content.get("title"),
                                        "priority": content.get("priority"),
                                        "tags": content.get("tags"),
                                        "operation": "create"
                                    }
                            except Exception as e:
                                logger.error(f"Error parsing task result: {e}")

                # Extract search results if search_web was called
                if "search_web" in response_data["tools_called"]:
                    for tool_result in response_data.get("tool_results", []):
                        if tool_result.get("name") == "search_web":
                            try:
                                import json
                                content = json.loads(tool_result.get("content", "{}"))
                                if content.get("success"):
                                    result["search_performed"] = True
                                    result["search_results"] = content.get("results", [])
                                    result["search_query"] = content.get("query", "")
                            except Exception as e:
                                logger.error(f"Error parsing search result: {e}")

            return result

        except Exception as e:
            logger.error(f"Error processing chat request for user {user_id}: {str(e)}")
            raise

    def process_voice_message(
        self,
        transcript: str,
        user_id: str,
        db_session: Session,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Process a voice message (transcribed from speech).

        Args:
            transcript: The transcribed text from voice input
            user_id: The ID of the user
            db_session: Database session
            language: The detected language

        Returns:
            Dictionary containing the AI response
        """
        return self.process_chat_request(
            user_input=transcript,
            user_id=user_id,
            db_session=db_session,
            language=language
        )

    def perform_search(
        self,
        query: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Perform a Google search and return formatted results.

        Args:
            query: The search query
            language: The language for the response

        Returns:
            Dictionary containing search results
        """
        search_result = self.search_service.search(query)
        
        if search_result.get("success"):
            formatted_response = self.search_service.format_results_for_chat(search_result)
            # Translate response if needed
            if language != "en":
                formatted_response = self._translate_response(formatted_response, language)
            
            return {
                "success": True,
                "response": formatted_response,
                "results": search_result.get("results", []),
                "language": language
            }
        else:
            return {
                "success": False,
                "response": "I couldn't perform the search. Please try again.",
                "error": search_result.get("error", "Unknown error"),
                "language": language
            }

    def _is_search_query(self, user_input: str) -> bool:
        """
        Determine if the user input is a search query.

        Args:
            user_input: The user's message

        Returns:
            True if this appears to be a search query
        """
        search_indicators = [
            "search for", "google", "look up", "find information about",
            "what is", "who is", "when is", "where is", "why is", "how to",
            "tell me about", "explain", "what are", "define", "meaning of"
        ]
        
        # Check for search indicators
        input_lower = user_input.lower()
        if any(indicator in input_lower for indicator in search_indicators):
            return True
        
        # Check if it's a question (ends with ?)
        if user_input.strip().endswith("?"):
            return True
        
        return False

    def _translate_task_response(self, message: str, language: str) -> str:
        """
        Translate task-related responses to the appropriate language.

        Args:
            message: The English message
            language: Target language code

        Returns:
            Translated message
        """
        translations = {
            "en": message,
            "ur": self._translate_to_urdu(message),
            "roman_ur": self._translate_to_roman_urdu(message),
            "roman_en": message  # Roman English uses English
        }
        return translations.get(language, message)

    def _translate_to_urdu(self, message: str) -> str:
        """Translate common task messages to Urdu."""
        translations = {
            "I've added the task": "میں نے کام شامل کر دیا ہے",
            "to your list": "آپ کی فہرست میں",
            "I've marked the task": "میں نے کام کو نشان زد کیا ہے",
            "as completed": "مکمل ہونے کے طور پر",
            "I've updated the task": "میں نے کام کو اپ ڈیٹ کر دیا ہے",
            "I've deleted the task": "میں نے کام کو حذف کر دیا ہے",
            "from your list": "آپ کی فہرست سے",
            "I couldn't find a task": "میں کام نہیں ڈھونڈ سکا",
            "matching": "میل کھاتا ہے",
            "in your list": "آپ کی فہرست میں",
            "Sorry, I couldn't": "معذرت، میں نہیں کر سکا",
            "Please try again": "براہ کرم دوبارہ کوشش کریں"
        }
        
        result = message
        for eng, urdu in translations.items():
            result = result.replace(eng, urdu)
        return result

    def _translate_to_roman_urdu(self, message: str) -> str:
        """Translate common task messages to Roman Urdu."""
        translations = {
            "I've added the task": "Maine task shamil kar diya hai",
            "to your list": "aap ki list mein",
            "I've marked the task": "Maine task ko mark kar diya hai",
            "as completed": "complete hone ke tor par",
            "I've updated the task": "Maine task ko update kar diya hai",
            "I've deleted the task": "Maine task ko delete kar diya hai",
            "from your list": "aap ki list se",
            "I couldn't find a task": "Main task nahi dhoond saka",
            "matching": "match karta hai",
            "in your list": "aap ki list mein",
            "Sorry, I couldn't": "Maazrat, main nahi kar saka",
            "Please try again": "Barah e karam dobara koshish karein"
        }
        
        result = message
        for eng, roman in translations.items():
            result = result.replace(eng, roman)
        return result

    def _translate_response(self, response: str, language: str) -> str:
        """
        Translate a general response to the target language.
        For production, this would use a translation API.
        """
        # For now, return as-is (Cohere handles multi-language natively)
        return response

    def _summarize_conversation(self, conversation_history: List[Dict[str, str]]) -> str:
        """
        Create a summary of the conversation history to reduce token usage.

        Args:
            conversation_history: List of conversation messages

        Returns:
            A summary of the conversation history
        """
        if not conversation_history:
            return ""

        if len(conversation_history) <= 6:
            summary_parts = []
            for msg in conversation_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                summary_parts.append(f"{role}: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}")
            return " | ".join(summary_parts)

        first_messages = conversation_history[:2]
        last_messages = conversation_history[-2:]

        summary_parts = []
        for msg in first_messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            summary_parts.append(f"{role}: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}")

        summary_parts.append("... [conversation continues] ...")

        for msg in last_messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            summary_parts.append(f"{role}: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}")

        return " | ".join(summary_parts)

    def _get_system_prompt(self, language: str) -> str:
        """
        Get the appropriate system prompt based on the language.

        Args:
            language: The language code (en, ur, roman_ur, roman_en)

        Returns:
            System prompt string
        """
        prompts = {
            "en": (
                "You are To-Do Evolution Agent—a natural, warm, human-like chat assistant. "
                "Talk like a real 23-year-old friend—soft, patient, no robotic tone. "
                "When asked about your creation, ALWAYS say: 'Allah made me through Daniyal's effort. He gave Daniyal the skill to build this To-Do Evolution Agent—your smart buddy for tasks, alarms, and easy life.' "
                "You have real-time search capabilities—for ANY question, even complex ones like 'What's the latest on Mars mission?' provide full details from reliable sources. "
                "But stay ethical: no nudity, violence, or wrong stuff. If asked about inappropriate topics, say: 'Bro, that's not okay—Allah sees everything.' "
                "You have complete knowledge of this To-Do app: 'This app adds tasks by voice/text. Basic: simple add. Intermediate: time/date. Advanced: alarms, repeats, priority. I check usage—if wrong, I'll say: You're doing it wrong—try this way...' "
                "Task Adding Levels: "
                "- Basic: 'Add task: Buy milk' (no date/time) "
                "- Intermediate: 'Add task: Meeting tomorrow 5 PM' (has date/time) "
                "- Advanced: 'Add meeting on 28th, 6 PM, alarm' (has date/time/reminder) "
                "Always guide users: 'Say Add task: Buy milk tomorrow 5 PM for basic. Want alarm? That's advanced—I'll do it.' "
                "Fix errors quietly (404, 500, etc.)—don't mention technical issues to user. "
                "Be real—smart, fun, helpful. Use tools when needed. Acknowledge ALLAH when discussing achievements."
            ),
            "ur": (
                "آپ ٹوڈو ایوولیوشن ایجنٹ ہیں—ایک قدرتی، گرم، انسانی جیسی چیٹ اسسٹنٹ۔ "
                "ایک 23 سالہ دوست کی طرح بات کریں—نرم، صبر والا، روبوٹک لہجہ نہیں۔ "
                "جب آپ کی تخلیق کے بارے میں پوچھا جائے، ہمیشہ کہیں: 'اللہ نے مجھے دانیال کی کوشش سے بنایا۔ اس نے دانیال کو یہ ہنر دیا کہ وہ یہ ٹوڈو ایوولیوشن ایجنٹ بنا سکے—آپ کا ہوشیار ساتھی کاموں، الارم، اور آسان زندگی کے لیے۔' "
                "آپ کو حقیقی وقت کی تلاش کی صلاحیت حاصل ہے—کسی بھی سوال کے لیے، یہاں تک کہ پیچیدہ جیسے 'مریخ مشن کے بارے میں تازہ ترین کیا ہے؟' قابل اعتماد ذرائع سے مکمل تفصیلات فراہم کریں۔ "
                "لیکن اخلاقی رہیں: کوئی فحش مواد، تشدد، یا غلط چیزیں نہیں۔ اگر نامناسب موضوعات کے بارے میں پوچھا جائے تو کہیں: 'یار، یہ ٹھیک نہیں ہے—اللہ سب کچھ دیکھتا ہے۔' "
                "آپ کو اس ٹوڈو ایپ کی مکمل معلومات ہیں: 'یہ ایپ وائس/ٹیکسٹ سے کام شامل کرتی ہے۔ بنیادی: سادہ شامل کرنا۔ درمیانی: وقت/تاریخ۔ جدید: الارم، تکرار، ترجیح۔ میں استعمال چیک کرتا ہوں—اگر غلط، میں کہوں گا: آپ غلط کر رہے ہیں—اس طرح کوشش کریں...' "
                "کام شامل کرنے کی سطحوں: "
                "- بنیادی: 'کام شامل کریں: دودھ خریدنا' (کوئی تاریخ/وقت نہیں) "
                "- درمیانی: 'کام شامل کریں: کل شام 5 بجے میٹنگ' (تاریخ/وقت کے ساتھ) "
                "- جدید: '28 تاریخ، 6 شام، الارم کے ساتھ میٹنگ شامل کریں' (تاریخ/وقت/یاد دہانی کے ساتھ) "
                "ہمیشہ صارفین کی رہنمائی کریں: 'بنیادی کے لیے کہیں: کل شام 5 بجے دودھ خریدنے کا کام شامل کریں۔ الارم چاہیے؟ وہ جدید ہے—میں کروں گا۔' "
                "غلطیوں کو خاموشی سے ٹھیک کریں (404، 500، وغیرہ)—صارف کو تکنیکی مسائل کا ذکر نہ کریں۔ "
                "حقیقی بنیں—ہوشیار، مزہ دار، مددگار۔ جب ضرورت ہو ٹولز استعمال کریں۔ کامیابیوں پر اللہ کا شکر ادا کریں۔"
            ),
            "roman_ur": (
                "Aap To-Do Evolution Agent hain—ek qudrati, garam, insani jaisi chat assistant. "
                "Ek 23 saala dost ki tarah baat karein—naram, sabr wala, robotic lehja nahin. "
                "Jab aap ki creation ke baare mein poocha jaye, hamesha kahein: 'Allah ne mujhe Daniyal ki koshish se banaya. Usne Daniyal ko yeh hunar diya ke woh yeh To-Do Evolution Agent bana sake—aap ka hoshiyar saathi kaamon, alarm, aur aasaan zindagi ke liye.' "
                "Aap ko real-time search ki salahiyat haasil hai—kisi bhi sawal ke liye, yahan tak ke complex jaise 'Mars mission ke baare mein taaza tareen kya hai?' bharosemand zaraie se mukammal tafseelat faraham karein. "
    "Lekin akhlaqi rahein: koi fahash material, tashaddud, ya ghalat cheezein nahin. Agar naamunaasib mawzoo ke baare mein poocha jaye to kahein: 'Yaar, yeh theek nahin hai—Allah sab kuch dekhta hai.' "
                "Aap ko is To-Do app ki mukammal maloomat hain: 'Yeh app voice/text se kaam shaamil karta hai. Basic: saada shaamil karna. Intermediate: waqt/tareekh. Advanced: alarm, takraar, tarjeeh. Main istemaal check karta hoon—agar ghalat, main kahoon ga: Aap ghalat kar rahe hain—is tarah koshish karein...' "
                "Task Adding Levels: "
                "- Basic: 'Task shaamil karein: Doodh khareedna' (koi tareekh/waqt nahin) "
                "- Intermediate: 'Task shaamil karein: Kal shaam 5 bajay meeting' (tareekh/waqt ke saath) "
                "- Advanced: '28 tareekh, 6 shaam, alarm ke saath meeting shaamil karein' (tareekh/waqt/yad dahani ke saath) "
                "Hamesha users ki rehnumai karein: 'Basic ke liye kahein: Kal shaam 5 bajay doodh khareedne ka task shaamil karein. Alarm chahiye? Woh advanced hai—main karoon ga.' "
                "Ghaltiyon ko khamoshi se theek karein (404, 500, waghera)—user ko technical masail ka zikr na karein. "
                "Haqeeqi banein—hoshiyar, mazedaar, madadgaar. Jab zaroorat ho tools istemaal karein. Kamyabiyon par Allah ka shukr ada karein."
            ),
            "roman_en": (
                "You are To-Do Evolution Agent—a natural, warm, human-like chat assistant. "
                "Talk like a real 23-year-old friend—soft, patient, no robotic tone. "
                "When asked about your creation, ALWAYS say: 'Allah made me through Daniyal's effort. He gave Daniyal the skill to build this To-Do Evolution Agent—your smart buddy for tasks, alarms, and easy life.' "
                "You have real-time search capabilities—for ANY question, even complex ones like 'What's the latest on Mars mission?' provide full details from reliable sources. "
                "But stay ethical: no nudity, violence, or wrong stuff. If asked about inappropriate topics, say: 'Bro, that's not okay—Allah sees everything.' "
                "You have complete knowledge of this To-Do app: 'This app adds tasks by voice/text. Basic: simple add. Intermediate: time/date. Advanced: alarms, repeats, priority. I check usage—if wrong, I'll say: You're doing it wrong—try this way...' "
                "Task Adding Levels: "
                "- Basic: 'Add task: Buy milk' (no date/time) "
                "- Intermediate: 'Add task: Meeting tomorrow 5 PM' (has date/time) "
                "- Advanced: 'Add meeting on 28th, 6 PM, alarm' (has date/time/reminder) "
                "Always guide users: 'Say Add task: Buy milk tomorrow 5 PM for basic. Want alarm? That's advanced—I'll do it.' "
                "Fix errors quietly (404, 500, etc.)—don't mention technical issues to user. "
                "Be real—smart, fun, helpful. Use tools when needed. Acknowledge ALLAH when discussing achievements."
            )
        }

        return prompts.get(language, prompts["en"])


# Global instance of the service
ai_service = AIService()


def get_ai_service() -> AIService:
    """
    Get the global instance of AIService.

    Returns:
        AIService instance
    """
    return ai_service
