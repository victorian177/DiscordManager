import nextcord


class TextForm(nextcord.ui.Modal):
    def __init__(self, name, form_inputs, response) -> None:
        super().__init__(name, timeout=300)
        self.items = {}
        self.form_inputs = form_inputs
        self.response = response
        self.values = {}

        for f in self.form_inputs:
            self.items[f["label"]] = nextcord.ui.TextInput(
                label=f["label"],
                placeholder=f["placeholder"],
                style=nextcord.TextInputStyle.paragraph,
                required=False,
            )
            self.add_item(self.items[f["label"]])

    async def _callback(self, interaction: nextcord.Interaction):
        for f in self.form_inputs:
            self.values[f["label"]] = self.items[f["label"]].value

        await interaction.send(self.response)
