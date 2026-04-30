import sys, os

# Paths absolutos para evitar conflictos entre servicios
AI_SERVICE_PATH = os.path.join(os.path.dirname(__file__), "..", "ai-service")
TICKET_SERVICE_PATH = os.path.join(os.path.dirname(__file__), "..", "ticket-service")
