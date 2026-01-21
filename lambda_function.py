import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from ask_sdk_model import Response
from ask_sdk_core.utils import get_supported_interfaces
import random
import os
from twilio.rest import Client

# Update this line (around line 10)
from launch_request import LaunchRequestHandler, LaunchMenuUserEventHandler, LaunchCabUserEventHandler, PhoneNumberIntentHandler, PhoneSubmittedEventHandler

# Import custom modules
# from menu_function import MenuIntentHandler
from cab_function import (
    BookCabIntentHandler,
    ProvideDestinationIntentHandler,
    ProvideTimeIntentHandler
)
from room_service import ROOM_SERVICE_HANDLERS


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


menu_items = [
    {"name": "Buffet Breakfast", "timings": "7 am to 10:30 am", "image": "https://fortunebay.com/sysimg/breakfast-buffet-dining-weekend-breakfast-buffet-image.jpg"},
    {"name": "Fruits and Juices", "timings": "7 am to 11:30 pm", "image": "https://t4.ftcdn.net/jpg/01/39/46/07/360_F_139460703_68ql2mESojJSBBLq9aM8NnCR6En2QLaM.jpg"},
    {"name": "Indian Corner", "timings": "7 am to 11:30 am & 4 pm to 11 pm", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf4P-z-iNLGSym0dqp89Bx3py0NyujQEIDzS_DacjPoVvory7B5YyJMG2hIqyuqYPy9uc&usqp=CAU"},
    {"name": "Healthy Breakfast", "timings": "7 am to 10:30 am", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3Nta9T48y2jHVcT9bpm8c_cz8i65iY-PUbg&s"},
    {"name": "Thali", "timings": "12 pm to 3:30 pm", "image": "https://content.jdmagicbox.com/v2/comp/mumbai/r4/022pxx22.xx22.190305131115.h5r4/catalogue/thalis-and-combos-by-treat-mumbai-north-indian-delivery-restaurants-kopls6wbq4.jpg"},
    {"name": "Main Course", "timings": "12 pm to 3 pm & 7 pm to 10:30 pm", "image": "https://sukhis.com/app/uploads/2022/11/veggie-platter-1024x753.jpg"},
    {"name": "Evening Snacks", "timings": "4 pm to 7 pm", "image": "https://assets.zeezest.com/blogs/PROD_Snacks_1663678190979.jpg"},
    {"name": "Hot Beverages", "timings": "4 pm to 7 pm", "image": "https://www.theauric.com/cdn/shop/articles/hot-beverages-500x500_500x.jpg?v=1659099661"},
    {"name": "Cold Beverages", "timings": "Around the clock", "image": "https://static.vecteezy.com/system/resources/thumbnails/040/174/391/small_2x/ai-generated-pictures-of-delicious-and-beautiful-drinks-photo.jpg"},
    {"name": "Starters", "timings": "12 pm to 10 pm", "image": "https://i.ytimg.com/vi/-eGHMvKx6BM/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLADYqfTS-9RC-P6T7FeUtLviOKt5g"},
    {"name": "Desserts", "timings": "Around the clock", "image": "https://thecookingfoodie.com/wp-content/uploads/2024/08/240672-jpg.jpg"}
]

sub_menu_items = {
    "Buffet Breakfast": [
        {"name": "Buffet", "quantity": "", "price": "275", "image": "https://content.jdmagicbox.com/comp/service_catalogue/restaurants-attr-catering-service-res36-6.jpg"}
    ],
    "Fruits and Juices": [
        {"name": "Seasonal Fresh Fruit Platter", "quantity": "(160 gms)", "price": "120", "image": "https://img.freepik.com/free-photo/front-view-different-fruits-composition-fresh-sliced-fruits-dark-background-health-fresh-fruit-mellow-ripe_140725-115670.jpg?semt=ais_incoming&w=740&q=80"},
        {"name": "Fresh Papaya Platter", "quantity": "(160 gms)", "price": "120", "image": "https://media.istockphoto.com/id/1154407594/photo/woman-hand-pouring-papaya-juice-on-glasses-with-slice-papaya-on-wooden-background.jpg?s=612x612&w=0&k=20&c=AiXJj9n4fI_v2ntq3XynZJT0Mp3TOx1mIkBongUpeHA="},
        {"name": "Seasonal Fresh Fruit Juice", "quantity": "(360 ml)", "price": "120", "image": "https://media.istockphoto.com/id/1127182311/photo/fruit-juices.jpg?s=612x612&w=0&k=20&c=M52yyMvgFUNkPtN9PACB9auB5uuA1CD6zcRsCTX8JsM="}
    ],
    "Indian Corner": [
        {"name": "Idly", "quantity": "(2 pc) (170 gms)", "price": "75", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Idli_%28South_Indian_cuisine%29.jpg"},
        {"name": "Sambar Idly Bowl", "quantity": "(2 pc)", "price": "90", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Idly_Wada.jpg/500px-Idly_Wada.jpg"},
        {"name": "Single Idly", "quantity": "(1 pc)", "price": "40", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Idli_%28South_Indian_cuisine%29.jpg"},
        {"name": "Button Idly Bowl", "quantity": "(360 gms)", "price": "85", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Idli_%28South_Indian_cuisine%29.jpg"},
        {"name": "Poori", "quantity": "(3 pc) (130 gms)", "price": "130", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Chole_Bhature_from_Nagpur.JPG/500px-Chole_Bhature_from_Nagpur.JPG"},
        {"name": "Plain Dosa", "quantity": "(80 gms)", "price": "105", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Masala_dosa_01.jpg"},
        {"name": "Masala Dosa", "quantity": "(150 gms)", "price": "135", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Paper_Masala_Dosa.jpg/500px-Paper_Masala_Dosa.jpg"},
        {"name": "Ghee Roast Dosa", "quantity": "(140 gms)", "price": "115", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Dosa_at_Sri_Ganesha_Restauran%2C_Bangkok_%2844570742744%29.jpg/500px-Dosa_at_Sri_Ganesha_Restauran%2C_Bangkok_%2844570742744%29.jpg"},
        {"name": "Onion Dosa", "quantity": "(140 gms)", "price": "135", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Paper_Masala_Dosa.jpg/500px-Paper_Masala_Dosa.jpg"},
        {"name": "Pesarattu", "quantity": "(150 gms)", "price": "140", "image": "https://upload.wikimedia.org/wikipedia/commons/6/6c/Pesarattu.jpg"},
        {"name": "Rava Plain Dosa", "quantity": "(100 gms)", "price": "140", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/%D7%93%D7%95%D7%A1%D7%94.jpg/1920px-%D7%93%D7%95%D7%A1%D7%94.jpg"},
        {"name": "Onion Rava Dosa", "quantity": "(100 gms)", "price": "150", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/%D7%93%D7%95%D7%A1%D7%94.jpg/1920px-%D7%93%D7%95%D7%A1%D7%94.jpg"},
        {"name": "Onion Uthappam / Masala Uthappam", "quantity": "(350 gms)", "price": "140", "image": "https://images.slurrp.com/prod/articles/hill9km8515.webp"},
        {"name": "Paper Dosa (Family Dosa 70mm)", "quantity": "(170 gms)", "price": "190", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Paper_Masala_Dosa.jpg/500px-Paper_Masala_Dosa.jpg"},
        {"name": "Paper Masala Dosa (Family Dosa 70mm)", "quantity": "(200 gms)", "price": "225", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Paper_Masala_Dosa.jpg/500px-Paper_Masala_Dosa.jpg"},
        # {"name": "Vada", "quantity": "(2 pc) (130 gms)", "price": "100", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Ondu_Plate_Idli_Vada.jpg"},
        {"name": "Vada", "quantity": "(1 pc)", "price": "50", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Ondu_Plate_Idli_Vada.jpg"},
        # {"name": "Sambhar Vada Bowl", "quantity": "(2 pc) (400 gms)", "price": "120", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Ondu_Plate_Idli_Vada.jpg"},
        {"name": "Sambhar Vada Bowl", "quantity": "(1 pc)", "price": "60", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Ondu_Plate_Idli_Vada.jpg"},
        {"name": "Upma", "quantity": "(260 gms)", "price": "80", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/A_photo_of_Upma.jpg/500px-A_photo_of_Upma.jpg"},
        {"name": "Pongal", "quantity": "(300 gms)", "price": "90", "image": "https://commons.wikimedia.org/wiki/Special:FilePath/Sakkarai_pongal_in_banana_leaf.jpg"},
        {"name": "M.L.A Pesarattu", "quantity": "(220 gms)", "price": "165", "image": "https://upload.wikimedia.org/wikipedia/commons/6/6c/Pesarattu.jpg"},
        {"name": "Chole Bhatura", "quantity": "(180 gms)", "price": "185", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Chole_Bhature_from_Nagpur.JPG/500px-Chole_Bhature_from_Nagpur.JPG"},
        {"name": "Dahi Vada", "quantity": "(2 pc) (140 gms)", "price": "130", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Dahi_bhalla_or_dahi_wada_or_dahi_bada.PNG/500px-Dahi_bhalla_or_dahi_wada_or_dahi_bada.PNG"},
        {"name": "Mysore Masala Dosa", "quantity": "(220 gms)", "price": "140", "image": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Bonda_%281%29.jpg"},
        {"name": "Set Dosa with Mixed Vegetable Korma", "quantity": "(220 gms)", "price": "135", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Davanagere_Benne_Dosa.jpg/500px-Davanagere_Benne_Dosa.jpg"}
    ],
    "Healthy Breakfast": [
        {"name": "Choice of Cereals", "quantity": "(250 ml)", "price": "130", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/NCI_Visuals_Food_Meal_Breakfast.jpg/250px-NCI_Visuals_Food_Meal_Breakfast.jpg"}
    ],
    "Evening Snacks": [
        {"name": "Vegetable Cutlet", "quantity": "(2 pc) (100 gms)", "price": "85", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Kotleta_031.jpg/1280px-Kotleta_031.jpg"},
        {"name": "Mysore Bajji", "quantity": "(5 pc) (200 gms)", "price": "85", "image": "https://d06d8ecd86.clvaw-cdnwnd.com/e8e09141654851d60ff52a9a865abca0/200000100-9c0f09c0f4/MysoreBonda.jpeg?ph=d06d8ecd86"},
        {"name": "Mirchi Bajji", "quantity": "(4 pc) (200 gms)", "price": "85", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Mirchi_Bada_from_Jodhpur_1.jpg/1280px-Mirchi_Bada_from_Jodhpur_1.jpg"},
        {"name": "Assorted Bajji", "quantity": "(220 gms)", "price": "85", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0A4tBAVuWMFOc5UT_vbXe5dHfNyBxM61SZjXr8MUMPzecGLnR-4wnBz-3STAaVlM17hM&usqp=CAU"},
        {"name": "Aloo Bonda", "quantity": "(2 pc) (160 gms)", "price": "85", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Mumbai-vada.jpg/500px-Mumbai-vada.jpg"},
        {"name": "Onion Thul Pakora", "quantity": "(220 gms)", "price": "110", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnW9700DGiH_Lh2GRYh-jCbIJj0Qk_aVdU9g&s"},
        {"name": "French Fries", "quantity": "(220 gms)", "price": "160", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/French_Fries.JPG/500px-French_Fries.JPG"},
        {"name": "Paneer Pakora", "quantity": "(220 gms)", "price": "260", "image": "https://www.whiskaffair.com/wp-content/uploads/2020/08/Paneer-Pakora-2-3.jpg"}
    ],
    "Hot Beverages": [
        {"name": "Filter Coffee", "quantity": "(150 ml)", "price": "70", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Filter_kaapi.JPG/500px-Filter_kaapi.JPG"},
        {"name": "Nescafe", "quantity": "(150 ml)", "price": "70", "image": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Nescaf%C3%A8_instant_coffee%2C_2019-%2801%29.jpg"},
        {"name": "Tea", "quantity": "(150 ml)", "price": "70", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Hong_Kong-style_Milk_Tea.jpg/1280px-Hong_Kong-style_Milk_Tea.jpg"},
        {"name": "Masala Tea", "quantity": "(150 ml)", "price": "75", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Chai_In_Sakora.jpg/500px-Chai_In_Sakora.jpg"},
        {"name": "Ginger Tea", "quantity": "(150 ml)", "price": "75", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Kullad_chai.jpg/250px-Kullad_chai.jpg"},
        {"name": "Green Tea", "quantity": "(150 ml)", "price": "75", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Green_Tea_Color.jpg/500px-Green_Tea_Color.jpg"},
        {"name": "Milk", "quantity": "(150 ml)", "price": "75", "image": "https://nutritionsource.hsph.harvard.edu/wp-content/uploads/2024/11/AdobeStock_354060824-1024x683.jpeg"},
        {"name": "Hot Chocolate", "quantity": "(150 ml)", "price": "90", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS88_eqhlpefxsrrK9B19IEFITyP6r2kYBQSg&s"},
        {"name": "Horlicks / Bournvita", "quantity": "(150 ml)", "price": "90", "image": "https://static.toiimg.com/thumb/57809429.cms?imgsize=374164&width=800&height=800"}
    ],
    "Cold Beverages": [
        {"name": "Fruit Punch", "quantity": "(300 ml)", "price": "130", "image": "https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,h_960,w_960//InstamartAssets/fruit_punch.webp"},
        {"name": "Milk Shakes", "quantity": "(300 ml)", "price": "140", "image": "https://i.pinimg.com/736x/bb/b3/2e/bbb32e014049db4d913bf6374a59722f.jpg"},
        {"name": "Cold Coffee Without Ice Cream", "quantity": "(300 ml)", "price": "130", "image": "https://barashadas.com/wp-content/uploads/2021/06/cold-coffee2.jpg"},
        {"name": "Cold Coffee With Ice Cream", "quantity": "(300 ml)", "price": "150", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQs2KLIsO6j3-JNn61xGl_Eb8xXshksqyyUiQ&s"},
        {"name": "Sweet / Salt Lassi", "quantity": "(300 ml)", "price": "90", "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Salt_lassi.jpg/500px-Salt_lassi.jpg"},
        {"name": "Masala Butter Milk", "quantity": "(300 ml)", "price": "70", "image": "https://x9s2d6a3.delivery.rocketcdn.me/wp-content/uploads/2019/01/masala-chaas-4_1200x1200.jpg"},
        {"name": "Fresh Lime Water/Soda", "quantity": "(300 ml)", "price": "70", "image": "https://booking.thesonahotel.com/storage/2022/10/lime-soda-620.jpg"},
        {"name": "Aerated Water", "quantity": "(300 ml)", "price": "40", "image": "https://upload.wikimedia.org/wikipedia/commons/5/59/Drinking_glass_00118.gif"},
        {"name": "Bottled Water", "quantity": "(1000 ml)", "price": "40", "image": "https://upload.wikimedia.org/wikipedia/commons/0/02/Stilles_Mineralwasser.jpg"}
    ],
    "Starters": [
        {"name": "Veg Spring Rolls", "quantity": "(220 gms)", "price": "250", "image": "https://d1mxd7n691o8sz.cloudfront.net/static/recipe/recipe/2023-12/Vegetable-Spring-Rolls-2-1-906001560ca545c8bc72baf473f230b4_thumbnail_170.jpeg"},
        {"name": "Crispy Fried Vegetables", "quantity": "(220 gms)", "price": "250", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRo49xKGDcoL-0lyVZL-JUJVlrrg0KPDVJb0g&s"},
        {"name": "Chilli Cauliflower", "quantity": "(220 gms)", "price": "265", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSexDqBioG78QOxPqav-50pmoD1-stJeXn_YnpFDHoHIVHjoQeTvn07RUMZo86Qj1lTT8Y&usqp=CAU"},
        {"name": "Golden Fried Baby Corn", "quantity": "(220 gms)", "price": "265", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRI75Kjfl0WXpJoa1YYOu5gX6vk-pDZmB2Iw&s"},
        {"name": "Gobi Manchurian", "quantity": "(350 gms)", "price": "265", "image": "https://www.bigbasket.com/media/uploads/recipe/w-l/1706_1.jpg"},
        {"name": "Corn Salt N Pepper", "quantity": "(180 gms)", "price": "275", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDPj5Ashu7lM_eH9oNxaOWpKaxei3gAtPeYCOeVR8LKJBy7YxrjyMhaUk46YlcgiglSMA&usqp=CAU"},
        {"name": "Chilli Paneer", "quantity": "(350 gms)", "price": "295", "image": "https://www.indianhealthyrecipes.com/wp-content/uploads/2022/02/chilli-paneer-recipe.jpg"},
        {"name": "Paneer Manchurian", "quantity": "(350 gms)", "price": "295", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQz9dFUxm5U5E-y4D08dcyDjs7yxUaSe5Y-GQ&s"},
        {"name": "Vegetable Manchurian Dry", "quantity": "(220 gms)", "price": "265", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDE1T1Jn_4Tjeh6kRSNBcz1SSGA1sZhtpTRQ&s"},
        {"name": "Baby Corn Manchurian", "quantity": "(220 gms)", "price": "265", "image": "https://i.pinimg.com/564x/21/1d/1e/211d1e0ff6cedc8131dff48178b4a25f.jpg"},
        {"name": "Crispy Corn Chilly", "quantity": "(180 gms)", "price": "275", "image": "https://madscookhouse.com/wp-content/uploads/2021/09/Spicy-Crispy-Corn-Kernels-500x375.jpg"},
        {"name": "Chilly Stuffed Mushroom", "quantity": "(350 gms)", "price": "320", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZWwOy1ml5xNAh0aGlAl_1X_YNfCN8IKl8pA&s"},
        {"name": "Paneer Tikka", "quantity": "(240 gms)", "price": "310", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSn-stvhbpCIHk4_aVCxb0aekKPAJPLWM2FeA&s"},
        {"name": "Paneer Majestic", "quantity": "(220 gms)", "price": "295", "image": "https://i.ytimg.com/vi/eBppixI8U6Y/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBfPpEA-H3d3_00axfyyM8gYv8Bnw"},
        {"name": "Paneer 65", "quantity": "(240 gms)", "price": "295", "image": "https://www.indianhealthyrecipes.com/wp-content/uploads/2022/06/paneer-65-recipe.jpg"},
        {"name": "Cauliflower 65", "quantity": "(240 gms)", "price": "270", "image": "https://i.pinimg.com/736x/77/d6/98/77d6988809c84270c949ae26f71e8874.jpg"}
    ],
    "Thali": [
        {"name": "South Indian Thali", "quantity": "", "price": "275", "image": "https://media.istockphoto.com/id/1469066868/photo/traditional-south-indian-food-platter.jpg?s=612x612&w=0&k=20&c=yOJ7kvAuL8Rez9cAdRAM6ZmHQu0BAD_lpcYzksp4h8w="},
        {"name": "Special Thali", "quantity": "", "price": "325", "image": "https://madhurasrecipe.com/wp-content/uploads/2023/02/Shravan-Somwar-Thali-Featured.jpg"}
    ],
    "Main Course": [
        {"name": "Fresh Green Salad", "quantity": "(160 gms)", "price": "55", "image": "https://getinspiredeveryday.com/wp-content/uploads/2022/02/Easy-Green-Salad-Get-Inspired-Everyday-7.jpg"},
        {"name": "Roasted Papad", "quantity": "(50 gms)", "price": "40", "image": "https://skydecklounge.in/wp-content/uploads/2022/08/SkyDeck-Roasted-Papad.jpg"},
        {"name": "Masala Papad", "quantity": "(60 gms)", "price": "45", "image": "https://i2.wp.com/kalimirchbysmita.com/wp-content/uploads/2016/09/Masala-Papad-03.jpg?fit=1024%2C569&ssl=1"},
        {"name": "Tomato Soup", "quantity": "(250 ml)", "price": "125", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBhLWZxw8pRd5rOlKQv03CmSqpidD-PCYBtg&s"},
        {"name": "Manchow Soup", "quantity": "(250 ml)", "price": "125", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9McWIhdFzh4arIMXejPIIF7D_xA-1GtUDww&s"},
        {"name": "Hot and Sour Soup", "quantity": "(250 ml)", "price": "125", "image": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Ping_SJ_hot_%26_sour_soup.JPG"},
        {"name": "Sweet Corn Soup", "quantity": "(250 ml)", "price": "125", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSC2FeSWsl8T37Q9QVI0Q8m4AnB7ox6RwnQwg&s"},
        {"name": "Healthy Clear Soup", "quantity": "(250 ml)", "price": "125", "image": "https://healux.in/wp-content/uploads/2020/11/HealthyClearSoup.jpg"},
        {"name": "Paneer Aap Ki Pasand", "quantity": "(400 gms)", "price": "285", "image": "https://i.ytimg.com/vi/FeoWXsqSV6g/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLBj-OYABtWaQRYJtHDNcFYbIsJsqg"},
        {"name": "Paneer Tikka Masala", "quantity": "(400 gms)", "price": "325", "image": "https://cookingfromheart.com/wp-content/uploads/2017/03/Paneer-Tikka-Masala-4-500x375.jpg"},
        {"name": "Choice of Kofta Curry (Malai Kofta / Vegetable Kofta)", "quantity": "(400 gms)", "price": "275", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKxc2FBbyZjHKRWE01JCeHp0VBT7ZcIglkrCkc9zIhgmI0LvmvDcJ5rbSXOmxTUUHSrG8&usqp=CAU"},
        {"name": "Methi Chaman", "quantity": "(400 gms)", "price": "285", "image": "https://vismaifood.com/storage/app/uploads/public/d11/aad/b97/thumb__1200_0_0_0_auto.jpg"},
        {"name": "Subji Ki Bahar", "quantity": "(400 gms)", "price": "260", "image": "https://i.ytimg.com/vi/6E2gotETHa0/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAeTmMxiJYgOJ77t1qwOQm3TiZleQ"},
        {"name": "CHOICE OF POTATO (jeera/methi/Gobhi/Hara Pyaz)", "quantity": "(400 gms)", "price": "255", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJ9_H63qmXrj79DndlLFbifjJfglHO5tNSkA&s"},
        {"name": "Mushroom Mutter Curry", "quantity": "(400 gms)", "price": "285", "image": "https://static.toiimg.com/photo/75534551.cms"},
        {"name": "Kaju Tomato Curry", "quantity": "(400 gms)", "price": "325", "image": "https://i.ytimg.com/vi/1JHPlYa3QN4/maxresdefault.jpg"}
    ],
    "Desserts": [
        {"name": "Gulab Jamun", "quantity": "(60 gms)", "price": "90", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTrkSTYkhjRV2wggrSj3W1q_RdzdJIA8aT2w&s"},
        {"name": "Gulab Jamun with Ice Cream", "quantity": "(2 pc)", "price": "120", "image": "https://i.pinimg.com/originals/eb/ef/0f/ebef0f698b774dbf46e5729ccfea4391.jpg"},
        {"name": "Khubaani Ka Meetha", "quantity": "(90 gms)", "price": "150", "image": "https://i.ytimg.com/vi/ulKuOuqzJRU/sddefault.jpg"},
        {"name": "Khubaani Ka Meetha with Ice Cream", "quantity": "(120 gms)", "price": "170", "image": "https://themadscientistskitchen.com/wp-content/uploads/2020/08/Khubani-ka-Meetha-480x270.jpg"},
        {"name": "Fruit Salad", "quantity": "(120 gms)", "price": "90", "image": "https://cdn.loveandlemons.com/wp-content/uploads/2025/06/fruit-salad.jpg"},
        {"name": "Fruit Salad with Ice Cream", "quantity": "(150 gms)", "price": "120", "image": "https://media.istockphoto.com/id/174849692/photo/ice-cream-and-fruits.jpg?s=612x612&w=0&k=20&c=ExH1Ui9CHYH5kHYtJplLUZIipWnYBTMhLx9Y6iwvIKE="},
        {"name": "Gajar Ka Halwa", "quantity": "", "price": "115", "image": "https://vanitascorner.com/wp-content/uploads/2018/01/carrothalwa.jpg"},
        {"name": "Gajar Ka Halwa with Ice Cream", "quantity": "", "price": "140", "image": "https://img-global.cpcdn.com/recipes/4129decfab260bec/680x781cq80/gajarcarrot-halwa-with-vanilla-ice-cream-recipe-main-photo.jpg"}
    ]
}

# ---------------- UNIFIED APL TEMPLATE ----------------
def get_unified_menu_apl(title, subtitle, hint_text, show_back_button=False, card_type="menu"):
    
    apl_document = {
        "type": "APL",
        "version": "1.7",
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
                        # Main Content
                        {
                            "type": "Container",
                            "paddingLeft": "20dp",
                            "paddingTop": "20dp",
                            "paddingRight": "20dp",
                            "paddingBottom": "100dp",
                            "items": [
                                {
                                    "type": "Text",
                                    "text": title,
                                    "style": "textStyleTitle",
                                    "paddingBottom": "10dp",
                                    "textAlign": "center",
                                    "fontFamily": "Amazon Ember"
                                },
                                {
                                    "type": "Text",
                                    "text": subtitle,
                                    "style": "textStyleSubTitle",
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
                                                                        "type": "MenuItemCard" if card_type == "menu" else "SubMenuItemCard",
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
                        # Hint Bar at Bottom
                        {
                            "type": "Container",
                            "position": "absolute",
                            "bottom": "0",
                            "width": "100%",
                            "height": "80dp",
                            "backgroundColor": "rgba(0, 0, 0, 0.85)",
                            "borderTopLeftRadius": "20dp",
                            "borderTopRightRadius": "20dp",
                            "paddingLeft": "20dp",
                            "paddingRight": "20dp",
                            "paddingTop": "10dp",
                            "paddingBottom": "10dp",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "items": [
                                {
                                    "type": "Container",
                                    "direction": "row",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "backgroundColor": "#C62828",
                                    "borderRadius": "12dp",
                                    "paddingTop": "12dp",
                                    "paddingBottom": "12dp",
                                    "paddingLeft": "20dp",
                                    "paddingRight": "20dp",
                                    "shadowColor": "black",
                                    "shadowOffset": {"width": 0, "height": 2},
                                    "width": "95%",
                                    "items": [
                                        {
                                            "type": "Text",
                                            "text": hint_text,
                                            "fontSize": "17dp",
                                            "fontWeight": "700",
                                            "color": "white",
                                            "fontFamily": "Amazon Ember",
                                            "textAlign": "center",
                                            "maxLines": 2
                                        }
                                    ]
                                }
                            ]
                        }
                    ] + ([
                        # Back Button (only if show_back_button=True)
                        {
                            "type": "TouchWrapper",
                            "position": "absolute",
                            "right": "30dp",
                            "bottom": "40dp",
                            "width": "110dp",
                            "height": "50dp",
                            "onPress": [{"type": "SendEvent", "arguments": ["back_to_menu"]}],
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
                                        "text": "MENU",
                                        "fontSize": "20dp",
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
                    ] if show_back_button else [])
                }
            ]
        },
        "layouts": {
            "MenuItemCard": {
                "parameters": ["item"],
                "item": {
                    "type": "TouchWrapper",
                    "width": "130dp",
                    "height": "200dp",
                    "paddingRight": "2%",
                    "onPress": [{"type": "SendEvent", "arguments": ["item_tap", "${item.name}"]}],
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
                        "paddingBottom": "8dp",
                        "paddingLeft": "6dp",
                        "paddingRight": "6dp",
                        "items": [
                            {
                                "type": "Image",
                                "source": "${item.image}",
                                "width": "130dp",
                                "height": "130dp",
                                "scale": "best-fill",
                                "borderRadius": "65dp"
                            },
                            {
                                "type": "Text",
                                "text": "${item.name}",
                                "style": "textStyleItem",
                                "textAlign": "center",
                                "paddingTop": "6dp",
                                "maxLines": 2,
                                "fontSize": "14dp",
                                "fontWeight": "600",
                                "fontFamily": "Amazon Ember"
                            },
                            {
                                "type": "Text",
                                "text": "${item.timings}",
                                "style": "textStyleTimings",
                                "textAlign": "center",
                                "paddingTop": "4dp",
                                "fontSize": "12dp",
                                "fontWeight": "bold",
                                "maxLines": 2,
                                "fontFamily": "Amazon Ember"
                            }
                        ]
                    }
                }
            },
            "SubMenuItemCard": {
                "parameters": ["item"],
                "item": {
                    "type": "TouchWrapper",
                    "width": "23%",
                    "height": "230dp",
                    "paddingRight": "2%",
                    "onPress": [{"type": "SendEvent", "arguments": ["subitem_tap", "${item.name}"]}],
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
                        "paddingBottom": "8dp",
                        "paddingLeft": "6dp",
                        "paddingRight": "6dp",
                        "items": [
                            {
                                "type": "Image",
                                "source": "${item.image}",
                                "width": "130dp",
                                "height": "130dp",
                                "scale": "best-fill",
                                "borderRadius": "65dp"
                            },
                            {
                                "type": "Container",
                                "direction": "row",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "spacing": 20,
                                "items": [
                                    {
                                        "type": "Text",
                                        "text": "₹${item.price} - ",
                                        "textAlign": "center",
                                        "fontSize": "18dp",
                                        "fontWeight": "bold",
                                        "color": "#27ae60",
                                        "fontFamily": "Amazon Ember"
                                    },
                                    {
                                        "type": "Text",
                                        "text": " ${item.quantity}",
                                        "textAlign": "center",
                                        "fontSize": "14dp",
                                        "fontWeight": "normal",
                                        "color": "#3498db",
                                        "fontFamily": "Amazon Ember"
                                    }
                                ]
                            },
                            {
                                "type": "Text",
                                "text": "${item.name}",
                                "style": "textStyleItem",
                                "textAlign": "center",
                                "paddingTop": "6dp",
                                "maxLines": 2,
                                "fontSize": "16dp",
                                "fontWeight": "600",
                                "fontFamily": "Amazon Ember"
                            }
                        ]
                    }
                }
            }
        },
        "styles": {
            "textStyleTitle": {
                "values": [{"color": "#000000", "fontSize": "36dp", "fontWeight": "bold", "fontFamily": "Amazon Ember"}]
            },
            "textStyleSubTitle": {
                "values": [{"color": "#000000", "fontSize": "18dp", "fontFamily": "Amazon Ember"}]
            },
            "textStyleItem": {
                "values": [{"color": "#000000", "fontSize": "14dp", "fontWeight": "600", "fontFamily": "Amazon Ember"}]
            },
            "textStyleTimings": {
                "values": [{"color": "#e74c3c", "fontSize": "12dp", "fontWeight": "bold", "fontFamily": "Amazon Ember"}]
            }
        }
    }
    
    return apl_document


# ---------------- UPDATED MENU HANDLER ----------------
class MenuIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MenuIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Here is today's menu with categories like Buffet Breakfast, Fruits and Juices, "
            "Indian Corner, Healthy Breakfast, Thali, Main Course, Evening Snacks, "
            "Hot Beverages, Cold Beverages, Starters and Desserts. Which category would you like to see?"
        )

        # Use unified template for main menu
        apl_document = get_unified_menu_apl(
            title="Restaurant Menu",
            subtitle="Tap an item to view the sub-menu",
            hint_text="🎤 <b>Say:</b> Show Starters • What are the items in Desserts • Select Starters | <b><span color='#FFEB3B'>Tap any item to view sub-menu</span></b>",
            show_back_button=False,
            card_type="menu"
        )

        def chunk_into_rows(items, items_per_row=4):
            rows = []
            for i in range(0, len(items), items_per_row):
                rows.append(items[i:i + items_per_row])
            return rows

        apl_data = {
            "categories": {
                "menuRows": chunk_into_rows(menu_items, 4)
            }
        }

        if ask_utils.get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="menuToken",
                    document=apl_document,
                    datasources=apl_data
                )
            )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("You can say show desserts, show me starters, or tap any menu item.")
                .response
        )


# ---------------- UPDATED SUBMENU HANDLER ----------------
class SubMenuIntentHandler(AbstractRequestHandler): 
    def can_handle(self, handler_input):
        if ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            args = handler_input.request_envelope.request.arguments
            if args and args[0] in ["item_tap", "back_to_menu"]:
                return True
            return False
        return ask_utils.is_intent_name("SubMenuIntent")(handler_input)

    def handle(self, handler_input):
        category = None

        if ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            args = handler_input.request_envelope.request.arguments
            logger.info(f"SubMenu touch event received with arguments: {args}")
            
            if args and args[0] == "back_to_menu":
                logger.info("Back button pressed - returning to main menu")
                menu_handler = MenuIntentHandler()
                return menu_handler.handle(handler_input)
            
            if args and len(args) > 1 and args[0] == "item_tap":
                category = args[1]
                logger.info(f"Category from touch: {category}")

        if ask_utils.is_intent_name("SubMenuIntent")(handler_input):
            slots = handler_input.request_envelope.request.intent.slots
            if slots.get("category") and slots["category"].value:
                category = slots["category"].value.title()
                logger.info(f"Category from voice: {category}")

        if not category or category not in sub_menu_items:
            speak_output = f"Sorry, I don't have details for {category if category else 'that category'}."
            return handler_input.response_builder.speak(speak_output).ask("Which category would you like?").response

        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["last_category"] = category
        logger.info(f"Stored last_category: {category}")

        items = sub_menu_items[category]
        logger.info(f"Items for {category}: {items}")
        
        item_names = ", ".join([i["name"] for i in items])
        speak_output = f"In {category}, we have {item_names}. What would you like to order"

        # Use unified template for submenu
        apl_document = get_unified_menu_apl(
            title=f"{category} Menu",
            subtitle="Tap items to add to cart",
            hint_text="🎤 <b>Say:</b> Order Idly • I would like to order Poori | <b><span color='#FFEB3B'>Tap any item you want to order</span></b>",
            show_back_button=True,
            card_type="submenu"
        )

        def chunk_into_rows(items, items_per_row=4):
            rows = []
            for i in range(0, len(items), items_per_row):
                rows.append(items[i:i + items_per_row])
            return rows

        apl_data = {
            "categories": {
                "menuRows": chunk_into_rows(items, 4)
            }
        }

        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="subMenuToken",
                    document=apl_document,
                    datasources=apl_data
                )
            )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("You can say order idly or tap an item")
                .response
        )


class GoBackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GoBackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("GoBackIntent triggered - returning to main menu")
        menu_handler = MenuIntentHandler(),

        return menu_handler.handle(handler_input)


class OrderFoodIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("OrderFoodIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        food_item = slots.get("foodItem").value if slots.get("foodItem") else None
        logger.info(f"User said food item: {food_item}")

        if not food_item:
            speak_output = "I didn't catch the item name. Please tell me what you want to order."
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response

        # Normalize input
        food_item = food_item.title().strip()

        # ✅ Check if the spoken item matches a submenu category (like Thali, Starters, etc.)
        if food_item in sub_menu_items:
            logger.info(f"'{food_item}' matches submenu category — redirecting to SubMenuIntentHandler.")
            # Reuse the same logic from SubMenuIntentHandler
            sub_menu_handler = SubMenuIntentHandler()
            # Simulate selecting that category
            handler_input.request_envelope.request.intent.slots["category"] = type(
                "obj", (object,), {"value": food_item}
            )()
            return sub_menu_handler.handle(handler_input)

        # Otherwise, check if the food item matches an individual item inside submenus
        for category, items in sub_menu_items.items():
            for item in items:
                if item["name"].lower() == food_item.lower():
                    logger.info(f"'{food_item}' matches submenu item — simulating selection.")
                    # Simulate the same as touch "subitem_tap"
                    user_event_handler = UserEventHandler()
                    handler_input.request_envelope.request.arguments = ["subitem_tap", item["name"]]
                    return user_event_handler.handle(handler_input)

        # If item not found
        speak_output = f"Sorry, I couldn't find {food_item} on the menu. You can say 'show menu' or 'menu' to browse items."
        return handler_input.response_builder.speak(speak_output).ask("Would you like to hear today's menu?").response

# ---------------- USER EVENT HANDLER (for subitem selection) ----------------
class UserEventHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Only handle "subitem_tap" events, not "item_tap" or "back_to_menu"
        if ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            arguments = handler_input.request_envelope.request.arguments
            # Check if it's a subitem_tap event
            if arguments and arguments[0] == "subitem_tap":
                return True
        return False

    def handle(self, handler_input):
        arguments = handler_input.request_envelope.request.arguments
        logger.info(f"UserEvent (subitem) received with arguments: {arguments}")
        
        if not arguments or len(arguments) < 2:
            return handler_input.response_builder.speak("Sorry, I didn't catch that selection.").response

        action_type = arguments[0]
        item_name = arguments[1].strip() if len(arguments) > 1 else None

        # Handle subitem tap
        if action_type == "subitem_tap" and item_name:
            logger.info(f"Searching for item: '{item_name}'")
            
            # Flatten all menu items from sub_menu_items with proper quantity field
            all_menu_items = []
            for category, items in sub_menu_items.items():
                for item in items:
                    # Ensure quantity field exists
                    if "quantity" not in item:
                        item["quantity"] = ""
                    all_menu_items.append(item)

            selected_item = next((i for i in all_menu_items if i["name"].lower() == item_name.lower()), None)

            if selected_item:
                session_attr = handler_input.attributes_manager.session_attributes
                session_attr["pending_food"] = selected_item["name"]
                session_attr["pending_price"] = selected_item["price"]
                session_attr["pending_image"] = selected_item["image"]
                session_attr["pending_quantity_display"] = selected_item.get("quantity", "")

                # Create proper speech output with quantity info
                quantity_text = f" {selected_item['quantity']}" if selected_item.get("quantity") else ""
                speak_output = f"You selected {selected_item['name']} for {selected_item['price']} rupees. How many would you like to order?"

                # Create datasource for APL
                apl_datasource = {
                    "selectedItem": {
                        "name": selected_item["name"],
                        "price": selected_item["price"],
                        "image": selected_item["image"],
                        "quantity": selected_item.get("quantity", "")
                    }
                }

                # APL for quantity input with enhanced display
                quantity_apl = {
                    "type": "APL",
                    "version": "1.7",
                    "mainTemplate": {
                        "parameters": ["payload"],
                        "items": [
                            {
                                "type": "Container",
                                "width": "100vw",
                                "height": "100vh",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "items": [
                                    {
                                        "type": "Image",
                                        "source": "https://media.istockphoto.com/id/922930296/video/grey-abstract-background.jpg?s=640x640&k=20&c=JTQRynekqaCHvt7Cu4xYdnHXrwKAprS_KTJJvAN5Us4=",
                                        "scale": "best-fill",
                                        "width": "100%",
                                        "height": "100%",
                                        "position": "absolute"
                                    },
                                    {
                                        "type": "Container",
                                        "alignItems": "center",
                                        "paddingLeft": "40dp",
                                        "paddingRight": "40dp",
                                        "items": [
                                            {
                                                "type": "Text",
                                                "text": "Selected Item",
                                                "fontSize": "36dp",
                                                "color": "#000000",
                                                "fontWeight": "bold",
                                                "paddingBottom": "10dp",
                                                "textAlign": "center",
                                                "fontFamily": "Amazon Ember"
                                            },
                                            {
                                                "type": "Frame",
                                                "width": "300dp",
                                                "height": "300dp",
                                                "backgroundColor": "rgba(255,255,255,0.1)",
                                                "borderRadius": "150dp",
                                                "borderWidth": "3dp",
                                                "borderColor": "#FFD700",
                                                "items": [
                                                    {
                                                        "type": "Image",
                                                        "source": "${payload.selectedItem.image}",
                                                        "width": "300dp",
                                                        "height": "300dp",
                                                        "borderRadius": "150dp",
                                                        "scale": "best-fill"
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "Container",
                                                "direction": "row",
                                                "alignItems": "center",
                                                "justifyContent": "spaceBetween",
                                                "paddingTop": "10dp",
                                                "paddingLeft": "40dp",
                                                "paddingRight": "40dp",
                                                "items": [
                                                    {
                                                        "type": "Text",
                                                        "text": "${payload.selectedItem.name} - ",
                                                        "fontSize": "30dp",
                                                        "color": "white",
                                                        "fontWeight": "700",
                                                        "maxLines": 2,
                                                        "flexGrow": 1,
                                                        "fontFamily": "Amazon Ember"
                                                    },
                                                    {
                                                        "type": "Text",
                                                        "text": "₹${payload.selectedItem.price}",
                                                        "fontSize": "28dp",
                                                        "color": "#27ae60",
                                                        "fontWeight": "bold",
                                                        "textAlign": "right",
                                                        "fontFamily": "Amazon Ember"
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "Container",
                                                "paddingTop": "10dp",
                                                "alignItems": "center",
                                                "items": [
                                                    {
                                                        "type": "Frame",
                                                        "backgroundColor": "rgba(255,215,0,0.2)",
                                                        "borderRadius": "12dp",
                                                        "borderWidth": "2dp",
                                                        "borderColor": "#FFD700",
                                                        "paddingLeft": "20dp",
                                                        "paddingRight": "20dp",
                                                        "paddingTop": "10dp",
                                                        "paddingBottom": "10dp",
                                                        "items": [
                                                            {
                                                                "type": "Text",
                                                                "text": "Please say the quantity as a number",
                                                                "fontSize": "20dp",
                                                                "color": "white",
                                                                "fontWeight": "500",
                                                                "textAlign": "center",
                                                                "fontFamily": "Amazon Ember"
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                      "type": "Container",
                                      "position": "absolute",
                                      "bottom": "0",
                                      "width": "100%",
                                      "height": "80dp",
                                      "backgroundColor": "rgba(0, 0, 0, 0.85)",
                                      "borderTopLeftRadius": "20dp",
                                      "borderTopRightRadius": "20dp",
                                      "paddingLeft": "20dp",
                                      "paddingRight": "20dp",
                                      "paddingTop": "30dp",
                                      "paddingBottom": "10dp",
                                      "alignItems": "center",
                                      "justifyContent": "center",
                                      "items": [
                                        {
                                          "type": "Container",
                                          "direction": "row",
                                          "alignItems": "center",
                                          "justifyContent": "center",
                                          "backgroundColor": "#C62828",
                                          "borderRadius": "12dp",
                                          "paddingTop": "12dp",
                                          "paddingBottom": "12dp",
                                          "paddingLeft": "20dp",
                                          "paddingRight": "20dp",
                                          "shadowColor": "black",
                                          "shadowOffset": {
                                            "width": 0,
                                            "height": 2
                                          },
                                          "width": "95%",
                                          "items": [
                                            {
                                              "type": "Text",
                                              "text": "<b>🎤 Say:</b> 2 • I want 4 • Add 8 • Make it 1 • 5 Please",
                                              "fontSize": "17dp",
                                              "fontWeight": "700",
                                              "color": "white",
                                              "fontFamily": "Amazon Ember",
                                              "textAlign": "center",
                                              "maxLines": 2
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

                if get_supported_interfaces(handler_input).alexa_presentation_apl:
                    handler_input.response_builder.add_directive(
                        RenderDocumentDirective(
                            token="singleItemToken",
                            document=quantity_apl,
                            datasources=apl_datasource
                        )
                    )

                return (
                    handler_input.response_builder
                        .speak(speak_output)
                        .ask("Please tell me the quantity.")
                        .response
                )
            else:
                logger.error(f"Item not found: {item_name}")
                return handler_input.response_builder.speak("Sorry, I couldn't find that item.").response

        return handler_input.response_builder.speak("Sorry, I didn't understand that.").response

# ---------------- PROVIDE QUANTITY HANDLER ----------------
class ProvideQuantityIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        
        # Only handle if we have a pending food item (correct context)
        return (ask_utils.is_intent_name("ProvideQuantityIntent")(handler_input) and 
                "pending_food" in session_attr)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        quantity = slots.get("quantity").value if slots.get("quantity") else None

        session_attr = handler_input.attributes_manager.session_attributes

        # Check if we have pending food item
        if "pending_food" not in session_attr:
            speak_output = "I don't have any item selected. Please choose an item first."
            return handler_input.response_builder.speak(speak_output).ask("What would you like to order?").response

        # Validate quantity
        if not quantity:
            speak_output = "I didn't catch the quantity. How many would you like?"
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response

        # Validate quantity is a valid positive number
        try:
            quantity_int = int(quantity)
            if quantity_int <= 0:
                speak_output = "Please provide a valid quantity greater than zero."
                return handler_input.response_builder.speak(speak_output).ask(speak_output).response
        except ValueError:
            speak_output = f"I didn't understand '{quantity}' as a number. Please tell me the quantity as a number."
            return handler_input.response_builder.speak(speak_output).ask(speak_output).response

        # Retrieve item details
        food_item_name = session_attr["pending_food"]
        price = int(session_attr.get("pending_price", 0))
        image = session_attr.get("pending_image", "")
        quantity_display = session_attr.get("pending_quantity_display", "")
        total_price = quantity_int * price

        # Initialize cart
        if "cart" not in session_attr:
            session_attr["cart"] = []

        # --- Check if item already exists ---
        existing_item = None
        for item in session_attr["cart"]:
            if item["name"].lower() == food_item_name.lower():
                existing_item = item
                break

        if existing_item:
            existing_item["quantity"] += quantity_int
            existing_item["total_price"] = existing_item["quantity"] * existing_item["price"]
            speak_output = (
                f"Updated your cart. You now have {existing_item['quantity']} {food_item_name} in total. "
            )
        else:
            session_attr["cart"].append({
                "name": food_item_name,
                "quantity": quantity_int,
                "price": price,
                "total_price": total_price,
                "image": image,
                "quantity_display": quantity_display
            })
            speak_output = f"Added {quantity_int} {food_item_name} to your cart. "

        # Clear pending item data
        session_attr.pop("pending_food", None)
        session_attr.pop("pending_price", None)
        session_attr.pop("pending_image", None)
        session_attr.pop("pending_quantity_display", None)

        # Calculate total
        overall_total = sum(item["total_price"] for item in session_attr["cart"])

        speak_output += (
            f"Your total cart value is now {overall_total} rupees. "
            "Would you like to order more?"
        )

        # Set state to track we're waiting for yes/no response
        session_attr["awaiting_order_more_response"] = True

        # Build dynamic cart display
        cart_item_rows = []
        for idx, item in enumerate(session_attr["cart"], start=1):
            cart_item_rows.append({
                "type": "Container",
                "direction": "row",
                "width": "95%",
                "height": "130dp",
                "backgroundColor": "rgba(255,255,255,0.08)",
                "borderRadius": "12dp",
                "borderWidth": "2dp",
                "borderColor": "#27ae60",
                "alignItems": "center",
                "justifyContent": "center",
                "paddingLeft": "15dp",
                "paddingRight": "15dp",
                "paddingTop": "10dp",
                "paddingBottom": "10dp",
                "spacing": "10dp",
                "items": [
                    {
                        "type": "Text",
                        "text": str(idx),
                        "fontSize": "26dp",
                        "color": "#8B0000",
                        "fontWeight": "600",
                        "width": "10%",
                        "textAlign": "center",
                        "alignSelf": "center",
                        "fontFamily": "Amazon Ember",
                        "paddingRight": "55dp"
                    },
                    {
                        "type": "Container",
                        "width": "20%",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "paddingRight": "40dp",
                        "items": [
                            {
                                "type": "Image",
                                "source": item["image"],
                                "width": "90dp",
                                "height": "90dp",
                                "borderRadius": "45dp",
                                "borderWidth": "2dp",
                                "borderColor": "#27ae60",
                                "scale": "best-fill"
                            }
                        ]
                    },
                    {
                        "type": "Text",
                        "text": item["name"],
                        "fontSize": "28dp",
                        "color": "#7b47ba",
                        "fontWeight": "600",
                        "width": "25%",
                        "textAlign": "center",
                        "alignSelf": "center",
                        "fontFamily": "Amazon Ember",
                        "paddingRight": "10dp"
                    },
                    {
                        "type": "Text",
                        "text": str(item["quantity"]),
                        "fontSize": "26dp",
                        "color": "#7b47ba",
                        "fontWeight": "500",
                        "width": "10%",
                        "textAlign": "center",
                        "alignSelf": "center",
                        "fontFamily": "Amazon Ember",
                        "paddingRight": "25dp"
                    },
                    {
                        "type": "Text",
                        "text": f"₹{item['total_price']}",
                        "fontSize": "28dp",
                        "color": "#27ae60",
                        "fontWeight": "bold",
                        "width": "15%",
                        "textAlign": "center",
                        "alignSelf": "center",
                        "fontFamily": "Amazon Ember",
                        "paddingRight": "20dp"
                    },
                    {
                        "type": "TouchWrapper",
                        "width": "50dp",
                        "height": "50dp",
                        "onPress": [],
                        "item": {
                            "type": "Frame",
                            "width": "100%",
                            "height": "100%",
                            "backgroundColor": "#B22222",
                            "borderRadius": "25dp",
                            "borderWidth": "2dp",
                            "borderColor": "#8B0000",
                            "items": [
                                {
                                    "type": "Text",
                                    "text": "✕",
                                    "fontSize": "32dp",
                                    "fontWeight": "bold",
                                    "color": "white",
                                    "textAlign": "center",
                                    "fontFamily": "Amazon Ember",
                                    "width": "100%",
                                    "height": "100%",
                                    "textAlignVertical": "center"
                                }
                            ],
                            "alignItems": "center",
                            "paddingTop":"5dp",
                            "paddingLeft":"3dp",
                            "justifyContent": "center"
                        }
                    }

                ]
            })

        # APL Layout
        apl_doc = {
            "type": "APL",
            "version": "1.7",
            "mainTemplate": {
                "parameters": ["payload"],
                "items": [
                    {
                        "type": "Container",
                        "width": "100vw",
                        "height": "100vh",
                        "alignItems": "center",
                        "justifyContent": "start",
                        "items": [
                            {
                                "type": "Image",
                                "source": "https://media.istockphoto.com/id/922930296/video/grey-abstract-background.jpg?s=640x640&k=20&c=JTQRynekqaCHvt7Cu4xYdnHXrwKAprS_KTJJvAN5Us4=",
                                "scale": "best-fill",
                                "width": "100%",
                                "height": "100%",
                                "position": "absolute"
                            },
                            {
                                "type": "ScrollView",
                                "width": "100%",
                                "height": "100%",
                                "item": {
                                    "type": "Container",
                                    "direction": "column",
                                    "alignItems": "center",
                                    "justifyContent": "start",
                                    "width": "100%",
                                    "paddingTop": "40dp",
                                    "paddingBottom": "120dp",
                                    "items": [
                                        {
                                            "type": "Text",
                                            "text": "🛒 CART ITEMS",
                                            "fontSize": "48dp",
                                            "color": "#000000",
                                            "fontWeight": "bold",
                                            "paddingBottom": "30dp",
                                            "fontFamily": "Amazon Ember"
                                        },
                                        {
                                            "type": "Container",
                                            "direction": "row",
                                            "width": "95%",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "paddingBottom": "10dp",
                                            "items": [
                                                {"type": "Text","text": "No.","fontSize": "24dp","color": "#000000","fontWeight": "bold","width": "10%","textAlign": "center", "fontFamily": "Amazon Ember"},
                                                {"type": "Text","text": "Image","fontSize": "24dp","color": "#000000","fontWeight": "bold","width": "20%","textAlign": "center", "fontFamily": "Amazon Ember"},
                                                {"type": "Text","text": "Item","fontSize": "24dp","color": "#000000","fontWeight": "bold","width": "25%","textAlign": "center", "fontFamily": "Amazon Ember"},
                                                {"type": "Text","text": "Qty","fontSize": "24dp","color": "#000000","fontWeight": "bold","width": "10%","textAlign": "center", "fontFamily": "Amazon Ember"},
                                                {"type": "Text","text": "Price","fontSize": "24dp","color": "#000000","fontWeight": "bold","width": "15%","textAlign": "center", "fontFamily": "Amazon Ember"},
                                                {"type": "Text","text": "Remove","fontSize": "24dp","color": "#000000","fontWeight": "bold","width": "10%","textAlign": "center", "fontFamily": "Amazon Ember"}
                                            ]
                                        },
                                        {
                                            "type": "Container",
                                            "direction": "column",
                                            "width": "100%",
                                            "alignItems": "center",
                                            "spacing": "15dp",
                                            "items": cart_item_rows
                                        },
                                        {"type": "Text","text": "========================================","color": "#7b47ba","fontSize": "22dp","paddingTop": "15dp","paddingBottom": "15dp", "fontFamily": "Amazon Ember"},
                                        {
                                            "type": "Container",
                                            "direction": "row",
                                            "width": "80%",
                                            "alignItems": "center",
                                            "justifyContent": "spaceBetween",
                                            "items": [
                                                {"type": "Text","text": "Total Price","fontSize": "32dp","color": "#000000","fontWeight": "bold", "fontFamily": "Amazon Ember"},
                                                {"type": "Text","text": f"₹{overall_total}","fontSize": "32dp","color": "#27ae60","fontWeight": "bold", "fontFamily": "Amazon Ember"}
                                            ]
                                        },
                                        {
                                            "type": "Text",
                                            "text": "Would you like to order more?",
                                            "fontSize": "28dp",
                                            "color": "white",
                                            "paddingTop": "30dp",
                                            "fontFamily": "Amazon Ember",
                                            "textAlign": "center"
                                        }
                                    ]
                                }
                            },
                            {
                                "type": "TouchWrapper",
                                "position": "absolute",
                                "bottom": "30dp",
                                "left": "30dp",
                                "width": "100dp",
                                "height": "50dp",
                                "onPress": [
                                    {
                                        "type": "SendEvent",
                                        "arguments": ["YES"]
                                    }
                                ],
                                "item": {
                                    "type": "Frame",
                                    "width": "100%","height": "100%",
                                    "backgroundColor": "#27ae60",
                                    "borderRadius": "12dp",
                                    "borderWidth": "3dp",
                                    "borderColor": "#1e8449",
                                    "paddingTop": "4dp",
                                    "items": [{"type": "Text","text": "YES","fontSize": "26dp","fontWeight": "bold","color": "white","textAlign": "center","width": "100%","height": "100%","textAlignVertical": "center", "fontFamily": "Amazon Ember"}]
                                }
                            },
                            {
                                "type": "TouchWrapper",
                                "position": "absolute",
                                "right": "30dp",
                                "bottom": "30dp",
                                "width": "100dp",
                                "height": "50dp",
                                "onPress": [
                                    {
                                        "type": "SendEvent",
                                        "arguments": ["NO"]
                                    }
                                ],
                                "item": {
                                    "type": "Frame",
                                    "width": "100%","height": "100%",
                                    "backgroundColor": "#B22222",
                                    "borderRadius": "12dp",
                                    "borderWidth": "3dp",
                                    "borderColor": "#8B0000",
                                    "paddingTop": "4dp",
                                    "items": [{"type": "Text","text": "NO","fontSize": "26dp","fontWeight": "bold","color": "white","textAlign": "center","width": "100%","height": "100%","textAlignVertical": "center", "fontFamily": "Amazon Ember"}]
                                }
                            }
                        ]
                    }
                ]
            }
        }

        # Send APL if device supports it
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token="cartConfirmToken",
                    document=apl_doc
                )
            )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to order more?")
                .response
        )


class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        
        # ✅ PRIORITY 1: Cab Service - "Would you like to book another cab?"
        if session_attr.get("awaiting_cab_another_response"):
            session_attr.pop("awaiting_cab_another_response", None)
            
            room_numbers = [101, 105, 110, 103, 114, 108, 117]
            room_number = random.choice(room_numbers)
            session_attr["cab_room_number"] = room_number
            
            # Clear previous booking data but keep cab_booking_active
            session_attr.pop("cab_destination", None)
            # ✅ Call BookCabIntentHandler directly
            cab_handler = BookCabIntentHandler()
            return cab_handler.handle(handler_input)

            
        # ✅ FIRST: Room Service - "Do you need anything else?"
        elif 'room_number' in session_attr:
            logger.info(f"User said YES in room service - keeping room number {session_attr['room_number']}")
            
            speak_output = "What else would you like?"
            
            # Show room service menu again
            from room_service import RoomServiceIntentHandler
            return RoomServiceIntentHandler().handle(handler_input)

        # ✅ FIRST YES/NO: Cart confirmation - "Would you like to order more?"
        elif session_attr.get("awaiting_order_more_response"):
            session_attr.pop("awaiting_order_more_response", None)
            session_attr["awaiting_menu_selection"] = True
            
            speak_output = "Great! Would you like to see Main Menu?"

            # Your menu selection APL (the one with SUB MENU and MAIN MENU buttons)
            apl_doc = apl_doc = {
                "type": "APL",
                "version": "1.7",
                "mainTemplate": {
                    "parameters": ["payload"],
                    "items": [
                        {
                            "type": "Container",
                            "width": "100vw",
                            "height": "100vh",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "items": [
                                {
                                    "type": "Image",
                                    "source": "https://media.istockphoto.com/id/922930296/video/grey-abstract-background.jpg?s=640x640&k=20&c=JTQRynekqaCHvt7Cu4xYdnHXrwKAprS_KTJJvAN5Us4=",
                                    "scale": "best-fill",
                                    "width": "100%",
                                    "height": "100%",
                                    "position": "absolute"
                                },
                                {
                                    "type": "Container",
                                    "direction": "column",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "width": "90%",
                                    "items": [
                                        {
                                            "type": "Text",
                                            "text": "🍽️ CHOOSE YOUR MENU",
                                            "fontSize": "52dp",
                                            "color": "#000000",
                                            "fontWeight": "bold",
                                            "paddingBottom": "20dp",
                                            "fontFamily": "Amazon Ember",
                                            "textAlign": "center"
                                        },
                                        {
                                            "type": "Text",
                                            "text": "Would you like to see Main menu?",
                                            "fontSize": "28dp",
                                            "color": "#000000",
                                            "paddingBottom": "30dp",
                                            "fontFamily": "Amazon Ember",
                                            "textAlign": "center"
                                        },
                                        {
                                            "type": "Container",
                                            "direction": "row",
                                            "width": "100%",
                                            "alignItems": "center",
                                            "justifyContent": "spaceAround",
                                            "spacing": "40dp",
                                            "items": [
                                                {
                                                    "type": "TouchWrapper",
                                                    "width": "220dp",
                                                    "height": "130dp",
                                                    "onPress": [
                                                        {
                                                            "type": "SendEvent",
                                                            "arguments": ["mainmenu"]
                                                        }
                                                    ],
                                                    "item": {
                                                        "type": "Frame",
                                                        "width": "100%",
                                                        "height": "100%",
                                                        "backgroundColor": "rgba(41, 128, 185, 0.9)",
                                                        "borderRadius": "18dp",
                                                        "borderWidth": "4dp",
                                                        "borderColor": "#1f618d",
                                                        "items": [
                                                            {
                                                                "type": "Container",
                                                                "width": "100%",
                                                                "height": "100%",
                                                                "alignItems": "center",
                                                                "justifyContent": "center",
                                                                "direction": "column",
                                                                "items": [
                                                                    {
                                                                        "type": "Text",
                                                                        "text": "MAIN MENU",
                                                                        "fontSize": "28dp",
                                                                        "fontWeight": "bold",
                                                                        "color": "white",
                                                                        "textAlign": "center",
                                                                        "fontFamily": "Amazon Ember"
                                                                    },
                                                                    {
                                                                        "type": "Text",
                                                                        "text": "View all items",
                                                                        "fontSize": "18dp",
                                                                        "color": "#e3f2fd",
                                                                        "textAlign": "center",
                                                                        "paddingTop": "6dp",
                                                                        "fontFamily": "Amazon Ember"
                                                                    }
                                                                ]
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    "type": "TouchWrapper",
                                                    "width": "220dp",
                                                    "height": "130dp",
                                                    "onPress": [
                                                        {
                                                            "type": "SendEvent",
                                                            "arguments": ["submenu"]
                                                        }
                                                    ],
                                                    "item": {
                                                        "type": "Frame",
                                                        "width": "100%",
                                                        "height": "100%",
                                                        "backgroundColor": "rgba(39, 174, 96, 0.9)",
                                                        "borderRadius": "18dp",
                                                        "borderWidth": "4dp",
                                                        "borderColor": "#1e8449",
                                                        "items": [
                                                            {
                                                                "type": "Container",
                                                                "width": "100%",
                                                                "height": "100%",
                                                                "alignItems": "center",
                                                                "justifyContent": "center",
                                                                "direction": "column",
                                                                "items": [
                                                                    
                                                                    {
                                                                        "type": "Text",
                                                                        "text": "SUB MENU",
                                                                        "fontSize": "28dp",
                                                                        "fontWeight": "bold",
                                                                        "color": "white",
                                                                        "textAlign": "center",
                                                                        "fontFamily": "Amazon Ember"
                                                                    },
                                                                    {
                                                                        "type": "Text",
                                                                        "text": "Browse categories",
                                                                        "fontSize": "18dp",
                                                                        "color": "#e8f5e9",
                                                                        "textAlign": "center",
                                                                        "paddingTop": "6dp",
                                                                        "fontFamily": "Amazon Ember"
                                                                    }
                                                                ]
                                                            }
                                                        ]
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                            "type": "TouchWrapper",
                                            "position": "absolute",
                                            "bottom": "30dp",
                                            "left": "30dp",
                                            "width": "100dp",
                                            "height": "50dp",
                                            "onPress": [
                                                {
                                                    "type": "SendEvent",
                                                    "arguments": ["mainmenu"]
                                                }
                                            ],
                                            "item": {
                                                "type": "Frame",
                                                "width": "100%","height": "100%",
                                                "backgroundColor": "#27ae60",
                                                "borderRadius": "12dp",
                                                "borderWidth": "3dp",
                                                "borderColor": "#1e8449",
                                                "paddingTop": "4dp",
                                                "items": [{"type": "Text","text": "YES","fontSize": "26dp","fontWeight": "bold","color": "white","textAlign": "center","width": "100%","height": "100%","textAlignVertical": "center", "fontFamily": "Amazon Ember"}]
                                            }
                                        },
                                {
                                            "type": "TouchWrapper",
                                            "position": "absolute",
                                            "right": "30dp",
                                            "bottom": "30dp",
                                            "width": "100dp",
                                            "height": "50dp",
                                            "onPress": [
                                                {
                                                    "type": "SendEvent",
                                                    "arguments": ["submenu"]
                                                }
                                            ],
                                            "item": {
                                                "type": "Frame",
                                                "width": "100%","height": "100%",
                                                "backgroundColor": "#B22222",
                                                "borderRadius": "12dp",
                                                "borderWidth": "3dp",
                                                "borderColor": "#8B0000",
                                                "paddingTop": "4dp",
                                                "items": [{"type": "Text","text": "NO","fontSize": "26dp","fontWeight": "bold","color": "white","textAlign": "center","width": "100%","height": "100%","textAlignVertical": "center", "fontFamily": "Amazon Ember"}]
                                            }
                                        }
                            ]
                        }
                    ]
                }
            }

            if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
                handler_input.response_builder.add_directive(
                    RenderDocumentDirective(
                        token="menuSelectionToken",
                        document=apl_doc
                    )
                )

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask("Say sub menu or main menu.")
                    .response
            )

        # ✅ SECOND YES: Menu selection - "Would you like to see Main Menu?"
        elif session_attr.get("awaiting_menu_selection"):
            session_attr.pop("awaiting_menu_selection", None)
            
            # ✅ Directly call your existing menu handler
            menu_handler = MenuIntentHandler()  # or LaunchRequestHandler() - whatever your menu handler is called
            return menu_handler.handle(handler_input)

        else:
            return handler_input.response_builder.speak(
                "I heard yes, but I'm not sure what you mean."
            ).ask("What would you like to do?").response
    
def send_food_order_whatsapp(room_number, cart_items, total_price):
    """Send WhatsApp notification with complete cart details and total price."""
    try:
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        twilio_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_FROM')
        recipient_phone = os.environ.get('RECIPIENT_PHONE')

        if not all([account_sid, auth_token, twilio_whatsapp_number, recipient_phone]):
            logger.error("Twilio env variables missing (SID, Token, From, or Recipient Phone)")
            return False

        client = Client(account_sid, auth_token)

        # Build cart items list
        cart_details = ""
        for idx, item in enumerate(cart_items, start=1):
            cart_details += (
                f"{idx}. {item['name']}\n"
                f"   Quantity: {item['quantity']}\n"
                f"   Price per item: ₹{item['price']}\n"
                f"   Subtotal: ₹{item['total_price']}\n\n"
            )

        message_body = (
            f"🍽️ *Mera Mehmaan – Food Order*\n\n"
            f"Room Number: {room_number}\n"
            f"{'='*30}\n\n"
            f"*ORDER DETAILS:*\n\n"
            f"{cart_details}"
            f"{'='*30}\n"
            f"*TOTAL AMOUNT: ₹{total_price}*\n"
            f"{'='*30}\n\n"
            f"Please prepare and deliver it to Room {room_number} shortly.\n"
        )

        client.messages.create(
            from_=twilio_whatsapp_number,
            to=f"whatsapp:{recipient_phone}",
            body=message_body
        )

        logger.info(f"Food order WhatsApp message sent successfully to {recipient_phone} for room {room_number}")
        return True

    except Exception as e:
        logger.error(f"Food order WhatsApp send failed: {e}", exc_info=True)
        return False

class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)
    
    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        
        # ✅ PRIORITY 1: Cab Service - "Would you like to book another cab?"
        if session_attr.get("awaiting_cab_another_response"):
            logger.info("NO in cab context - returning to launch screen")
            session_attr["awaiting_cab_another_response"] = False
            
            # Clear all cab-related session data
            session_attr.pop("cab_booking_active", None)
            session_attr.pop("cab_room_number", None)
            session_attr.pop("cab_destination", None)
            
            speak_output = "Thank you for using our cab service. How may I help you?"
            
            # Return to launch screen
            return LaunchRequestHandler().handle(handler_input)
            
        elif session_attr.get("awaiting_order_more_response"):
            session_attr.pop("awaiting_order_more_response", None)

            # Get cart details and room number for WhatsApp
            ROOM_NUM = [101, 102, 104, 106, 108, 110, 112]

            # Assign room number if not already assigned
            if 'room_num' not in session_attr:
                session_attr['room_num'] = random.choice(ROOM_NUM)
            
            room_num = session_attr['room_num']
            cart_items = session_attr.get("cart", [])
            overall_total = sum(item["total_price"] for item in cart_items)
            
            # Send WhatsApp notification with cart details
            if cart_items:
                logger.info(f"Sending food order to WhatsApp for room {room_num}")
                send_food_order_whatsapp(room_num, cart_items, overall_total)
            
            # Clear cart after order is placed
            session_attr.pop("cart", None)
            
            speak_output = "Your order has been received and will be delivered shortly. Thank you"
            
            # Thank you APL screen
            apl_doc = {
                "type": "APL",
                "version": "1.7",
                "mainTemplate": {
                    "parameters": ["payload"],
                    "items": [
                        {
                            "type": "Container",
                            "width": "100vw",
                            "height": "100vh",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "items": [
                                # Background
                                {
                                    "type": "Image",
                                    "source": "https://media.istockphoto.com/id/922930296/video/grey-abstract-background.jpg?s=640x640&k=20&c=JTQRynekqaCHvt7Cu4xYdnHXrwKAprS_KTJJvAN5Us4=",
                                    "scale": "best-fill",
                                    "width": "100%",
                                    "height": "100%",
                                    "position": "absolute"
                                },
                                
                                # Thank you container
                                {
                                    "type": "Container",
                                    "direction": "column",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "paddingLeft": "40dp",
                                    "paddingRight": "40dp",
                                    "items": [
                                        # Order placed heading
                                        {
                                            "type": "Text",
                                            "text": "ORDER PLACED!",
                                            "fontSize": "48dp",
                                            "color": "#27ae60",
                                            "fontWeight": "bold",
                                            "textAlign": "center",
                                            "paddingBottom": "20dp",
                                            "fontFamily": "Amazon Ember"
                                        },
                                        
                                        # Message
                                        {
                                            "type": "Text",
                                            "text": "Your order has been received and will be delivered shortly",
                                            "fontSize": "28dp",
                                            "color": "#000000",
                                            "fontWeight": "600",
                                            "textAlign": "center",
                                            "paddingBottom": "10dp",
                                            "fontFamily": "Amazon Ember"
                                        },
                                        
                                        # Thank you icon
                                        {
                                            "type": "Text",
                                            "text": "🙏",
                                            "fontSize": "100dp",
                                            "paddingBottom": "10dp",
                                            "fontFamily": "Amazon Ember"
                                        },
                                        
                                        # Thank you heading
                                        {
                                            "type": "Text",
                                            "text": "THANK YOU!",
                                            "fontSize": "56dp",
                                            "color": "#000000",
                                            "fontWeight": "bold",
                                            "textAlign": "center",
                                            "paddingBottom": "20dp",
                                            "fontFamily": "Amazon Ember"
                                        },
                                        
                                        # Have a great day
                                        {
                                            "type": "Frame",
                                            "backgroundColor": "rgba(255,215,0,0.15)",
                                            "borderRadius": "16dp",
                                            "borderWidth": "2dp",
                                            "borderColor": "#FFD700",
                                            "paddingLeft": "40dp",
                                            "paddingRight": "40dp",
                                            "paddingTop": "20dp",
                                            "paddingBottom": "20dp",
                                            "items": [
                                                {
                                                    "type": "Text",
                                                    "text": "Have a Great Day! 😊",
                                                    "fontSize": "28dp",
                                                    "color": "#27ae60",
                                                    "fontWeight": "600",
                                                    "textAlign": "center",
                                                    "fontFamily": "Amazon Ember"
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
            
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .add_directive(
                        RenderDocumentDirective(
                            document=apl_doc
                        )
                    )
                    .response
            )
        
        elif 'room_number' in session_attr:
            room_number = session_attr['room_number']
            logger.info(f"User said NO to room service - clearing room number {room_number}")
            session_attr.pop('room_number', None)
            
            speak_output = "Thank you for using our room service. How may I help you?"
            
            # Return to launch screen
            return LaunchRequestHandler().handle(handler_input)
            
        # ✅ SECOND NO: Menu selection - Go back to last category
        elif session_attr.get("awaiting_menu_selection"):
            logger.info("NO pressed - attempting to return to last category")
            session_attr.pop("awaiting_menu_selection", None)
            
            # ✅ Check if user has a last_category stored
            last_category = session_attr.get("last_category")
            
            if last_category and last_category in sub_menu_items:
                logger.info(f"Returning to last category: {last_category}")
                
                # ✅ SOLUTION: Temporarily change request type and add arguments
                original_request_type = handler_input.request_envelope.request.object_type
                
                # Change to APL UserEvent type so SubMenuIntentHandler can handle it
                handler_input.request_envelope.request.object_type = "Alexa.Presentation.APL.UserEvent"
                handler_input.request_envelope.request.arguments = ["item_tap", last_category]
                
                # Create and call SubMenuIntentHandler
                submenu_handler = SubMenuIntentHandler()
                response = submenu_handler.handle(handler_input)
                
                # Restore original request type (optional cleanup)
                handler_input.request_envelope.request.object_type = original_request_type
                
                return response
            
        else:
            return (
                handler_input.response_builder
                    .speak("I heard no, but I'm not sure what you mean.")
                    .ask("What would you like to do?")
                    .response
            )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors."""
    
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speak_output = (
            "Sorry, I had trouble processing your request. "
            "Please try again."
        )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Welcome to Mera Mehmaan! "
            "You can say: Room Service for housekeeping needs, "
            "Menu or Food to order from our restaurant, "
            "or Book a Cab for transportation. "
            "What would you like to do?"
        )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Thank you for choosing Mera Mehmaan. Have a wonderful day! Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here
        logger.info("Session ended")
        return handler_input.response_builder.response


class NavigateHomeIntentHandler(AbstractRequestHandler):
    """Handler for Navigate Home Intent."""
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NavigateHomeIntent")(handler_input)

    def handle(self, handler_input):
        # Return to main menu
        menu_handler = MenuIntentHandler()
        return menu_handler.handle(handler_input)

# ---------------- APL USER EVENT HANDLER (for YES/NO buttons) ----------------
class APLUserEventHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        if ask_utils.is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            arguments = handler_input.request_envelope.request.arguments
            # Handle yes/no button taps, and submenu/mainmenu selection
            if arguments and arguments[0] in ["YES", "NO", "submenu", "mainmenu"]:
                return True
        return False

    def handle(self, handler_input):
        arguments = handler_input.request_envelope.request.arguments
        logger.info(f"APL UserEvent received with arguments: {arguments}")
        
        if not arguments:
            return handler_input.response_builder.speak("Sorry, I didn't catch that selection.").response

        action = arguments[0].lower()
        session_attr = handler_input.attributes_manager.session_attributes

        # Handle YES button press
        if action == "yes":
            logger.info("YES button pressed - routing to YesIntentHandler")
            yes_handler = YesIntentHandler()
            return yes_handler.handle(handler_input)
        
        # Handle NO button press
        elif action == "no":
            logger.info("NO button pressed - routing to NoIntentHandler")
            no_handler = NoIntentHandler()
            return no_handler.handle(handler_input)
        
        # Handle Sub Menu button press - go back to last browsed category
        elif action == "submenu":
            logger.info("Sub Menu button pressed")
            session_attr.pop("awaiting_menu_selection", None)
            
            # ✅ Check if user has a last_category stored
            last_category = session_attr.get("last_category")
            
            if last_category and last_category in sub_menu_items:
                logger.info(f"Returning to last category: {last_category}")
                # Create a SubMenuIntentHandler and simulate category selection
                submenu_handler = SubMenuIntentHandler()
                
                # Simulate the category being selected via touch event
                handler_input.request_envelope.request.arguments = ["item_tap", last_category]
                
                return submenu_handler.handle(handler_input)
            else:
                # No last category or invalid - show category selection
                logger.info("No valid last_category found - showing category menu")
                menu_handler = MenuIntentHandler()
                return menu_handler.handle(handler_input)
        
        # Handle Main Menu button press - show all categories
        elif action == "mainmenu":
            logger.info("Main Menu button pressed - showing category selection")
            session_attr.pop("awaiting_menu_selection", None)
            menu_handler = MenuIntentHandler()
            return menu_handler.handle(handler_input)

        return handler_input.response_builder.speak("Sorry, I didn't understand that action.").response 


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Sorry, I didn't understand that. You can say again."
        reprompt = "Try saying, anything you want."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

# ---------------- REGISTER HANDLERS ----------------
sb = SkillBuilder()

# 1. Launch Handler
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PhoneNumberIntentHandler())
sb.add_request_handler(PhoneSubmittedEventHandler())

# 2. Room Service Handlers
for handler in ROOM_SERVICE_HANDLERS:
    sb.add_request_handler(handler)
    
# 3. Launch Button Handlers
sb.add_request_handler(LaunchMenuUserEventHandler())
sb.add_request_handler(LaunchCabUserEventHandler())

# 4. Standard Amazon Intents
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(NavigateHomeIntentHandler())

# 5. Cab Booking Handlers (WITHOUT Yes/No - those are unified now)
sb.add_request_handler(BookCabIntentHandler())
sb.add_request_handler(ProvideDestinationIntentHandler())
sb.add_request_handler(ProvideTimeIntentHandler())

# 6. Food Ordering Handlers
sb.add_request_handler(MenuIntentHandler())
sb.add_request_handler(SubMenuIntentHandler())
sb.add_request_handler(OrderFoodIntentHandler())
sb.add_request_handler(GoBackIntentHandler())
sb.add_request_handler(UserEventHandler())
sb.add_request_handler(ProvideQuantityIntentHandler())

# 7. UNIFIED Yes/No Handlers (handles all contexts)
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(APLUserEventHandler())

# 8. Fallback and Session End
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# 9. Exception Handler
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()