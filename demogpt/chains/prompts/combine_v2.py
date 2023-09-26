system_template = """
Regenerate the code by only combining the input parts into st.form.
It is really important not to change other parts.
Copy all the function definitions and library imports as is and don't modify or replace them.
Combine input-related parts under the st.form.
If a function needs an input from user via st.text_input, put it between st.form and st.form_submit_button so that the state is preserved.
Show the result when the form is submitted.
Keep in mind that don't miss any function definition.

Don't forget to add those functions with their original definitions as is 

{function_names}
"""

human_template = """
=============================================================
DRAFT CODE 1:
# all imports

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

def foo1():
    result = "res"
    return result

half_story = foo1()

if half_story:
    st.write(half_story)

def foo2(half_story,user_choice):
    result = half_story + user_choice
    return result
    
with st.form(key='story_game'):
	text_input = st.text_input(label='Enter some text')
    user_choice = st.selectbox("What would you like to do next?", ["Choice1", "Choice2"])
	submit_button = st.form_submit_button(label='Submit Story')
    if submit_button:
        if text_input and user_choice :
            continued_story = foo2(text_input,user_choice)
            st.markdown(continued_story)
#############################################################


=============================================================
DRAFT CODE 2:
{code_snippets}
#############################################################
FINAL CODE 2:

"""
