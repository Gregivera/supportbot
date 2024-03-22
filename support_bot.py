import discord
import openai
import os
import difflib  # Add this line to import the difflib module

# Intents are a way of telling Discord which events your bot needs to receive
intents = discord.Intents.default()
intents.messages = True
intents.guild_messages = True  # This line is necessary
intents.message_content = True  # This allows the bot to receive DMs.
openai.api_key = os.getenv('OPENAI_API')

client = discord.Client(intents=intents)

# Define a dictionary of FAQs where the key is the question and the value is the answer
faq_dict = {
    "how to trade": "You can start trading by signing up to Coindeck, make your first deposit and start your trading journey with an exciting deposit bonus.",
    "reset password": "To reset your password, go to the log in page > click > reset password.",
    "what is cryptocurrency": "Cryptocurrency is a type of digital or virtual currency that uses cryptography for security. It operates independently of a central bank and can be used for secure, online transactions.",
    "how to trade with leverage": "To trade with leverage, you'll need to navigate to the Coindeck Margin Trade Page, Choose the crypto pair you would like to trade, Enter Margin/Stake, Choose Leverage and tagerts and place your trade Successfully!",
    "what is blockchain": "Blockchain is a distributed ledger technology that underlies cryptocurrencies like Bitcoin. It securely records transactions across multiple computers in a way that prevents alterations, ensuring data integrity and trust.",
    "best crypto trading platform": "Coindeck.app stands out as the premier trading platform due to its user-friendly interface, robust security measures, and comprehensive support for a wide range of cryptocurrencies. Its innovative tools and analytics empower users to make informed decisions, while its low transaction fees enhance profitability, making it top choice for trading.",
    "how to store crypto safely": "Cryptocurrencies can be stored in a digital wallet intergrated to each user's Coindeck Trading Account",
    "what is bitcoin": "Bitcoin is the first and most well-known cryptocurrency, created in 2009 by an unknown person using the pseudonym Satoshi Nakamoto. It allows for peer-to-peer transactions without the need for intermediaries, using blockchain technology for security.",
    "difference between bitcoin and ethereum": "Bitcoin was created primarily as a digital currency. Ethereum, while also a cryptocurrency, features a platform for creating smart contracts and decentralized applications (dApps), offering more functionality beyond just transactions.",
    "what is crypto mining": "Crypto mining is the process by which transactions for various cryptocurrencies are verified and added to the blockchain digital ledger. It also refers to the process of creating new coins as a reward for miners.",
    "what are smart contracts": "Smart contracts are self-executing contracts with the terms of the agreement between buyer and seller being directly written into lines of code. They run on blockchain networks, enabling automated, secure, and trustless transactions.",
    "what is a crypto wallet": "A cryptocurrency wallet is a digital tool that securely stores your crypto assets. It acts like a bank account, holding your digital currencies and allowing you to send, receive, and manage your cryptocurrencies. Wallets can be hardware-based or software-based, with varying features for security and convenience.",
    "what is cryptocurrency trading?": "Cryptocurrency trading is the act of speculating on cryptocurrency price movements via a trading platform. It involves exchanging fiat money for digital assets or trading one cryptocurrency for another, aiming to profit from short-term price fluctuations or long-term trends within this decentralized digital currency space.",
    "how do i deposit?": "Navigate to your Coindeck Dashboard, on the sidebar you will see 'Deposit Funds', click on it and select your payment option. Enter ammount, your deposit bonus would depend on your deposit ammount. After entering the ammount you wish to deposit Click 'Proceed to Payment'. Send the desired to token to your displayed address by scanning the QR or copying the address. After sending crypto to your wallet, click on 'I Have Sent It'. Your deposit will then be confirmed shortly!",
    "how do i withdraw?": "Navigate to your Coindeck Dashboard, on the sidebar you will see 'Withdraw Funds', click on it and enter the ammount & token you wish to withdraw, Choose which of your wallet you wish to withdraw from & enter the wallet address you wish to withdraw to. Then click on 'Make withdrawal request'. Your withdrawl will then be processed and you will be notified shortly!",
    "what are trading pairs?": "Trading pairs are combinations of two different currencies that can be traded for each other on an exchange. For example, in the pair BTC/USD, Bitcoin can be traded for US Dollars. The first currency (BTC) is the 'base' and the second (USD) is the 'quote' currency.",
    "can I trade on my mobile phone or device?": "Absolutely! Coindeck offers a mobile-friendly platform that allows traders to execute transactions directly from their smartphones. Our app provides a seamless trading experience with full access to all trading features, ensuring you can manage your portfolio and trade on the go, anytime, anywhere, with just a few taps on your device.",
    "what tools and resources are available for beginners?": "Coindeck offers a range of features ideal for beginners, including margin trading with leverage, options trading, and engaging trading contests where you can compete with others and earn rewards. For newcomers not yet versed in market nuances, thier priority should be the auto trading feature, which can help navigate and execute profitable trades, easing a profitable learning curve while they familiarize themselves with market dynamics.",
    "how can I track my portfolio performance and profitability?": " At Coindeck, we offer an intuitive dashboard that enables traders to easily monitor their portfolio's performance and profitability. Our user-friendly interface provides real-time data and analytics, allowing you to make informed decisions and track your investment growth effectively.",
    "how do I set stop-loss?": " A stop-loss order is crucial for managing risk by automatically selling your assets if the price falls to a certain level, preventing potential heavy losses. To set one, determine the price at which you want to exit your position to minimize losses, then enter this price into the stop-loss field on the margin trading panel. Always consider the asset's volatility and your risk tolerance before setting the stop-loss level.",
    "how do I set take-profit?": " Setting a take-profit helps you lock in profits at your target price. To ensure potential losses don't exceed your comfort level, also set a stop-loss. On Coindeck margin trading panel, you can set these by entering your desired take profit levels before placing your trade. Always make sure to consider the asset's volatility before setting your levels.",
    "what is margin trading?": " Margin trading in cryptocurrency is a method that allows traders to open positions with leverage, amplifying both potential profits and losses. Coindeck supports margin trading, offering up to 100X leverage, which means you can enter larger trades with a smaller capital outlay. This can significantly increase your buying power, allowing for greater exposure to market movements and the opportunity to amplify returns. However, it's crucial to approach margin trading with caution due to the increased risk of higher leverage.",
    "what is options trading?": " Option trading is a financial strategy where traders buy the right, but not the obligation, to purchase or sell a cryptocurrency at a specified price within a set time frame. It offers the flexibility to hedge against market volatility, speculate on market movements for greater profit potential. Coindeck proudly supports option trading, allowing for profitability of up to 100%. Our platform provides robust tools and features to enhance your trading experience, giving you the opportunity to capitalize on the dynamic crypto market with the strategic advantage of options trading.",
    "can I trade 24/7 on the coindeck app?": " Coindeck supports round-the-clock trading, allowing you to trade 24 hours a day, seven days a week, in sync with the always-open cryptocurrency markets.",
    "what are trading limit?": "Trading limits are caps on the amount of currency you can trade to manage risk. For options, Coindeck's limit is $1000 per trade. Margin trading is leveraged, allowing larger trades; Coindeck offers up to 100x leverage, with a maximum trade size of $40 million. Always trade responsibly, considering the risks, especially with leveraged positions which can amplify both gains and losses.",
}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Don't let the bot respond to its own messages or respond in non-text channels
    if message.author == client.user or not isinstance(message.channel, (discord.TextChannel, discord.DMChannel)):
        return

    help_channel_id = '1208727091059630120'  # Help channel ID

    # Define a helper function to process the message
    async def process_message(msg_content, channel):
        message_content_lower = msg_content.lower()
        questions = list(faq_dict.keys())
        closest_matches = difflib.get_close_matches(message_content_lower, questions, n=1, cutoff=0.4)
        
        if closest_matches:
            question = closest_matches[0]
            await channel.send(faq_dict[question])
        else:
            await channel.send('I am not sure how to answer that. Can you please rephrase or check our FAQ section?')

    # Check if the message is in the help channel or a DM
    if message.channel.id == int(help_channel_id) or isinstance(message.channel, discord.DMChannel):
        if message.content.startswith(('Hello', 'Hi')):
            await message.channel.send('Hello! How can I assist you today?')
        else:
            # Process the message if it's in the help channel or a DM
            await process_message(message.content, message.channel)
    # If the message is not in the help channel or a DM, do not respond

# Replace 'YOUR_BOT_TOKEN' with your bot's token
client.run(os.getenv('SUPPORT_BOT_TOKEN'))
