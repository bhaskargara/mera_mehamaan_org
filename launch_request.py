import ask_sdk_core.utils as ask_utils
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from ask_sdk_model import Response
from ask_sdk_core.dispatch_components import AbstractRequestHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from room_service import RoomServiceIntentHandler

# Define icon configurations
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

# Generate icon items dynamically with responsive sizing
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

# Build the icon buttons list with spacers
def build_icon_buttons():
    """Build the list of icon buttons with spacers between them."""
    items = []
    for i, config in enumerate(ICON_CONFIGS):
        items.append(create_icon_button(config))
        # Add spacer between buttons (but not after the last one)
        if i < len(ICON_CONFIGS) - 1:
            items.append({"type": "Container", "width": "@spacerWidth"})
    return items

# APL Document with responsive resources
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
                                        "text": "MERA MEHMAAN",
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
    
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        speak_output = ("Welcome to Mera Mehmaan! "
                       "You can say Room Service, Food, or Book a Cab. "
                       "How may I help you?")
        
        # Add APL if device supports it
        if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="launchToken",
                    document=LAUNCH_APL_DOCUMENT,
                    datasources={}
                )
            )
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("How may I assist you today?")
            .response
        )


class LaunchMenuUserEventHandler(AbstractRequestHandler):
    
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
        
        # Only handle "room_service_button" event
        if len(request.arguments) > 0 and request.arguments[0] == "room_service_button":
            logger.info("✅ Matched room_service_button!")
            return True
        
        logger.info(f"Not room_service_button, it's: {request.arguments[0] if request.arguments else 'none'}")
        return False
    
    def handle(self, handler_input):
        logger.info("=== LaunchMenuUserEventHandler.handle called ===")
        return RoomServiceIntentHandler().handle(handler_input)


class LaunchCabUserEventHandler(AbstractRequestHandler):
    
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
        
        # Only handle "book_cab_button" event
        if len(request.arguments) > 0 and request.arguments[0] == "book_cab_button":
            logger.info("✅ Matched book_cab_button!")
            return True
        
        logger.info(f"Not book_cab_button, it's: {request.arguments[0] if request.arguments else 'none'}")
        return False
    
    def handle(self, handler_input):
        logger.info("=== LaunchCabUserEventHandler.handle called ===")
        from cab_function import BookCabIntentHandler
        return BookCabIntentHandler().handle(handler_input)