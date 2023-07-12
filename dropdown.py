import nextcord


class Dropdown(nextcord.ui.View):
    def __init__(self, placeholder, options_list) -> None:
        super().__init__()
        options = [nextcord.SelectOption(label=o) for o in options_list]
        self.add_item(nextcord.ui.Select(placeholder=placeholder, options=options))
