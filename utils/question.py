import discord


class QuestionPanel:
    def __init__(self, category,  value, question, answer):
        self.category = category
        value = value.replace(',', '')
        self.value = int(value.strip('$'))
        self.question = question
        self.answer = answer

    def get_answer(self):
        return self.answer

    def get_value(self):
        return self.value

# displays Question panel onto screen
    def get_embed(self):
        embed = discord.Embed(title=f'Category: {self.category}', description=self.question, inline=False)
        embed.add_field(name='Value', value="$"+str(self.value), inline=False)
        return embed
