import random
import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from twilio.rest import Client
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --------------------------------------------------
# APL SUPPORT CHECK
# --------------------------------------------------

def supports_apl(handler_input):
    try:
        interfaces = handler_input.request_envelope.context.system.device.supported_interfaces
        return hasattr(interfaces, "alexa_presentation_apl")
    except Exception:
        return False

# --------------------------------------------------
# UNIVERSAL APL DOCUMENT
# --------------------------------------------------

def get_universal_apl():
    return {
        "type": "APL",
        "version": "1.8",
        "mainTemplate": {
            "parameters": ["payload"],
            "items": [
                {
                    "type": "Container",
                    "width": "100vw",
                    "height": "100vh",
                    "items": [
                        {
                            "type": "Image",
                            "source": "${payload.ui.background}",
                            "width": "100vw",
                            "height": "100vh",
                            "scale": "best-fill",
                            "position": "absolute",
                            "overlayColor": "rgba(0,0,0,0.7)"
                        },
                        {
                            "type": "Container",
                            "width": "100vw",
                            "height": "100vh",
                            "direction": "column",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "items": [
                                {
                                    "type": "Text",
                                    "text": "${payload.ui.title}",
                                    "fontSize": "60dp",
                                    "fontWeight": "bold",
                                    "color": "${payload.ui.titleColor}",
                                    "textAlign": "center"
                                },
                                {
                                    "type": "Text",
                                    "text": "${payload.ui.subtitle}",
                                    "fontSize": "42dp",
                                    "color": "#FFFFFF",
                                    "textAlign": "center",
                                    "paddingTop": "20dp"
                                },
                                {
                                    "type": "Text",
                                    "text": "${payload.ui.footer}",
                                    "fontSize": "32dp",
                                    "color": "#000000",
                                    "textAlign": "center",
                                    "paddingTop": "25dp"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }

# --------------------------------------------------
# APL RENDER HELPER
# --------------------------------------------------

def render_apl(handler_input, title, subtitle, footer,
               background="https://media.istockphoto.com/id/922930296/video/grey-abstract-background.jpg?s=640x640&k=20&c=JTQRynekqaCHvt7Cu4xYdnHXrwKAprS_KTJJvAN5Us4=",
               title_color="#FFD700"):
    if not supports_apl(handler_input):
        return

    handler_input.response_builder.add_directive(
        RenderDocumentDirective(
            token="universalAPL",
            document=get_universal_apl(),
            datasources={
                "ui": {
                    "title": title,
                    "subtitle": subtitle,
                    "footer": footer,
                    "background": background,
                    "titleColor": title_color
                }
            }
        )
    )

# --------------------------------------------------
# LAUNCH REQUEST
# --------------------------------------------------

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Welcome to Mera Mehmaan. "
            "You can say book a cab to get started."
        )

        render_apl(
            handler_input,
            title="Welcome to Mera Mehmaan",
            subtitle="Luxury | Comfort | Service",
            footer="Say 'Book a cab' to continue"
        )

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("How can I help you?")
            .response
        )

# --------------------------------------------------
# BOOK CAB (STEP 1)
# --------------------------------------------------

class BookCabIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CabBookIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        room_number = random.choice([101, 103, 105, 108, 110, 114, 117])
        session_attr["cab_room_number"] = room_number


        session_attr.pop("cab_destination", None)
        session_attr["cab_booking_active"] = True
            
        speak_output = "Sure. Where would you like to go?"

        render_apl(
            handler_input,
            title="Booking Your Cab",
            subtitle="Where would you like to go?",
            footer="Tell me your destination"
        )

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Please tell me your destination.")
            .response
        )

# --------------------------------------------------
# DESTINATION (STEP 2)
# --------------------------------------------------

class ProvideDestinationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CabDestinationIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        destination = "your destination"
        slots = handler_input.request_envelope.request.intent.slots
        if slots.get("destination") and slots["destination"].value:
            destination = slots["destination"].value

        session_attr["destination"] = destination

        speak_output = f"At what time should I book the cab to {destination}?"

        render_apl(
            handler_input,
            title="Booking Your Cab",
            subtitle=f"Destination: {destination}",
            footer="What time should I book?"
        )

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Please tell me the pickup time.")
            .response
        )

# --------------------------------------------------
# TIME + CONFIRMATION (STEP 3)
# --------------------------------------------------
def send_cab_booking_whatsapp(room_number, destination, pickup_time):
    """Send WhatsApp notification for cab booking confirmation."""
    try:
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_FROM')
        recipient_phone = os.environ.get('RECIPIENT_PHONE')

        if not all([account_sid, auth_token, twilio_whatsapp_number, recipient_phone]):
            logger.error("Twilio env variables missing (SID, Token, From, or Recipient Phone)")
            return False

        client = Client(account_sid, auth_token)

        message_body = (
            f"🚕 *Mera Mehmaan – Cab Booking*\n\n"
            f"Room Number: {room_number}\n"
            f"Destination: {destination}\n"
            f"Pickup Time: {pickup_time}\n\n"
            f"✅ *BOOKING CONFIRMED*\n\n"
            f"⏰ Cab confirmed for Room {room_number}. Pickup shortly.\n\n"
        )

        client.messages.create(
            from_=twilio_whatsapp_number,
            to=f"whatsapp:{recipient_phone}",
            body=message_body
        )

        logger.info(f"Cab booking WhatsApp sent successfully to {recipient_phone} for room {room_number}")
        return True

    except Exception as e:
        logger.error(f"Cab booking WhatsApp send failed: {e}", exc_info=True)
        return False

class ProvideTimeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CabTimeIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        pickup_time = "the specified time"
        slots = handler_input.request_envelope.request.intent.slots
        if slots.get("time") and slots["time"].value:
            pickup_time = slots["time"].value

        destination = session_attr.get("destination", "your destination")
        room_number = session_attr.get("cab_room_number", "your room")

        # Send WhatsApp notification before confirming
        logger.info(f"Sending cab booking confirmation to WhatsApp for room {room_number}")
        send_cab_booking_whatsapp(room_number, destination, pickup_time)
                
        session_attr["awaiting_cab_another_response"] = True

        speak_output = (
            f"Your cab to {destination} from room {room_number} "
            f"is booked at {pickup_time}. "
            "Please be ready fifteen minutes early. "
            "Would you like to book another cab?"
        )

        render_apl(
            handler_input,
            title="Cab Booking Confirmed",
            subtitle=f"{destination} • Room {room_number}",
            footer=f"Pickup Time: {pickup_time}",
            title_color="#00FF00"
        )

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Would you like to book another cab?")
            .response
        )

# --------------------------------------------------
# ERROR HANDLER
# --------------------------------------------------

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        return (
            handler_input.response_builder
            .speak("Sorry, something went wrong. Please try again.")
            .ask("What would you like to do?")
            .response
        )

# --------------------------------------------------
# SKILL BUILDER
# --------------------------------------------------

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BookCabIntentHandler())
sb.add_request_handler(ProvideDestinationIntentHandler())
sb.add_request_handler(ProvideTimeIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
