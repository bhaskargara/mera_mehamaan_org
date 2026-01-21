import ask_sdk_core.utils as ask_utils
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from ask_sdk_model import Response
from ask_sdk_core.dispatch_components import AbstractRequestHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from room_service import RoomServiceIntentHandler

# Phone Number Input APL Document with Background Image
PHONE_INPUT_APL = {
    "type": "APL",
    "version": "1.7",
    "theme": "dark",
    "resources": [
        {
            "description": "Echo Show 5 (5.5 inch, 960x480)",
            "when": "${viewport.pixelWidth == 960 && viewport.pixelHeight == 480}",
            "dimensions": {
                "inputWidth": "350dp",
                "inputHeight": "60dp",
                "buttonWidth": "200dp",
                "buttonHeight": "60dp",
                "fontSize": "22dp",
                "titleFontSize": "42dp",
                "subtitleFontSize": "18dp"
            }
        },
        {
            "description": "Echo Show 8 (8 inch, 1280x800)",
            "when": "${viewport.pixelWidth == 1280 && viewport.pixelHeight == 800}",
            "dimensions": {
                "inputWidth": "450dp",
                "inputHeight": "70dp",
                "buttonWidth": "250dp",
                "buttonHeight": "70dp",
                "fontSize": "26dp",
                "titleFontSize": "52dp",
                "subtitleFontSize": "22dp"
            }
        },
        {
            "description": "Echo Show 10 & 15 (10.1 inch, 1920x1200)",
            "when": "${viewport.pixelWidth == 1920 && viewport.pixelHeight == 1200}",
            "dimensions": {
                "inputWidth": "550dp",
                "inputHeight": "80dp",
                "buttonWidth": "300dp",
                "buttonHeight": "80dp",
                "fontSize": "30dp",
                "titleFontSize": "62dp",
                "subtitleFontSize": "26dp"
            }
        },
        {
            "description": "Default fallback",
            "dimensions": {
                "inputWidth": "400dp",
                "inputHeight": "60dp",
                "buttonWidth": "200dp",
                "buttonHeight": "60dp",
                "fontSize": "24dp",
                "titleFontSize": "48dp",
                "subtitleFontSize": "20dp"
            }
        }
    ],
    "styles": {
        "textStyleTitle": {
            "values": [{
                "color": "#FFFFFF",
                "fontWeight": "bold",
                "fontSize": "@titleFontSize",
                "textAlign": "center",
                "fontFamily": "Amazon Ember Display"
            }]
        },
        "textStyleSubtitle": {
            "values": [{
                "color": "#FFFFFF",
                "fontWeight": "400",
                "fontSize": "@subtitleFontSize",
                "textAlign": "center",
                "fontFamily": "Amazon Ember"
            }]
        }
    },
    "mainTemplate": {
        "parameters": ["payload"],
        "bind": [
            {
                "name": "phoneInputValue",
                "value": "",
                "type": "string"
            }
        ],
        "items": [{
            "type": "Container",
            "width": "100vw",
            "height": "100vh",
            "items": [
                {
                    "type": "Image",
                    "source": "https://res.cloudinary.com/dysbwjj9u/image/upload/v1767877878/Create_a_modern_202601081817-removebg-preview_gruopj.png",
                    "width": "100%",
                    "height": "100%",
                    "scale": "best-fill",
                    "position": "absolute",
                    "overlayColor": "rgba(0, 0, 0, 0.4)"
                },
                {
                    "type": "Container",
                    "width": "100%",
                    "height": "100%",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "items": [
                        {
                            "type": "Container",
                            "alignItems": "center",
                            "spacing": "30dp",
                            "paddingLeft": "40dp",
                            "paddingRight": "40dp",
                            "items": [
                                {
                                    "type": "Text",
                                    "text": "Welcome to Mera Mehmaan",
                                    "style": "textStyleTitle",
                                    "color": "#FFFFFF"
                                },
                                {
                                    "type": "Text",
                                    "text": "Please enter your phone number",
                                    "style": "textStyleSubtitle",
                                    "color": "#FFFFFF",
                                    "paddingBottom": "20dp"
                                },
                                {
                                    "type": "EditText",
                                    "id": "phoneInput",
                                    "hint": "Enter 10-digit number",
                                    "keyboardType": "numberPad",
                                    "selectOnFocus": True,
                                    "secureInput": False,
                                    "width": "@inputWidth",
                                    "height": "@inputHeight",
                                    "fontSize": "@fontSize",
                                    "borderWidth": "2dp",
                                    "borderColor": "#D4AF37",
                                    "borderRadius": "8dp",
                                    "paddingLeft": "15dp",
                                    "paddingRight": "15dp",
                                    "color": "#ffffff",
                                    "backgroundColor": "#ffffff",
                                    "maxLength": 10,
                                    "validCharacters": "0-9",
                                    "submitKeyType": "done",
                                    "onTextChange": [
                                        {
                                            "type": "SetValue",
                                            "property": "phoneInputValue",
                                            "value": "${event.source.value}"
                                        }
                                    ],
                                    "onSubmit": [
                                        {
                                            "type": "SendEvent",
                                            "arguments": ["phone_submitted", "${event.source.value}"]
                                        }
                                    ],
                                    "onFocus": [
                                        {
                                            "type": "SetValue",
                                            "componentId": "phoneInput",
                                            "property": "borderColor",
                                            "value": "#FFD700"
                                        }
                                    ]
                                },
                                {
                                    "type": "TouchWrapper",
                                    "id": "submitButton",
                                    "paddingTop": "30dp",
                                    "onPress": [
                                        {
                                            "type": "SendEvent",
                                            "arguments": ["phone_submitted", "${phoneInputValue}"]
                                        }
                                    ],
                                    "item": {
                                        "type": "Frame",
                                        "backgroundColor": "#D4AF37",
                                        "borderRadius": "8dp",
                                        "width": "@buttonWidth",
                                        "height": "@buttonHeight",
                                        "item": {
                                            "type": "Text",
                                            "text": "Submit",
                                            "fontSize": "@fontSize",
                                            "color": "#000000",
                                            "fontWeight": "bold",
                                            "textAlign": "center",
                                            "width": "100%",
                                            "height": "100%",
                                            "textAlignVertical": "center"
                                        }
                                    }
                                },
                                {
                                    "type": "Text",
                                    "text": "Or simply say your 10-digit phone number, with each digit spoken separately",
                                    "fontSize": "18dp",
                                    "color": "#FFFFFF",
                                    "textAlign": "center",
                                    "paddingTop": "20dp",
                                    "opacity": 0.9
                                }
                            ]
                        }
                    ]
                }
            ]
        }]
    }
}

# Icon configurations
ICON_CONFIGS = [
    {
        "event_name": "room_service_button",
        "icon_url": "https://res.cloudinary.com/dysbwjj9u/image/upload/v1768033743/Gemini_Generated_Image_1iogdd1iogdd1iog_bina8b.png",
        "label": "Room Service"
    },
    {
        "event_name": "back_to_menu",
        "icon_url": "https://res.cloudinary.com/dysbwjj9u/image/upload/v1767953091/menu_image_nci4kj.png",
        "label": "Restaurant"
    },
    {
        "event_name": "book_cab_button",
        "icon_url": "https://res.cloudinary.com/dysbwjj9u/image/upload/v1767877631/book_a_cab_lsuyj2.webp",
        "label": "Book a Cab"
    }
]

def create_icon_button(config):
    return {
        "type": "Container",
        "alignItems": "center",
        "items": [
            {
                "type": "TouchWrapper",
                "onPress": [{"type": "SendEvent", "arguments": [config["event_name"]]}],
                "item": {
                    "type": "Frame",
                    "backgroundColor": "transparent",
                    "borderWidth": "0dp",
                    "borderRadius": "@buttonBorderRadius",
                    "width": "@buttonWidth",
                    "height": "@buttonHeight",
                    "items": [{
                        "type": "Container",
                        "width": "100%",
                        "height": "100%",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "items": [
                            {
                                "type": "Image",
                                "source": "https://res.cloudinary.com/dysbwjj9u/image/upload/v1767877878/Create_a_modern_202601081817-removebg-preview_gruopj.png",
                                "scale": "best-fit",
                                "width": "@middleImageWidth",
                                "height": "@middleImageHeight",
                                "align": "center"
                            },
                            {
                                "type": "Frame",
                                "position": "absolute",
                                "top": "@iconTop",
                                "left": "@iconLeft",
                                "width": "@iconSize",
                                "height": "@iconSize",
                                "borderRadius": "@iconBorderRadius",
                                "backgroundColor": "transparent",
                                "items": [{
                                    "type": "Image",
                                    "source": config["icon_url"],
                                    "scale": "best-fill",
                                    "width": "100%",
                                    "height": "100%"
                                }]
                            }
                        ]
                    }]
                }
            },
            {
                "type": "Text",
                "text": config["label"],
                "style": "textStyleLabel",
                "paddingTop": "2dp",
                "fontSize": "@labelFontSize"
            }
        ]
    }

def build_icon_buttons():
    """Build the list of icon buttons with spacers between them."""
    items = []
    for i, config in enumerate(ICON_CONFIGS):
        items.append(create_icon_button(config))
        if i < len(ICON_CONFIGS) - 1:
            items.append({"type": "Container", "width": "@spacerWidth"})
    return items

# Main Menu APL Document
LAUNCH_APL_DOCUMENT = {
    "type": "APL",
    "version": "1.7",
    "theme": "dark",
    "resources": [
        {
            "description": "Echo Show 5 (5.5 inch, 960x480)",
            "when": "${viewport.pixelWidth == 960 && viewport.pixelHeight == 480}",
            "dimensions": {
                "buttonWidth": "280dp",
                "buttonHeight": "150dp",
                "buttonBorderRadius": "12dp",
                "middleImageWidth": "250dp",
                "middleImageHeight": "200dp",
                "iconSize": "46dp",
                "iconBorderRadius": "23dp",
                "iconTop": "44dp",
                "iconLeft": "117dp",
                "labelFontSize": "18dp",
                "spacerWidth": "20dp",
                "logoSize": "100dp",
                "titleFontSize": "48dp",
                "subtitleFontSize": "20dp"
            }
        },
        {
            "description": "Echo Show 8 (8 inch, 1280x800)",
            "when": "${viewport.pixelWidth == 1280 && viewport.pixelHeight == 800}",
            "dimensions": {
                "buttonWidth": "350dp",
                "buttonHeight": "190dp",
                "buttonBorderRadius": "15dp",
                "middleImageWidth": "310dp",
                "middleImageHeight": "250dp",
                "iconSize": "58dp",
                "iconBorderRadius": "29dp",
                "iconTop": "56dp",
                "iconLeft": "146dp",
                "labelFontSize": "22dp",
                "spacerWidth": "25dp",
                "logoSize": "125dp",
                "titleFontSize": "60dp",
                "subtitleFontSize": "25dp"
            }
        },
        {
            "description": "Echo Show 10 & 15 (10.1 inch, 1280x800)",
            "when": "${viewport.pixelWidth == 1920 && viewport.pixelHeight == 1200}",
            "dimensions": {
                "buttonWidth": "420dp",
                "buttonHeight": "230dp",
                "buttonBorderRadius": "18dp",
                "middleImageWidth": "375dp",
                "middleImageHeight": "300dp",
                "iconSize": "70dp",
                "iconBorderRadius": "35dp",
                "iconTop": "68dp",
                "iconLeft": "175dp",
                "labelFontSize": "26dp",
                "spacerWidth": "30dp",
                "logoSize": "150dp",
                "titleFontSize": "72dp",
                "subtitleFontSize": "30dp"
            }
        },
        {
            "description": "Default fallback for other devices",
            "dimensions": {
                "buttonWidth": "280dp",
                "buttonHeight": "150dp",
                "buttonBorderRadius": "12dp",
                "middleImageWidth": "250dp",
                "middleImageHeight": "200dp",
                "iconSize": "46dp",
                "iconBorderRadius": "23dp",
                "iconTop": "44dp",
                "iconLeft": "117dp",
                "labelFontSize": "18dp",
                "spacerWidth": "20dp",
                "logoSize": "100dp",
                "titleFontSize": "48dp",
                "subtitleFontSize": "20dp"
            }
        }
    ],
    "styles": {
        "textStyleTitle": {
            "values": [{
                "color": "#000000",
                "fontWeight": "300",
                "fontSize": "@titleFontSize",
                "textAlign": "center",
                "fontFamily": "Amazon Ember Display",
                "letterSpacing": "1.5dp"
            }]
        },
        "textStyleSubtitle": {
            "values": [{
                "color": "#000000",
                "fontWeight": "300",
                "fontSize": "@subtitleFontSize",
                "textAlign": "center",
                "fontFamily": "Amazon Ember",
                "opacity": 0.9
            }]
        },
        "textStyleLabel": {
            "values": [{
                "color": "#000000",
                "fontWeight": "500",
                "textAlign": "center",
                "fontFamily": "Amazon Ember"
            }]
        }
    },
    "mainTemplate": {
        "parameters": ["payload"],
        "items": [{
            "type": "Frame",
            "width": "100vw",
            "height": "100vh",
            "backgroundColor": "#bfb6b6",
            "item": {
                "type": "Container",
                "width": "100%",
                "height": "100%",
                "items": [
                    {
                        "type": "Image",
                        "source": "https://res.cloudinary.com/dysbwjj9u/image/upload/v1767943376/cropped_circle_image_gofc4u.png",
                        "position": "absolute",
                        "top": "27dp",
                        "left": "27dp",
                        "width": "@logoSize",
                        "height": "@logoSize",
                        "scale": "best-fit"
                    },
                    {
                        "type": "Container",
                        "position": "absolute",
                        "top": "0",
                        "left": "0",
                        "right": "0",
                        "bottom": "0",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "paddingLeft": "60dp",
                        "paddingRight": "60dp",
                        "items": [
                            {
                                "type": "Container",
                                "alignItems": "center",
                                "items": [
                                    {
                                        "type": "Text",
                                        "text": "MERA MEHMAAN HOTEL",
                                        "style": "textStyleTitle",
                                        "paddingBottom": "8dp",
                                        "fontWeight": "bold"
                                    },
                                    {
                                        "type": "Container",
                                        "width": "120dp",
                                        "height": "2dp",
                                        "backgroundColor": "#D4AF37",
                                        "marginBottom": "20dp"
                                    },
                                    {
                                        "type": "Text",
                                        "text": "Your Luxury Experience Awaits",
                                        "style": "textStyleSubtitle",
                                        "paddingBottom": "60dp",
                                        "fontWeight": "bold"
                                    }
                                ]
                            },
                            {
                                "type": "Container",
                                "direction": "row",
                                "width": "90%",
                                "maxWidth": "1400dp",
                                "justifyContent": "center",
                                "items": build_icon_buttons()
                            }
                        ]
                    }
                ]
            }
        }]
    }
}


class LaunchRequestHandler(AbstractRequestHandler):
    """Handles LaunchRequest - shows phone input screen first"""
    
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("=== LaunchRequestHandler called ===")
        
        # Check if user already has phone number in session
        session_attr = handler_input.attributes_manager.session_attributes
        
        if 'phone_number' in session_attr:
            logger.info(f"User has phone number: {session_attr['phone_number']}")
            # User already entered phone, show main menu
            speak_output = "Welcome back to Mera Mehmaan! You can say Room Service, Food, or Book a Cab."
            
            if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                handler_input.response_builder.add_directive(
                    RenderDocumentDirective(
                        token="launchToken",
                        document=LAUNCH_APL_DOCUMENT,
                        datasources={}
                    )
                )
        else:
            logger.info("No phone number in session - showing phone input screen")
            # First time - show phone input screen
            speak_output = ("Welcome to Mera Mehmaan! "
                           "Please provide your phone number. You can type it on screen or say it aloud.")
            
            if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                handler_input.response_builder.add_directive(
                    RenderDocumentDirective(
                        token="phoneInputToken",
                        document=PHONE_INPUT_APL,
                        datasources={}
                    )
                )
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("How may I assist you today?")
            .response
        )


class PhoneNumberIntentHandler(AbstractRequestHandler):
    """Handles voice input of phone number"""
    
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("PhoneNumberIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.NumberIntent")(handler_input))
    
    def handle(self, handler_input):
        logger.info("=== PhoneNumberIntentHandler called ===")
        session_attr = handler_input.attributes_manager.session_attributes
        
        # Get phone number from slot
        slots = handler_input.request_envelope.request.intent.slots
        phone_number = None
        
        if "phoneNumber" in slots:
            phone_number = slots["phoneNumber"].value
        elif "number" in slots:
            phone_number = slots["number"].value
        
        logger.info(f"Received phone number: {phone_number}")
        
        if phone_number and len(str(phone_number)) == 10:
            session_attr['phone_number'] = phone_number
            logger.info(f"Saved phone number to session: {phone_number}")
            
            speak_output = f"Your number {phone_number} has been registered."
            "You can say Room Service, Food, or Book a Cab. "
            "How may I help you?"
            
            # Show main menu
            if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                handler_input.response_builder.add_directive(
                    RenderDocumentDirective(
                        token="launchToken",
                        document=LAUNCH_APL_DOCUMENT,
                        datasources={}
                    )
                )
        else:
            speak_output = "I didn't catch that. Please say your 10-digit phone number clearly."
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("How may I assist you?")
            .response
        )


class PhoneSubmittedEventHandler(AbstractRequestHandler):
    """Handles phone number submission from APL screen (both button and keyboard submit)"""
    
    def can_handle(self, handler_input):
        logger.info("=== PhoneSubmittedEventHandler.can_handle called ===")
        
        if not ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            logger.info("Not a UserEvent")
            return False
        
        request = handler_input.request_envelope.request
        if not hasattr(request, 'arguments') or not request.arguments:
            logger.info("No arguments found")
            return False
        
        logger.info(f"UserEvent arguments: {request.arguments}")
        
        result = len(request.arguments) > 0 and request.arguments[0] == "phone_submitted"
        logger.info(f"Is phone_submitted event: {result}")
        return result
    
    def handle(self, handler_input):
        logger.info("=== PhoneSubmittedEventHandler.handle called ===")
        
        request = handler_input.request_envelope.request
        session_attr = handler_input.attributes_manager.session_attributes
        
        if len(request.arguments) > 1:
            phone_number = str(request.arguments[1]).strip()
            logger.info(f"Received phone number from APL: '{phone_number}'")
            
            # Validate phone number
            if len(phone_number) == 10 and phone_number.isdigit():
                session_attr['phone_number'] = phone_number
                logger.info(f"✅ Valid phone number saved to session: {phone_number}")
                
                speak_output = (
                    f"Your number {phone_number} has been registered. "
                    "You can say Room Service, Food, or Book a Cab. "
                    "How may I help you?"
                )
                
                # ✅ KEY FIX: Show main menu with three icons
                if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                    logger.info("✅ Rendering main menu APL document with icons")
                    handler_input.response_builder.add_directive(
                        RenderDocumentDirective(
                            token="launchToken",
                            document=LAUNCH_APL_DOCUMENT,
                            datasources={}
                        )
                    )
                else:
                    logger.warning("⚠️ Device does not support APL")
            else:
                logger.warning(f"❌ Invalid phone number: '{phone_number}' (length: {len(phone_number)})")
                speak_output = "Please enter a valid 10-digit phone number."
                
                # Re-show phone input screen
                if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                    handler_input.response_builder.add_directive(
                        RenderDocumentDirective(
                            token="phoneInputToken",
                            document=PHONE_INPUT_APL,
                            datasources={}
                        )
                    )
        else:
            logger.warning("❌ No phone number in arguments")
            speak_output = "Please enter your phone number."
            
            # Re-show phone input screen
            if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                handler_input.response_builder.add_directive(
                    RenderDocumentDirective(
                        token="phoneInputToken",
                        document=PHONE_INPUT_APL,
                        datasources={}
                    )
                )
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("What would you like to do?")
            .response
        )


class LaunchMenuUserEventHandler(AbstractRequestHandler):
    """Handles Room Service button press on main menu"""
    
    def can_handle(self, handler_input):
        logger.info("=== LaunchMenuUserEventHandler.can_handle called ===")
        
        if not ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            logger.info("Not a UserEvent, skipping")
            return False
        
        request = handler_input.request_envelope.request
        if not hasattr(request, 'arguments') or not request.arguments:
            logger.info("No arguments found")
            return False
        
        logger.info(f"Arguments: {request.arguments}")
        
        if len(request.arguments) > 0 and request.arguments[0] == "room_service_button":
            logger.info("✅ Matched room_service_button!")
            return True
        
        logger.info(f"Not room_service_button, it's: {request.arguments[0] if request.arguments else 'none'}")
        return False
    
    def handle(self, handler_input):
        logger.info("=== LaunchMenuUserEventHandler.handle called ===")
        return RoomServiceIntentHandler().handle(handler_input)


class LaunchCabUserEventHandler(AbstractRequestHandler):
    """Handles Book Cab button press on main menu"""
    
    def can_handle(self, handler_input):
        logger.info("=== LaunchCabUserEventHandler.can_handle called ===")
        
        if not ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            logger.info("Not a UserEvent, skipping")
            return False
        
        request = handler_input.request_envelope.request
        if not hasattr(request, 'arguments') or not request.arguments:
            logger.info("No arguments found")
            return False
        
        logger.info(f"Arguments: {request.arguments}")
        
        if len(request.arguments) > 0 and request.arguments[0] == "book_cab_button":
            logger.info("✅ Matched book_cab_button!")
            return True
        
        logger.info(f"Not book_cab_button, it's: {request.arguments[0] if request.arguments else 'none'}")
        return False
    
    def handle(self, handler_input):
        logger.info("=== LaunchCabUserEventHandler.handle called ===")
        from cab_function import BookCabIntentHandler
        return BookCabIntentHandler().handle(handler_input)