import discord
from discord.ext import commands

embeds = [discord.Embed(title="First embed"),
          discord.Embed(title="Second embed"),
          discord.Embed(title="Third embed")]

class Simple(discord.ui.View):

    def __init__(self, *,
                 timeout: int = 60,
                 PreviousButton: discord.ui.Button = discord.ui.Button(emoji="<:AsylumBackPage:902651756377440278>", style=discord.ButtonStyle.grey),
                 NextButton: discord.ui.Button = discord.ui.Button(emoji="<:AsylumNextPage:902644474528813096>", style=discord.ButtonStyle.grey),
                 PageCounterStyle: discord.ButtonStyle = discord.ButtonStyle.grey,
                 InitialPage: int = 0) -> None:
        self.PreviousButton = PreviousButton
        self.NextButton = NextButton
        self.PageCounterStyle = PageCounterStyle
        self.InitialPage = InitialPage

        self.pages = None
        self.ctx = None
        self.message = None
        self.current_page = None
        self.page_counter = None
        self.total_page_count = None
        super().__init__(timeout=timeout)

    async def start(self, ctx: commands.Context, pages: list[discord.Embed]):
        self.pages = pages
        self.total_page_count = len(pages)
        self.ctx = ctx
        self.current_page = self.InitialPage
        self.PreviousButton.callback = self.previous_button_callback
        self.NextButton.callback = self.next_button_callback
        self.add_item(self.PreviousButton)
        self.add_item(self.NextButton)
        self.message = await ctx.send(embed=self.pages[self.InitialPage], view=self)

    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1
        self.page_counter = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1
        self.page_counter = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)
          
    async def next_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description="You're unable to use this interaction, make sure you run the command yourself!", color=0x747F8D)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.next()

    async def previous_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            embed = discord.Embed(description="You're unable to use this interaction, make sure you run the command yourself!", color=0x747F8D)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.previous()

class SimplePaginatorPageCounter(discord.ui.Button):
    def __init__(self, style: discord.ButtonStyle, TotalPages, InitialPage):
        super().__init__(emoji=f"{InitialPage + 1}/{TotalPages}", style=style, disabled=True)