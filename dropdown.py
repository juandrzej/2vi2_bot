import discord
from discord.ui import View, Select

civ_list = [
    discord.SelectOption(label="Abraham-Lincoln", emoji="<:AmericaAbrahamLincoln:1078426690365182042>"),
    discord.SelectOption(label="Catherine-BQ"),
    discord.SelectOption(label="Catherine-Magnificence"),
    discord.SelectOption(label="Chandragupta"),
    discord.SelectOption(label="Cree"),
    discord.SelectOption(label="Egypt"),
    discord.SelectOption(label="Eleanor-En"),
    discord.SelectOption(label="Gaul"),
    discord.SelectOption(label="Gorgo"),
    discord.SelectOption(label="Gran-Colombia"),
    discord.SelectOption(label="Hojo-Tokimune"),
    discord.SelectOption(label="Indonesia"),
    discord.SelectOption(label="Khmer"),
    discord.SelectOption(label="Korea"),
    discord.SelectOption(label="Maya"),
    discord.SelectOption(label="Mbande"),
    discord.SelectOption(label="Nader-Shah"),
    discord.SelectOption(label="Nubia"),
    discord.SelectOption(label="Persia"),
    discord.SelectOption(label="Poland"),
    discord.SelectOption(label="EPtolemaic-Cleopatra"),

    discord.SelectOption(label="Zulu")
]


class ReportView(View):
    def __init__(self, report_info):
        super().__init__()
        self.author = report_info[0]
        self.players = report_info[1]
        self.report_civs = ["Empty", "Empty", "Empty", "Empty", "Empty"]
        self.report_info = [self.author, self.players, self.report_civs]

        self.add_item(CivSelect("1", "Choose civ picked by Team 1 Slot 1 player!", self.report_info))
        self.add_item(CivSelect("2", "Choose civ picked by Team 2 Slot 2 player!", self.report_info))
        self.add_item(CivSelect("3", "Choose civ picked by Team 2 Slot 3 player!", self.report_info))
        self.add_item(CivSelect("4", "Choose civ picked by Team 1 Slot 4 player!", self.report_info))

    @discord.ui.select(
        custom_id="0",
        placeholder="Choose two banned civilizations!",
        min_values=2,
        max_values=2,
        options=civ_list)
    async def on_select(self, interaction, select):
        await interaction.response.defer()

        self.report_civs[int(select.custom_id)] = select.values[0] + ", " + select.values[1]

        if "Empty" not in self.report_civs:
            await interaction.edit_original_response(
                content=f'GameType 2vi2'
                        f'\n Bans: {self.report_civs[0]}'
                        f'\n T1 slot 1: {self.report_civs[1]} {self.players[0].mention}'
                        f'\n T2 slot 2: {self.report_civs[2]} {self.players[1].mention}'
                        f'\n T2 slot 3: {self.report_civs[3]} {self.players[2].mention}'
                        f'\n T1 slot 4: {self.report_civs[4]} {self.players[3].mention}',
                view=Confirm(self.report_info))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author[0]


class CivSelect(Select):
    def __init__(self, custom_id, placeholder, report_info):
        super().__init__(
            custom_id=custom_id,
            placeholder=placeholder,
            options=civ_list
        )

        self.author = report_info[0]
        self.players = report_info[1]
        self.report_civs = report_info[2]
        self.report_info = report_info

    async def callback(self, interaction):
        await interaction.response.defer()
        self.report_civs[int(self.custom_id)] = self.values[0]

        if "Empty" not in self.report_civs:
            await interaction.edit_original_response(
                content=f'GameType 2vi2'
                        f'\n Bans: {self.report_civs[0]}'
                        f'\n T1 slot 1: {self.report_civs[1]} {self.players[0].mention}'
                        f'\n T2 slot 2: {self.report_civs[2]} {self.players[1].mention}'
                        f'\n T2 slot 3: {self.report_civs[3]} {self.players[2].mention}'
                        f'\n T1 slot 4: {self.report_civs[4]} {self.players[3].mention}',
                view=Confirm(self.report_info))


class PlayerDDView(View):
    def __init__(self, report_info):
        super().__init__()
        self.author = report_info[0]
        self.players = report_info[1]
        self.report_civs = report_info[2]
        self.choices = ["Empty", "Empty"]
        self.report_info = [self.author, self.players, self.report_civs, self.choices]
        self.add_item(PlayerDD(self.report_info))

    @discord.ui.select(
        placeholder="Choose winner!",
        options=[
            discord.SelectOption(label="Team 1"),
            discord.SelectOption(label="Team 2")
        ])
    async def on_select(self, interaction, select):
        await interaction.response.defer()

        self.choices[0] = select.values[0]

        if "Empty" not in self.choices:
            await interaction.edit_original_response(
                content=f'GameType 2vi2'
                        f'\n Winning team: {self.choices[0]}'
                        f'\n Host: {self.choices[1].mention}'
                        f'\n Bans: {self.report_civs[0]}'
                        f'\n T1 slot 1: {self.report_civs[1]} {self.players[0].mention}'
                        f'\n T2 slot 2: {self.report_civs[2]} {self.players[1].mention}'
                        f'\n T2 slot 3: {self.report_civs[3]} {self.players[2].mention}'
                        f'\n T1 slot 4: {self.report_civs[4]} {self.players[3].mention}',
                view=SecondConfirm(self.report_info))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author[0]


class PlayerDD(Select):
    def __init__(self, report_info):
        super().__init__(
            placeholder="Choose a host!",
            options=[
                discord.SelectOption(label=str(report_info[1][0]), value="0"),
                discord.SelectOption(label=str(report_info[1][1]), value="1"),
                discord.SelectOption(label=str(report_info[1][2]), value="2"),
                discord.SelectOption(label=str(report_info[1][3]), value="3")
            ])
        self.author = report_info[0]
        self.players = report_info[1]
        self.report_civs = report_info[2]
        self.choices = report_info[3]
        self.report_info = report_info

    async def callback(self, interaction):
        await interaction.response.defer()

        self.choices[1] = self.players[int(self.values[0])]

        if "Empty" not in self.choices:
            await interaction.edit_original_response(
                content=f'GameType 2vi2'
                        f'\n Winning team: {self.choices[0]}'
                        f'\n Host: {self.choices[1].mention}'
                        f'\n Bans: {self.report_civs[0]}'
                        f'\n T1 slot 1: {self.report_civs[1]} {self.players[0].mention}'
                        f'\n T2 slot 2: {self.report_civs[2]} {self.players[1].mention}'
                        f'\n T2 slot 3: {self.report_civs[3]} {self.players[2].mention}'
                        f'\n T1 slot 4: {self.report_civs[4]} {self.players[3].mention}',
                view=SecondConfirm(self.report_info))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.author[0]


class Confirm(View):
    def __init__(self, report_info):
        super().__init__()
        self.report_info = report_info
        self.author = report_info[0]
        self.players = report_info[1]
        self.report_civs = report_info[2]

    @discord.ui.button(label="Proceed", style=discord.ButtonStyle.green)
    async def button_green_callback(self, interaction, button):
        await interaction.response.edit_message(
            content=f'GameType 2vi2'
                    f'\n Bans: {self.report_civs[0]}'
                    f'\n T1 slot 1: {self.report_civs[1]} {self.players[0].mention}'
                    f'\n T2 slot 2: {self.report_civs[2]} {self.players[1].mention}'
                    f'\n T2 slot 3: {self.report_civs[3]} {self.players[2].mention}'
                    f'\n T1 slot 4: {self.report_civs[4]} {self.players[3].mention}',
            view=PlayerDDView(self.report_info))

    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.red)
    async def button_red_callback(self, interaction, button):
        await interaction.response.edit_message(
            content=f'GameType 2vi2'
                    f'\n Bans: {self.report_civs[0]}'
                    f'\n T1 slot 1: {self.report_civs[1]} {self.players[0].mention}'
                    f'\n T2 slot 2: {self.report_civs[2]} {self.players[1].mention}'
                    f'\n T2 slot 3: {self.report_civs[3]} {self.players[2].mention}'
                    f'\n T1 slot 4: {self.report_civs[4]} {self.players[3].mention}',
            view=ReportView(self.report_info))


class SecondConfirm(View):
    def __init__(self, report_info):
        super().__init__()
        self.report_info = report_info
        self.author = report_info[0]
        self.players = report_info[1]
        self.report_civs = report_info[2]
        self.choices = report_info[3]

    @discord.ui.button(label="Proceed", style=discord.ButtonStyle.green)
    async def button_green_callback(self, interaction, button):
        await interaction.response.edit_message(
                content=f'GameType 2vi2'
                        f'\n Winning team: {self.choices[0]}'
                        f'\n Host: {self.choices[1].mention}'
                        f'\n Bans: {self.report_civs[0]}'
                        f'\n T1 slot 1: {self.report_civs[1]} {self.players[0].mention}'
                        f'\n T2 slot 2: {self.report_civs[2]} {self.players[1].mention}'
                        f'\n T2 slot 3: {self.report_civs[3]} {self.players[2].mention}'
                        f'\n T1 slot 4: {self.report_civs[4]} {self.players[3].mention}',
                view=None)

        message = await interaction.followup.send(
                    content=f"\n Players pending confirmation: {','.join([x.mention for x in self.players])}",
                    view=View()
                )

        await message.add_reaction('👍')

        players = [player for player in self.players if player.id != 1077667810009960469]
        for user in players:
            channel = await user.create_dm()
            await channel.send(f"Hey {user.mention}, "
                               f"please react with 👍 to the linked report to confirm its validity."
                               f"\nLink to the report: {message.jump_url}")

    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.red)
    async def button_red_callback(self, interaction, button):
        await interaction.response.edit_message(
            content=f'GameType 2vi2'
                    f'\n Winning team: {self.choices[0]}'
                    f'\n Host: {self.choices[1].mention}'
                    f'\n Bans: {self.report_civs[0]}'
                    f'\n T1 slot 1: {self.report_civs[1]} {self.players[0].mention}'
                    f'\n T2 slot 2: {self.report_civs[2]} {self.players[1].mention}'
                    f'\n T2 slot 3: {self.report_civs[3]} {self.players[2].mention}'
                    f'\n T1 slot 4: {self.report_civs[4]} {self.players[3].mention}',
            view=PlayerDDView(self.report_info))
