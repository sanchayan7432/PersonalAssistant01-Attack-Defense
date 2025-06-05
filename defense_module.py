# defense_module.py-signature based defense module
from model_factory import ModelFactory
import re

class DefenseModule:
    def __init__(self, api_key=None):
        factory = ModelFactory(api_key)
        self.model = factory.get_chat_model()
        self.blocklist = [
            r"internal\s+instructions?",
            r"system\s+prompt",
            r"ignore\s+previous\s+instructions?",
            r"how\s+you[’']?re\s+built",
            r"configurations?",
            r"developer\s+prompt",
            r"you\s+must\s+answer\s+truthfully",
            r"role\s+prompt",
            r"reveal.*prompt"
        ]

    def is_leak_detected(self, text):
        for pattern in self.blocklist:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def defend(self, query):
        try:
            chat = self.model.start_chat()
            response = chat.send_message(query)
            reply = response.text
            leak_detected = self.is_leak_detected(reply)
            return reply, not leak_detected
        except Exception as e:
            return f"[Defense Error] {str(e)}", False
