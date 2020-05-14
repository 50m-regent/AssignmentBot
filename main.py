import discord

async def kadaihelp(message):
    string = ''
    for command in COMMANDS:
        string += '{}: {}\n'.format('!' + command, COMMANDS[command]['description'])
        string += '    使い方: {}\n'.format(COMMANDS[command]['use'])
        string += '    省略形: {}\n'.format(COMMANDS[command]['alias'])

    await message.channel.send('コマンドリスト\n' + string)

async def newkadai(message):
    msg = message.content.split(' ')
    try:
        title, deadline, memo = msg[1:]

        assignment_list.append({
            'title': title,
            'deadline': deadline,
            'memo': memo
        })

        await message.channel.send('課題を追加しました！')
    except:
        await message.channel.send('入力形式が間違っています。')

async def deletekadai(message):
    msg = message.content.split(' ')
    for i in range(len(assignment_list)):
        if assignment_list[i]['title'] == msg[1]:
            assignment_list.pop(i)
            await message.channel.send('課題を削除しました')

async def kadailist(message):
    string = '課題一覧\n'
    for i, assignment in enumerate(assignment_list):
        string += '------------------------\n'
        string += '{}. {}\n'.format(i + 1, assignment['title'])
        string += '締切: {}\n'.format(assignment['deadline'])
        string += '備考: {}\n'.format(assignment['memo'])
        string += '------------------------\n'
        
    string += '現在、{}個の課題が出されています。'.format(len(assignment_list))
    await message.channel.send(string)

TOKEN = 'NzEwMDg0MjMxMTM2ODA0OTM0.XrvUOw.X5sCgLGqX5_RvT6ADIqH7eWAF10'
COMMANDS = {
    'kadaihelp': {
        'description': 'このリストを表示します。',
        'use': '!kadaihelp',
        'alias': '!kh',
        'func': kadaihelp
    },
    'newkadai': {
        'description': '新しい課題を追加します。',
        'use': '!newkadai \{タイトル\} \{締切\} \{備考\}',
        'alias': '!nk',
        'func': newkadai
    },
    'deletekadai': {
        'description': '課題削除',
        'use': '!deletekadai \{課題名\}',
        'alias': '!dk',
        'func': deletekadai
    },
    'kadailist': {
        'description': '登録されている課題一覧を表示します。',
        'use': '!kadailist',
        'alias': '!kl',
        'func': kadailist
    }
}

client = discord.Client()

def load_assignments():
    return []

@client.event
async def on_ready():
    global assignment_list
    
    assignment_list = load_assignments()

    print('KadaiShosu起動')

@client.event
async def on_message(message):
    msg = message.content.split(' ')

    if message.author.bot:
        return

    for command in COMMANDS:
        if msg[0] in ['!' + command, COMMANDS[command]['alias']]:
            await COMMANDS[command]['func'](message)

client.run(TOKEN)