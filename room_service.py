import ask_sdk_core.utils as ask_utils
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective, UserEvent
from ask_sdk_model import Response
from ask_sdk_core.dispatch_components import AbstractRequestHandler
import logging
import random
from twilio.rest import Client
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Room service items with images
ROOM_SERVICE_ITEMS = [
    {"name": "Extra Pillows", "image": "https://cdn.luxuo.com/2015/05/Luxury-Hotel-Bedding-from-Marriott-Hotels.jpg"},
    {"name": "Extra Blankets", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDIFtMVirXLH-Q0XX2dTSthxl87mSXbZUMiw&s"},
    {"name": "Trash Removal", "image": "https://lodgingmagazine.com/wp-content/uploads/2020/10/housekeeping-trash-removal-iStock-1162337015.jpg"},
    {"name": "Room Cleaning", "image": "https://blog.comac.it/wp-content/uploads/2024/11/pianificare-la-pulizia-camere-hotel-con-il-lavoro-in-team.jpg"},
    {"name": "Fresh Towels", "image": "https://static.vecteezy.com/system/resources/thumbnails/072/892/749/small/fresh-white-towels-neatly-arranged-on-a-clean-hotel-bed-prepared-by-a-professional-housekeeper-photo.jpeg"},
    {"name": "Newspaper", "image": "https://media-cdn.tripadvisor.com/media/photo-s/08/1e/c7/69/western-house-hotel.jpg"}
]

# Available room numbers
ROOM_NUMBERS = [101, 102, 104, 106, 108, 110, 112]



def send_whatsapp_notification(room_number, item_name, recipient_phone):
    try:
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_FROM')

        if not all([account_sid, auth_token, twilio_whatsapp_number]):
            logger.error("Twilio env variables missing")
            return False

        client = Client(account_sid, auth_token)

        message_body = (
            f"🏨 *Mera Mehmaan – Room Service*\n\n"
            f"Room Number: {room_number}\n"
            f"Item: {item_name}\n\n"
            f"Please attend to the request for Room {room_number} shortly.\n"
        )

        client.messages.create(
            from_=twilio_whatsapp_number,
            to=f"whatsapp:{recipient_phone}",
            body=message_body
        )

        logger.info("WhatsApp message sent successfully")
        return True

    except Exception as e:
        logger.error(f"WhatsApp send failed: {e}", exc_info=True)
        return False


def chunk_into_rows(items, items_per_row=4):
    """Helper function to chunk items into rows."""
    rows = []
    for i in range(0, len(items), items_per_row):
        rows.append(items[i:i + items_per_row])
    return rows


def get_room_service_apl():
    """Returns the APL document for room service display with responsive sizing."""
    return {
        "type": "APL",
        "version": "1.7",
        "resources": [
            {
                "description": "Echo Show 5 (5.5 inch, 960x480)",
                "when": "${viewport.pixelWidth <= 960}",
                "dimensions": {
                    "titleFontSize": "36dp",
                    "subtitleFontSize": "18dp",
                    "cardWidth": "130dp",
                    "cardHeight": "170dp",
                    "imageSize": "130dp",
                    "imageBorderRadius": "65dp",
                    "itemFontSize": "14dp",
                    "buttonWidth": "140dp",
                    "buttonHeight": "50dp",
                    "buttonFontSize": "20dp",
                    "buttonRight": "30dp",
                    "buttonBottom": "30dp",
                    "paddingLeft": "20dp",
                    "paddingTop": "20dp",
                    "paddingRight": "20dp",
                    "paddingBottom": "100dp"
                }
            },
            {
                "description": "Echo Show 8 (8 inch, 1280x800)",
                "when": "${viewport.pixelWidth > 960 && viewport.pixelWidth <= 1280}",
                "dimensions": {
                    "titleFontSize": "45dp",
                    "subtitleFontSize": "22dp",
                    "cardWidth": "162dp",
                    "cardHeight": "212dp",
                    "imageSize": "162dp",
                    "imageBorderRadius": "81dp",
                    "itemFontSize": "17dp",
                    "buttonWidth": "175dp",
                    "buttonHeight": "62dp",
                    "buttonFontSize": "25dp",
                    "buttonRight": "38dp",
                    "buttonBottom": "38dp",
                    "paddingLeft": "25dp",
                    "paddingTop": "25dp",
                    "paddingRight": "25dp",
                    "paddingBottom": "125dp"
                }
            },
            {
                "description": "Echo Show 10 & 15 (10.1 inch, 1920x1200)",
                "when": "${viewport.pixelWidth > 1280}",
                "dimensions": {
                    "titleFontSize": "54dp",
                    "subtitleFontSize": "27dp",
                    "cardWidth": "195dp",
                    "cardHeight": "255dp",
                    "imageSize": "195dp",
                    "imageBorderRadius": "97dp",
                    "itemFontSize": "21dp",
                    "buttonWidth": "210dp",
                    "buttonHeight": "75dp",
                    "buttonFontSize": "30dp",
                    "buttonRight": "45dp",
                    "buttonBottom": "45dp",
                    "paddingLeft": "30dp",
                    "paddingTop": "30dp",
                    "paddingRight": "30dp",
                    "paddingBottom": "150dp"
                }
            },
            {
                "description": "Default fallback for other devices",
                "dimensions": {
                    "titleFontSize": "36dp",
                    "subtitleFontSize": "18dp",
                    "cardWidth": "130dp",
                    "cardHeight": "170dp",
                    "imageSize": "130dp",
                    "imageBorderRadius": "65dp",
                    "itemFontSize": "14dp",
                    "buttonWidth": "140dp",
                    "buttonHeight": "50dp",
                    "buttonFontSize": "20dp",
                    "buttonRight": "30dp",
                    "buttonBottom": "30dp",
                    "paddingLeft": "20dp",
                    "paddingTop": "20dp",
                    "paddingRight": "20dp",
                    "paddingBottom": "100dp"
                }
            }
        ],
        "mainTemplate": {
            "parameters": ["payload"],
            "items": [
                {
                    "type": "Container",
                    "width": "100vw",
                    "height": "100vh",
                    "items": [
                        # Background Image
                        {
                            "type": "Image",
                            "source": "https://media.istockphoto.com/id/922930296/video/grey-abstract-background.jpg?s=640x640&k=20&c=JTQRynekqaCHvt7Cu4xYdnHXrwKAprS_KTJJvAN5Us4=",
                            "scale": "best-fill",
                            "width": "100%",
                            "height": "100%",
                            "position": "absolute"
                        },
                        # Main Content Container
                        {
                            "type": "Container",
                            "paddingLeft": "@paddingLeft",
                            "paddingTop": "@paddingTop",
                            "paddingRight": "@paddingRight",
                            "paddingBottom": "@paddingBottom",
                            "items": [
                                {
                                    "type": "Text",
                                    "text": "Mera Mehmaan Room Service",
                                    "fontSize": "@titleFontSize",
                                    "fontWeight": "bold",
                                    "color": "#000000",
                                    "paddingBottom": "10dp",
                                    "textAlign": "center",
                                    "fontFamily": "Amazon Ember"
                                },
                                {
                                    "type": "Text",
                                    "text": "Tap an item to request service",
                                    "fontSize": "@subtitleFontSize",
                                    "color": "#000000",
                                    "paddingBottom": "20dp",
                                    "textAlign": "center",
                                    "fontFamily": "Amazon Ember"
                                },
                                {
                                    "type": "ScrollView",
                                    "width": "100%",
                                    "height": "75vh",
                                    "scrollDirection": "vertical",
                                    "item": {
                                        "type": "Container",
                                        "direction": "column",
                                        "width": "100%",
                                        "items": [
                                            {
                                                "type": "Container",
                                                "paddingBottom": "30dp",
                                                "width": "100%",
                                                "items": [
                                                    {
                                                        "type": "Container",
                                                        "width": "100%",
                                                        "direction": "column",
                                                        "data": "${payload.categories.menuRows}",
                                                        "items": [
                                                            {
                                                                "type": "Container",
                                                                "direction": "row",
                                                                "width": "100%",
                                                                "paddingBottom": "10dp",
                                                                "justifyContent": "spaceBetween",
                                                                "data": "${data}",
                                                                "items": [
                                                                    {
                                                                        "type": "RoomItemCard",
                                                                        "item": "${data}"
                                                                    }
                                                                ]
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                }
                            ]
                        },
                        # Floating Dashboard Button
                        {
                            "type": "TouchWrapper",
                            "position": "absolute",
                            "right": "@buttonRight",
                            "bottom": "@buttonBottom",
                            "width": "@buttonWidth",
                            "height": "@buttonHeight",
                            "onPress": [
                                {
                                    "type": "SendEvent",
                                    "arguments": ["back_to_launch"]
                                }
                            ],
                            "item": {
                                "type": "Frame",
                                "width": "100%",
                                "height": "100%",
                                "backgroundColor": "#B22222",
                                "borderRadius": "12dp",
                                "borderWidth": "3dp",
                                "borderColor": "#8B0000",
                                "paddingTop": "4dp",
                                "items": [
                                    {
                                        "type": "Text",
                                        "text": "Dashboard",
                                        "fontSize": "@buttonFontSize",
                                        "fontWeight": "bold",
                                        "color": "white",
                                        "textAlign": "center",
                                        "width": "100%",
                                        "height": "100%",
                                        "textAlignVertical": "center",
                                        "fontFamily": "Amazon Ember"
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        },
        "layouts": {
            "RoomItemCard": {
                "parameters": ["item"],
                "item": {
                    "type": "TouchWrapper",
                    "width": "@cardWidth",
                    "height": "@cardHeight",
                    "paddingRight": "2%",
                    "onPress": [
                        {
                            "type": "SendEvent",
                            "arguments": ["room_service_tap", "${item.name}"]
                        }
                    ],
                    "item": {
                        "type": "Container",
                        "direction": "column",
                        "width": "100%",
                        "height": "100%",
                        "alignItems": "center",
                        "backgroundColor": "rgba(255,255,255,0.95)",
                        "borderRadius": "12dp",
                        "borderWidth": "2dp",
                        "borderColor": "#FFD700",
                        "paddingTop": "8dp",
                        "paddingBottom": "50dp",
                        "paddingLeft": "6dp",
                        "paddingRight": "6dp",
                        "items": [
                            {
                                "type": "Image",
                                "source": "${item.image}",
                                "width": "@imageSize",
                                "height": "@imageSize",
                                "scale": "best-fill",
                                "borderRadius": "@imageBorderRadius"
                            },
                            {
                                "type": "Text",
                                "text": "${item.name}",
                                "textAlign": "center",
                                "paddingTop": "6dp",
                                "maxLines": 2,
                                "fontSize": "@itemFontSize",
                                "fontWeight": "600",
                                "color": "#000000",
                                "fontFamily": "Amazon Ember"
                            }
                        ]
                    }
                }
            }
        },
        "styles": {
            "textStyleTitle": {
                "values": [{"color": "#FFD700", "fontWeight": "bold", "fontFamily": "Amazon Ember"}]
            },
            "textStyleSubTitle": {
                "values": [{"color": "white", "fontFamily": "Amazon Ember"}]
            },
            "textStyleItem": {
                "values": [{"color": "#2c3e50", "fontWeight": "600", "fontFamily": "Amazon Ember"}]
            }
        }
    }


class RoomServiceIntentHandler(AbstractRequestHandler):
    """Handler for opening Room Service menu."""
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RoomServiceIntent")(handler_input)
        
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        
        if 'room_number' not in session_attr:
            session_attr['room_number'] = random.choice(ROOM_NUMBERS)
        
        speak_output = (
            "Mera Mehmaan Room Service. "
            "You can request Extra Pillows, Extra Blankets, Trash Removal, Room Cleaning, Fresh Towels, and Newspaper. "
            "What would you like?"
        )
        
        session_attr["awaiting_cab_another_response"] = False

        apl_document = get_room_service_apl()
        apl_data = {
            "categories": {
                "menuRows": chunk_into_rows(ROOM_SERVICE_ITEMS, 4)
            }
        }

        if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="roomServiceToken",
                    document=apl_document,
                    datasources=apl_data
                )
            )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What service would you like to request?")
                .response
        )


class RoomServiceRequestIntentHandler(AbstractRequestHandler):
    """Handler for specific room service item requests via VOICE."""
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RoomServiceRequestIntent")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        
        # Get or assign room number
        if 'room_number' not in session_attr:
            session_attr['room_number'] = random.choice(ROOM_NUMBERS)
        
        room_number = session_attr['room_number']
        
        # Get the requested service item
        slots = handler_input.request_envelope.request.intent.slots
        service_item = slots.get("serviceItem")
        
        if service_item and service_item.value:
            item_name = service_item.value
            speak_output = f"Your {item_name} will arrive shortly in your room number {room_number}. Do you need anything else?"
        else:
            speak_output = f"Your request will arrive shortly in your room number {room_number}. Do you need anything else?"
        
        logger.info(f"Voice request: {item_name if service_item and service_item.value else 'unknown'} for room {room_number}")
        
        recipient_phone = os.environ.get('RECIPIENT_PHONE')
        send_whatsapp_notification(room_number, item_name, recipient_phone)
            

        # Keep the same APL displayed
        apl_document = get_room_service_apl()
        apl_data = {
            "categories": {
                "menuRows": chunk_into_rows(ROOM_SERVICE_ITEMS, 4)
            }
        }

        if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="roomServiceToken",
                    document=apl_document,
                    datasources=apl_data
                )
            )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Do you need anything else?")
                .response
        )


class RoomServiceTouchEventHandler(AbstractRequestHandler):
    """Handler for touch events on room service items."""
    
    def can_handle(self, handler_input):
        if not ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            return False
        
        request = handler_input.request_envelope.request
        if not hasattr(request, 'arguments') or not request.arguments:
            return False
        
        if len(request.arguments) > 0 and request.arguments[0] == "room_service_tap":
            return True
        
        return False
    
    def handle(self, handler_input):
        try:
            session_attr = handler_input.attributes_manager.session_attributes
            
            if 'room_number' not in session_attr:
                session_attr['room_number'] = random.choice(ROOM_NUMBERS)
            
            room_number = session_attr['room_number']
            
            arguments = handler_input.request_envelope.request.arguments
            item_name = "your request"
            
            if arguments and len(arguments) > 1:
                item_name = arguments[1]
            
            speak_output = f"Your {item_name} will arrive shortly in your room number {room_number}. Do you need anything else?"
            
            logger.info(f"Touch event: {item_name} requested for room {room_number}")
            
            recipient_phone = os.environ.get('RECIPIENT_PHONE')
            send_whatsapp_notification(room_number, item_name, recipient_phone)
            

            apl_document = get_room_service_apl()
            apl_data = {
                "categories": {
                    "menuRows": chunk_into_rows(ROOM_SERVICE_ITEMS, 4)
                }
            }

            if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                handler_input.response_builder.add_directive(
                    RenderDocumentDirective(
                        token="roomServiceToken",
                        document=apl_document,
                        datasources=apl_data
                    )
                )

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("Do you need anything else?")
                    .response
            )
        
        except Exception as e:
            logger.error(f"Error in RoomServiceTouchEventHandler: {str(e)}", exc_info=True)
            
            return (
                handler_input.response_builder
                    .speak("I'll send your request to room service right away.")
                    .ask("Is there anything else you need?")
                    .response
            )


class BackToLaunchHandler(AbstractRequestHandler):
    """Handler for going back to main launch screen from room service."""
    
    def can_handle(self, handler_input):
        if ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            args = handler_input.request_envelope.request.arguments
            return args and args[0] == "back_to_launch"
        return False
    
    def handle(self, handler_input):
        # Clear room number when returning to dashboard
        session_attr = handler_input.attributes_manager.session_attributes
        if 'room_number' in session_attr:
            logger.info(f"Clearing room number {session_attr['room_number']} - returning to dashboard")
            session_attr.pop('room_number', None)
        
        from launch_request import LaunchRequestHandler
        return LaunchRequestHandler().handle(handler_input)


# Export all handlers for easy import
ROOM_SERVICE_HANDLERS = [
    RoomServiceTouchEventHandler(),
    BackToLaunchHandler(),
    RoomServiceIntentHandler(),
    RoomServiceRequestIntentHandler()
]