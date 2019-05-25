import re
from flask import Flask, render_template, request
import random

app = Flask(__name__)

###### Endpoints ######

# Index / 'home' page - works for GET or POST 
@app.route("/")
def index():
    return render_template('index.html')


# POST the user-bot interaction 
@app.route("/", methods=['POST'])
def register():
    
    # Create templates
    bot_template = "Cannabis Rep : {0}"
    user_template = "USER : {0}"

    keywords = {'strain sativa': ['sativa'],
    'strain indica': ['indica'],
    'seeds': ['seed', 'seeds' ],
    'femanized':['femanized'],
    'non-femanized':['non-femanized','non femenaized'],
    'greet': ['hello', 'hi', 'hey', 'menu'],
    'cannabis': ['flowers', 'order cannabis', 'order flowers'],
 #   'cannabisquantity': [''],
    'fuckyou': ['fuck you']}

    responses = {'default': "Sorry, I didn't understand that.  Say 'menu' to start over, 'order' for cannabis.",
    'strain sativa': 'Our sativa strains: Bubble Kush, and Sour Desiel! Say "menu" to start again',
    'strain indica': 'Our sativa strains: Berry Kush, and Sour Cookies Say "menu" to start again',
    'seeds': 'Sure, femanized or non-femanized?',
    'femanized': 'Our femanized strains in stock today are: This Strain, That Strain',
    'non-femanized': 'Our non-femanized strains in stock today are: Fire Strain, and Bomb Strain',
    'type': 'Great! How many grams?',
    'greet': "Would you like seeds, or flowers today?",
    'cannabis': 'What kind of strain would you like? Sativa or indica',
    'fuckyou':"fuck you too!"
    }
    
    # Define an empty dictionary of patterns
    patterns = {}
    
    # Get form text
    meal_order=request.form['meal_order']

    # Iterate over the keywords dictionary
    for intent, keys in keywords.items():
    # Create regular expressions and compile them into pattern objects
        patterns[intent] = re.compile('|'.join(keys))

# Print the patterns
#print(patterns)


    # Define a function to find the intent of a message
    def match_intent(meal_order):
        matched_intent = None
        # Define intent, pattern as new iterator variables ask keys and values 
        #of the dict patterns
        for intent, pattern in patterns.items():
            # Check if the pattern occurs in the message 
            if pattern.search(meal_order):
                matched_intent = intent
        return matched_intent

    # Define a respond function
    def respond(meal_order):
        # Call the match_intent function, save to var called intent
        intent = match_intent(meal_order)
        # Fall back to the default response, save to var called key
        key = "default"
        if intent in responses:
            key = intent
        return responses[key]

    def send_message(meal_order):
        # return user_template including the user_message
        return user_template.format(meal_order)
    # Get the bot's response to the message
    response = respond(meal_order)
    # return the bot template including the bot's response.
    return render_template('index.html', meal_order=bot_template.format(response), drink_order=user_template.format(meal_order))

### Run APP ###
if __name__ == "__main__":
    app.run(port=8080)




"""
Similar technique but looking for name keywords, and then returning those words
with a particular response
"""

"""
# Define find_name()
def find_name(message):
    name = None
    # Create a pattern for checking if the keywords occur
    name_keyword = re.compile("name|call")
    # Create a pattern for finding capitalized words
    name_pattern = re.compile("[A-Z]{1}[a-z]*")
    if name_keyword.search(message):
        # Get the matching words in the string
        name_words = name_pattern.findall(message)
        if len(name_words) > 0:
            # Return the name if the keywords are present
            name = ' '.join(name_words)
    return name



# Send messages
send_message("my name is David Copperfield")
send_message("call me Ishmael")
send_message("People call me Cassandra")

"""
