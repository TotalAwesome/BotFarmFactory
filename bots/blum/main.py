from client import BlumClient

client = BlumClient()

while True:
    client.daily_reward()
    client.friends_claim()
    client.update_balance()
    client.play_game()
    client.start_farming()
