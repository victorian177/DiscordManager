from asyncio import Event

import nextcord


class Dropdown(nextcord.ui.View):
    def __init__(self, placeholder, options_list, event=Event()):
        super().__init__()
        self.selected = None
        self.event = event
        options = [nextcord.SelectOption(label=o) for o in options_list]
        self.dropdown = nextcord.ui.Select(placeholder=placeholder, options=options)
        self.add_item(self.dropdown)

    @nextcord.ui.button(label="Submit", style=nextcord.ButtonStyle.green)
    async def submit(self, button, interaction: nextcord.Interaction):
        self.event.set()
        self.selected = self.dropdown.values[0]

        await interaction.response.send_message(f"You selected: {self.selected}")

        # Clear the view so it is removed from the message
        self.clear_items()
