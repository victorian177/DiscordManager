import nextcord


class TextForm(nextcord.ui.Modal):
    def __init__(self, name, form_inputs) -> None:
        super().__init__(name, timeout=300)

        for f in form_inputs:
            item = nextcord.ui.TextInput(
                label=f["label"],
                placeholder=f["placeholder"],
                style=nextcord.TextInputStyle.paragraph,
                required=False,
            )
            self.add_item(item)
