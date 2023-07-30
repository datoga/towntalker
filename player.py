from elevenlabs import play

from _redis import pop

def get_and_process_message():
    print('Waiting messages...')
    [_, message] = pop()
    [_, audio] = pop()

    print(message)
    play(audio)

while True:
    get_and_process_message()