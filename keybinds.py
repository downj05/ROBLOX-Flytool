import configparser

# Load config file
config = configparser.ConfigParser()
config.read('config.ini')

toggle_key = config.get('toggle', 'key', fallback='g')
reset_key = config.get('reset', 'key', fallback='r')
forward_key = config.get('forward', 'key', fallback='w')
left_key = config.get('left', 'key', fallback='a')
right_key = config.get('right', 'key', fallback='d')
back_key = config.get('back', 'key', fallback='s')
up_key = config.get('up', 'key', fallback='space')
down_key = config.get('down', 'key', fallback='shift')
exit_key = config.get('exit', 'key', fallback=';')
# Print variables
print(f'Toggle key: {toggle_key}')
print(f'Reset key: {reset_key}')
print(f'Forward key: {forward_key}')
print(f'Left key: {left_key}')
print(f'Right key: {right_key}')
print(f'Back key: {back_key}')
print(f'Up key: {up_key}')
print(f'Down key: {down_key}')
print(f'Exit key: {exit_key}')