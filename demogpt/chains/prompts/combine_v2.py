system_template = """
Regenerate the code by combining all the user input parts into st.form.
It is really important not to change other parts.
Copy all the function definitions and library imports as is and don't modify or replace them.
Combine input-related parts under the st.form.
If a function needs an input from user via st.text_input, put it between st.form and st.form_submit_button so that the state is preserved.
Show the result when the form is submitted under the if submit_button: statement.
Keep in mind that don't miss any function definition.

Don't forget to add those functions with their original definitions as is 

{function_names}

Always put "if submit_button:" inside of st.form block
"""

human_template = """
=============================================================
DRAFT CODE 1:
# all imports

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

def foo1():
    result = "res"
    return result

half_story = foo1()

if half_story:
    st.write(half_story)

user_choice = st.selectbox("What would you like to do next?", ["Choice1", "Choice2"])

def foo2(half_story,user_choice):
    result = half_story + user_choice
    return result

if half_story and user_choice:
    continued_story = foo2(half_story,user_choice)
else:
    continued_story = ""

if continued_story:
    st.markdown(continued_story)
#############################################################
FINAL CODE 1:
# all imports

# all functions

openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

def foo1():
    result = "res"
    return result

def foo2(half_story,user_choice):
    result = half_story + user_choice
    return result
    
with st.form(key='story_game'):
    # take all user inputs
	text_input = st.text_input(label='Enter some text')
    user_choice = st.selectbox("What would you like to do next?", ["Choice1", "Choice2"])
	submit_button = st.form_submit_button(label='Submit Story')
    # run functions if submit button is pressed
    if submit_button:
        half_story = foo1()
        if half_story:
            st.write(half_story)
        if text_input and user_choice :
            continued_story = foo2(text_input,user_choice)
        else:
            continued_story = ""
        if continued_story:
            st.markdown(continued_story)
    else: # if not submitted yet, we need to initizalize continued_story to get rid of name error
        continued_story = ""
#############################################################


=============================================================
DRAFT CODE 2:
{code_snippets}
#############################################################
FINAL CODE 2:

"""
