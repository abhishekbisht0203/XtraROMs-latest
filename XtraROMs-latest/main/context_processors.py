# myapp/context_processors.py

from django.contrib.messages import get_messages
import json

def serialized_messages(request):
    messages = get_messages(request)
    serialized_messages = [{'message': message.message, 'level': message.level} for message in messages]
    return {"serialized_messages": json.dumps(serialized_messages)}
