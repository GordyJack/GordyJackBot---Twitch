from twitchio.ext import commands

import command_data_utils


class ModCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.event()
    async def event_ready(self):
        print(f"{__name__} registered with | {self.bot.user_id}")

    @commands.command(name='disable')
    async def disable_command(self, ctx: commands.Context, command_name: str):
        if not ctx.author.is_mod:
            return
        # Check if the command is not already disabled
        if command_name not in self.bot.disabled_commands:
            # Get the command instance and store it
            command = self.bot.get_command(command_name)
            if command is not None:
                # Add the command to the disabled commands list
                self.bot.disabled_commands[command_name] = command
                # Remove the command dynamically
                self.bot.remove_command(command_name)
                command_data_utils.save_command_property(command_name, "enabled", False)
                await ctx.send(f'Command "{command_name}" disabled.')
            else:
                await ctx.send(f'Command "{command_name}" does not exist.')
        else:
            await ctx.send(f'Command "{command_name}" is already disabled.')

    @commands.command(name='enable')
    async def enable_command(self, ctx: commands.Context, command_name: str):
        if not ctx.author.is_mod:
            return
        # Check if the command is disabled
        if command_name in self.bot.disabled_commands:
            # Get the command from the disabled commands list
            command = self.bot.disabled_commands.pop(command_name, None)
            # Add the command back dynamically
            if command is not None:
                self.bot.add_command(command)
                command_data_utils.save_command_property(command_name, "enabled", True)
                await ctx.send(f'Command "{command_name}" enabled.')
            else:
                await ctx.send(f'Command "{command_name}" does not exist.')
        else:
            await ctx.send(f'Command "{command_name}" is not disabled.')

    @commands.command()
    async def reload_cog(self, ctx: commands.Context, cog_name: str):
        if not ctx.author.is_mod:
            return
        self.bot.reload_module(f"cogs.{cog_name}")


def prepare(bot):
    bot.add_cog(ModCommandsCog(bot))
