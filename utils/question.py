import discord


class QuestionPanel:
    def __init__(self, category,  value, question, answer):
        self.category = category
        self.value = value
        self.question = question
        self.answer = answer

    def get_answer(self):
        return self.answer

# displays Question panel onto screen
    def get_embed(self):
        embed = discord.Embed(title=f'Category: {self.category}', description=self.question, inline=False)
        embed.add_field(name='Value', value=self.value, inline=False)
        return embed
