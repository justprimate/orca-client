

import asyncio
import json
from decimal import Decimal
from pathlib import Path
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from solana.keypair import Keypair

# ported functions from whirlpools-sdk and common-sdk
from whirlpool_essentials import WhirlpoolContext, DecimalUtil, PriceMath, SwapUtil, PDAUtil, TokenUtil
from whirlpool_essentials.constants import ORCA_WHIRLPOOL_PROGRAM_ID
from whirlpool_essentials.instruction import WhirlpoolIx, SwapParams
from whirlpool_essentials.transaction import TransactionBuilder


RPC_ENDPOINT_URL = "https://api.mainnet-beta.solana.com/"
SAMO_USDC_WHIRLPOOL_PUBKEY = PublicKey("9vqYJjDUFecLL2xPUC4Rc7hyCtZ6iJ4mDiVZX7aFXoAe")

async def main():

    with Path("wallet.json").open() as f:
        keypair = Keypair.from_secret_key(bytes(json.load(f)))
        print("wallet pubkey", keypair.public_key)

    print(ORCA_WHIRLPOOL_PROGRAM_ID)

    connection = AsyncClient(RPC_ENDPOINT_URL)
    ctx = WhirlpoolContext(ORCA_WHIRLPOOL_PROGRAM_ID, connection, keypair)

    whirlpool_pubkey = SAMO_USDC_WHIRLPOOL_PUBKEY
    whirlpool = await ctx.fetcher.get_whirlpool(whirlpool_pubkey)
    token_a_decimal = (await ctx.fetcher.get_token_mint(whirlpool.token_mint_a)).decimals  # SAMO_DECIMAL
    token_b_decimal = (await ctx.fetcher.get_token_mint(whirlpool.token_mint_b)).decimals  # USDC_DECIMAL
    print("whirlpool token_mint_a", whirlpool.token_mint_a)
    print("whirlpool token_mint_b", whirlpool.token_mint_b)
    print("whirlpool tick_spacing", whirlpool.tick_spacing)
    print("whirlpool tick_current_index", whirlpool.tick_current_index)
    print("whirlpool sqrt_price", whirlpool.sqrt_price)
    price = PriceMath.sqrt_price_x64_to_price(whirlpool.sqrt_price, token_a_decimal, token_b_decimal)
    print("whirlpool price", DecimalUtil.to_fixed(price, token_b_decimal))


asyncio.run(main())
#copper drift alert inquiry earth admit infant glove author museum banana nest