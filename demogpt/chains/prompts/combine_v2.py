system_template = """
Regenerate the code by combining all the user input parts into st.form.
It is really important not to change other parts and the final code should be error-free.
Copy all the function definitions and library imports as is and don't modify or replace them.
Show the result when the form is submitted under the if submit_button: statement.
Keep in mind that don't miss any function definition
Don't forget to add those functions with their original definitions as is 

If a library is imported even in the middle of the code, import the same library in the final code as well.

{function_names}

The final code content should be in the following format.
1. All library imports anywhere in the code
2. Get openai_api_key
3. Copy and paste all the functions as is
4. Create only a single global form
5. Under the global form, take all the user inputs
6. If form is submitted by st.form_submit_button run the logic
7. Under the st.form_submit_button, show the results.
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
# All library imports

# Get openai_api_key
openai_api_key = st.sidebar.text_input(
    "OpenAI API Key",
    placeholder="sk-...",
    value=os.getenv("OPENAI_API_KEY", ""),
    type="password",
)

### Copy and paste all the functions as is

def foo1():
    result = "res"
    return result

def foo2(half_story,user_choice):
    result = half_story + user_choice
    return result
    

### Create a form

with st.form(key='story_game'):
    # Under the form, take all the user inputs
	text_input = st.text_input(label='Enter some text')
    user_choice = st.selectbox("What would you like to do next?", ["Choice1", "Choice2"])
	submit_button = st.form_submit_button(label='Submit Story')
    # If form is submitted by st.form_submit_button run the logic
    if submit_button:
        half_story = foo1()
        if half_story:
            #Under the st.form_submit_button, show the results.
            st.write(half_story)
        if text_input and user_choice :
            continued_story = foo2(text_input,user_choice)
        else:
            continued_story = ""
        if continued_story:
            #Under the st.form_submit_button, show the results.
            st.markdown(continued_story)
#############################################################


=============================================================
DRAFT CODE 2:
{code_snippets}
#############################################################
FINAL CODE 2:

"""
