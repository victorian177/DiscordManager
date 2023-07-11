import nextcord

# link to example form: https://github.com/nextcord/nextcord/blob/master/examples/modals/modal.py

"""
Here are the list of the form input classes that would be useful:- 
TextInput(text input)
Select(options)
XXXXSelect(other types of options) 

Classes can be accessed through nextcord.ui.
"""

# TODO: An object that can specifies what the contents of the form should be (think schema for databases). Could be a dict.
# The Form's output is to be used to either create or update a record of a Database.
# TODO: An object that handles the response. From example, response is in the callback class.


class Form(nextcord.ui.Modal):
    ...
