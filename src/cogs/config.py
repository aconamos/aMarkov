#
# Manages per-server configuration files
#


from discord import Permissions, SlashCommandGroup, Option
from discord.ext.commands import Cog
from discord.commands.context import ApplicationContext

from bot import aMarkovBot
from sql import schema


class Config(Cog):
    def __init__(self, bot: aMarkovBot):
        self.bot = bot

    admin_perms = Permissions.none()
    admin_perms.administrator = True

    config = SlashCommandGroup("config", "Commands for configuration", guild_only=True)

    config_query = config.create_subgroup("query", "Commands to read the configuration")

    config_toggle = config.create_subgroup(
        "toggle",
        "Commands to toggle on/off configuration parameters",
        default_member_permissions=admin_perms,
    )

    config_set = config.create_subgroup(
        "set",
        "Commands to set configuration parameters",
        default_member_permissions=admin_perms,
    )

    @config_query.before_invoke
    @config_set.before_invoke
    @config_toggle.before_invoke
    async def check_server_in_db(self, ctx: ApplicationContext):
        if not schema.server_present(ctx.guild_id, self.bot.conn):
            schema.init_server(ctx.guild_id, self.bot.conn)
            await ctx.send("Default server config initialized", reference=ctx.message)

    @config.command()
    async def init(
        self,
        ctx: ApplicationContext,
    ):
        if not schema.server_present(ctx.guild_id, self.bot.conn):
            schema.write_schema(self.bot.conn)
            await ctx.interaction.respond("Bot configuration is now initialized!", ephemeral=True)
        else:
            await ctx.interaction.respond("Bot has already been initialized!", ephemeral=True)

    @config.command(name="query_all")
    async def _query_all(
        self,
        ctx: ApplicationContext,
    ):
        config = schema.fetch_config(ctx.guild_id, self.bot.conn)

        if config is None:
            await ctx.respond("Bot hasn't been initialized in this server yet! Use /config init to start it")
        else:
            id, probability, enabled, mentions, equal_chance = config
            await ctx.respond(f"""## The bot is currently {"enabled" if enabled else "disabled"}.
                              Probability: {probability}%
                              Mentions are: {"escaped" if mentions else "left in"}
                              ### Markov Chain Parameters:equal_chance: {equal_chance}""")

    @config_query.command(name="probability")
    async def _query_probability(
        self,
        ctx: ApplicationContext,
    ):
        prob = schema.query_probability(ctx.guild_id, self.bot.conn)
        await ctx.interaction.respond(f"Probability is currently {prob}%.", ephemeral=True)

    @config_set.command(name="probability")
    async def _set_probability(
        self,
        ctx: ApplicationContext,
        probability: Option(float),  # type: ignore
    ):
        if probability <= 0:
            await ctx.interaction.respond("Probability must be above 0%!", ephemeral=True)
            return

        if probability > 100:
            await ctx.interaction.respond("Probability can't be above 100%!", ephemeral=True)
            return

        schema.set_probability(ctx.guild_id, probability, self.bot.conn)
        await ctx.interaction.respond(f"Probability set to {probability}%", ephemeral=True)

    @config_query.command(name="mentions")
    async def _query_mentions(
        self,
        ctx: ApplicationContext,
    ):
        on = schema.query_mentions(ctx.guild_id, self.bot.conn)
        await ctx.interaction.respond(f"Mentions are currently {'enabled' if on else 'disabled'}.", ephemeral=True)

    @config_toggle.command(name="mentions")
    async def _toggle_mentions(
        self,
        ctx: ApplicationContext,
    ):
        on = schema.toggle_mentions(ctx.guild_id, self.bot.conn)
        await ctx.interaction.respond(f"Bot is now {'enabled' if on else 'disabled'}.", ephemeral=True)

    @config_query.command(name="equal_chance")
    async def _query_equal_chance(
        self,
        ctx: ApplicationContext,
    ):
        on = schema.query_equal_chance(ctx.guild_id, self.bot.conn)
        await ctx.interaction.respond(f"Chance is currently {'equal' if on else 'inequal'}.", ephemeral=True)

    @config_toggle.command(name="equal_chance")
    async def _toggle_equal_chance(
        self,
        ctx: ApplicationContext,
    ):
        on = schema.toggle_equal_chance(ctx.guild_id, self.bot.conn)
        await ctx.interaction.respond(f"Chance is now {'equal' if on else 'inequal'}.", ephemeral=True)

    @config_query.command(name="enabled")
    async def _toggle_query(self, ctx: ApplicationContext):
        on = schema.query_enabled(ctx.guild_id, self.bot.conn)
        await ctx.interaction.respond(f"Bot is currently {'enabled' if on else 'disabled'}.", ephemeral=True)

    @config_toggle.command(name="enabled")
    async def _toggle_set(self, ctx: ApplicationContext):
        on = schema.toggle_enabled(ctx.guild_id, self.bot.conn)
        await ctx.interaction.respond(f"Bot is now {'enabled' if on else 'disabled'}.", ephemeral=True)


def setup(bot: aMarkovBot):
    bot.add_cog(Config(bot))
