import discord
import pickle

assignment_list = []

client = discord.Client()

async def kadaihelp(message):
    string = 'コマンドリスト\n'
    for command in COMMANDS:
        string += '------------------------\n'
        string += '{}: {}\n'.format('!' + command, COMMANDS[command]['description'])
        string += '    使い方: {}\n'.format(COMMANDS[command]['use'])
        string += '    省略形: {}\n'.format(COMMANDS[command]['alias'])
        string += '------------------------'

    await message.channel.send(string)

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

async def close(message):
    pickle.dump(assignment_list, open('assignments.pkl', 'wb'))

    await message.channel.send('Bye^^')

    await client.close()

TOKEN = 'NzEwMDg0MjMxMTM2ODA0OTM0.Xr0JIg.GSZGT8j3ThQKfNw_GCEKD3T2PAs'
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
    },
    'exit': {
        'description': 'Botを終了します。',
        'use': '!exit',
        'alias': '!ex',
        'func': close
    }
}

def load_assignments():
    global assignment_list

    assignment_list = pickle.load(open('assignments.pkl', 'rb'))

@client.event
async def on_ready():
    load_assignments()

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
