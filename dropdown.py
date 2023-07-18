from asyncio import Event

import nextcord


class Dropdown(nextcord.ui.View):
    def __init__(self, dropdown_data):
        super().__init__()
        self.selected = []
        self.dropdowns = []
        self.event = Event()
        
        for k, v in dropdown_data.items():
            options = [nextcord.SelectOption(label=o) for o in v]
            dropdown = nextcord.ui.Select(placeholder=k, options=options)
            self.dropdowns.append(dropdown)
            self.add_item(dropdown)

    @nextcord.ui.button(label="Submit", style=nextcord.ButtonStyle.green)
    async def submit(self, button, interaction: nextcord.Interaction):
        self.event.set()
        for dd in self.dropdowns:
            self.selected.append(dd.values[0])

        await interaction.response.send_message(f"You selected: {self.selected}")

        # Clear the view so it is removed from the message
        self.clear_items()
