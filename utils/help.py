import discord
from discord.ext import commands

client = discord.Client()
class AsylumHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s %s' % (command.qualified_name, command.signature)




    async def send_bot_help(self, mapping):
        ctx = self.context
        self.client = client

        embed = discord.Embed(
            color=0xffffff,
            title="help",
            description=f"```diff\n- [] = optional argument\n+ <> = required argument```\nfor regular commands use `help <help>`\nfor subcommands use `help <cmd> <subcmd>`\nan asterisk(*) means the command has subcommands"
        )
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            commands = [f"`{c.name}`" if not hasattr(c, 'walk_commands') else f"`{c.name}`\*" for c in filtered]
            if commands:
                cogname = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cogname, value=', '.join(commands), inline=False)
        dest = self.get_destination()
        await dest.send(embed=embed)

    async def send_command_help(self, command):
        ctx = self.context
        bot = ctx.bot

        embed = discord.Embed(
            color=0xffffff,
            title=f"{command.qualified_name}",
            description=command.help or "This command has no description"
        ) \
            .add_field(name="usage", value=self.get_command_signature(command))
        alias = command.aliases
        if alias:
            embed.add_field(name="aliases", value=", ".join(alias), inline=False)
        await ctx.send(embed=embed)

    async def send_group_help(self, group):
        ctx = self.context
        bot = ctx.bot

        embed = discord.Embed(
            color=0xffffff,
            title=f"{group.qualified_name}",
            description=group.help or "This group has no description"
        ) \
            .add_field(name="usage", value=self.get_command_signature(group))
        alias = group.aliases
        subs = group.walk_commands()
        sub = list(f"{group.qualified_name} {sub.name} - {sub.help}" for sub in subs)
        if sub:
            embed.add_field(name="subcommands", value="\n".join(sub), inline=False)
        if alias:
            embed.add_field(name="aliases", value=", ".join(alias), inline=False)
        await ctx.send(embed=embed)
    async def send_cog_help(self, cog):
        pass