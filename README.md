# MenoBot
MenoBot is a Telegram bot designed to daily check price fluctuations of YuGiOh cards on CardMarket.

## Command List
Available commands:
 * **help** - Show a list of available commands
 * **list_most_wanted_cards** - Show most wanted cards on CardMarket
 * **list_my_cards** - Show the cards you are following
 * **add_card** card - Start following a card
 * **remove_card** card_number - Stop following a card
 * **search** card - Looks for a card on CardMarket
 * **update_price** card_number - Forces price update of a card
 * **update_prices** - Forces price update of all cards
 * **set_timeout** timeout - Changes time to wait between price updates

### Requirements
MenoBot requires Python library `python-telegram-bot`. You can obtain this library by running:
```
python -m pip install python-telegram-bot
```
