# generate docs for dbt models from manifest.json with jinja

from ast import main
from jinja2 import Environment, BaseLoader
import json
import os
manifest = json.load(open('./manifest.json', 'r'))

ROOT_DIR = "docs/dbt"

# sources

src_template = '''---
title: {{ name }}
---

# {{ schema }}.**{{ name }}**

{{ description }}

[Model](https://github.com/duneanalytics/abstractions/blob/master/spellbook/{{ path }})

## Columns

| Column | Description |
| -- | -- |
{% for c in columns.values() %}| {{ c.name }} | {{ c.description }} |
{% endfor %}
'''

rsrc_template = Environment(loader=BaseLoader()).from_string(src_template)

SRC_DIR = f"{ROOT_DIR}/sources"
sources = manifest['sources']

os.makedirs(SRC_DIR, exist_ok=True)

for schema in set(src['schema'] for src in sources.values()):
    dirname = f"{SRC_DIR}/{schema}"
    filename = f"{dirname}/.pages"

    os.makedirs(dirname, exist_ok=True)
    with open(filename, "w") as f:
        f.write(f'title: {schema}')

for src in sources.values():

    filename = f"{SRC_DIR}/{src['schema']}/{src['name']}.md"
    with open(filename, "w") as f:
        f.write(rsrc_template.render(**src))

# models

model_template = '''---
title: {{ name }}
---

# {{ config.schema }}.**{{ config.alias }}**

{{ description }}

[Model](https://github.com/duneanalytics/abstractions/blob/master/spellbook/{{ path }})

{% for user in contrib %}
![{{ user }}](https://github.com/{{ user }}.png)
{% endfor %}

## Columns

| Column | Description |
| -- | -- |
{% for c in columns.values() %}| {{ c.name }} | {{ c.description }} |
{% endfor %}
'''

rmodel_template = Environment(loader=BaseLoader()).from_string(model_template)

MODEL_DIR = f"{ROOT_DIR}/models"
models = manifest['nodes']

os.makedirs(MODEL_DIR, exist_ok=True)

for schema in set(mdl['config']['schema'] for mdl in models.values()):
    dirname = f"{MODEL_DIR}/{schema}"
    filename = f"{dirname}/.pages"

    os.makedirs(dirname, exist_ok=True)
    with open(filename, "w") as f:
        f.write(f'title: {schema}')

for mdl in models.values():

    config = mdl['config']

    filename = f"{MODEL_DIR}/{config['schema']}/{config['alias']}.md"
    with open(filename, "w") as f:
        contrib = config['meta'].get('contributors', [])
        contrib = contrib.split(', ') if isinstance(contrib, str) else contrib
        f.write(rmodel_template.render(**mdl, contrib=contrib))

# source example: 'source.spellbook.ethereum.transactions'

# {'fqn': ['spellbook', 'base_sources', 'ethereum', 'transactions'],
#  'database': None,
#  'schema': 'ethereum',
#  'unique_id': 'source.spellbook.ethereum.transactions',
#  'package_name': 'spellbook',
#  'root_path': '/Users/davidkell/dev/abstractions/spellbook',
#  'path': 'models/base_sources/ethereum_base_sources.yml',
#  'original_file_path': 'models/base_sources/ethereum_base_sources.yml',
#  'name': 'transactions',
#  'source_name': 'ethereum',
#  'source_description': 'Ethereum raw tables including transactions, traces and logs.',
#  'loader': '',
#  'identifier': 'transactions',
#  'resource_type': 'source',
#  'quoting': {'database': None,
#   'schema': None,
#   'identifier': None,
#   'column': None},
#  'loaded_at_field': 'block_time',
#  'freshness': {'warn_after': {'count': 12, 'period': 'hour'},
#   'error_after': {'count': 24, 'period': 'hour'},
#   'filter': None},
#  'external': None,
#  'description': 'An Ethereum transaction refers to an action initiated by an externally-owned account (i.e., an account managed by a human, not a contract).',
#  'columns': {'block_date': {'name': 'block_date',
#    'description': 'Block event date in UTC',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'block_time': {'name': 'block_time',
#    'description': 'Timestamp for block event time in UTC',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'value': {'name': 'value',
#    'description': 'Amount of ETH transfered from sender to recipient',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'block_number': {'name': 'block_number',
#    'description': 'Block number',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'gas_limit': {'name': 'gas_limit',
#    'description': 'Maximum amount of gas units that can be consumed by the transaction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'gas_price': {'name': 'gas_price',
#    'description': 'Gas price denoted in gwei, which itself is a denomination of ETH - each gwei is equal to 10-9 ETH',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'gas_used': {'name': 'gas_used',
#    'description': 'Number of gas units consumed by the transaction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'max_fee_per_gas': {'name': 'max_fee_per_gas',
#    'description': 'Maximum amount of gas willing to be paid for the transaction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'max_priority_fee_per_gas': {'name': 'max_priority_fee_per_gas',
#    'description': 'Maximum amount of gas to be included as a tip to the miner',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'base_fee_per_gas': {'name': 'base_fee_per_gas',
#    'description': 'Market price for gas',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'nonce': {'name': 'nonce',
#    'description': 'Number of confirmed transactions previously sent by this account',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'index': {'name': 'index',
#    'description': 'Transaction index',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'success': {'name': 'success',
#    'description': 'Whether the transaction was completed sucessfully',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'from': {'name': 'from',
#    'description': 'Wallet address that initiated the transaction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'to': {'name': 'to',
#    'description': 'Wallet address that received the transaction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'block_hash': {'name': 'block_hash',
#    'description': 'Primary key of the block',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'data': {'name': 'data',
#    'description': 'Any binary data payload',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'hash': {'name': 'hash',
#    'description': 'Primary key of the transaction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'type': {'name': 'type',
#    'description': 'Transaction type',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'access_list': {'name': 'access_list',
#    'description': 'Specifies a list of addresses and storage keys',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []}},
#  'meta': {},
#  'source_meta': {},
#  'tags': [],
#  'config': {'enabled': True},
#  'patch_path': None,
#  'unrendered_config': {},
#  'relation_name': 'ethereum.transactions',
#  'created_at': 1661198884.865589}

# model example: model.spellbook.nft_trades

# {'raw_sql': "{{ config(\n        alias ='trades'\n        )\n}}\n\nSELECT *\nFROM\n(\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM {{ ref('opensea_trades') }} \n        UNION\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM {{ ref('magiceden_trades') }}\n        UNION\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM {{ ref('looksrare_ethereum_trades') }}\n        UNION\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM {{ ref('x2y2_ethereum_trades') }}\n        UNION\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM {{ ref('sudoswap_ethereum_trades') }}\n)",
#  'compiled': True,
#  'resource_type': 'model',
#  'depends_on': {'macros': [],
#   'nodes': ['model.spellbook.opensea_trades',
#    'model.spellbook.magiceden_trades',
#    'model.spellbook.looksrare_ethereum_trades',
#    'model.spellbook.x2y2_ethereum_trades',
#    'model.spellbook.sudoswap_ethereum_trades']},
#  'config': {'enabled': True,
#   'alias': 'trades',
#   'schema': 'nft',
#   'database': None,
#   'tags': ['nft',
#    'opensea',
#    'looksrare',
#    'x2y2',
#    'magiceden',
#    'sudoswap',
#    'ethereum',
#    'solana',
#    'trades'],
#   'meta': {'blockchain': 'ethereum, solana',
#    'sector': 'nft',
#    'contributors': 'soispoke, hildobby, ilemi'},
#   'materialized': 'view',
#   'persist_docs': {},
#   'quoting': {},
#   'column_types': {},
#   'full_refresh': None,
#   'unique_key': None,
#   'on_schema_change': 'ignore',
#   'grants': {},
#   'post-hook': [],
#   'pre-hook': []},
#  'database': None,
#  'schema': '._nft',
#  'fqn': ['spellbook', 'nft', 'nft_trades'],
#  'unique_id': 'model.spellbook.nft_trades',
#  'package_name': 'spellbook',
#  'root_path': '/Users/davidkell/dev/abstractions/spellbook',
#  'path': 'nft/nft_trades.sql',
#  'original_file_path': 'models/nft/nft_trades.sql',
#  'name': 'nft_trades',
#  'alias': 'trades',
#  'checksum': {'name': 'sha256',
#   'checksum': '31d98d59c2fce97f4def9e945bb55fdc10b6fd3a2d145005db2616778cd558e9'},
#  'tags': ['nft',
#   'opensea',
#   'looksrare',
#   'x2y2',
#   'magiceden',
#   'sudoswap',
#   'ethereum',
#   'solana',
#   'trades'],
#  'refs': [['opensea_trades'],
#   ['magiceden_trades'],
#   ['looksrare_ethereum_trades'],
#   ['x2y2_ethereum_trades'],
#   ['sudoswap_ethereum_trades']],
#  'sources': [],
#  'metrics': [],
#  'description': 'NFT trades\n',
#  'columns': {'blockchain': {'name': 'blockchain',
#    'description': 'Blockchain',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'project': {'name': 'project',
#    'description': 'Project',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'version': {'name': 'version',
#    'description': 'Project version',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'block_time': {'name': 'block_time',
#    'description': 'UTC event block time',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'token_id': {'name': 'token_id',
#    'description': 'NFT Token ID',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'collection': {'name': 'collection',
#    'description': 'NFT collection name',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'amount_usd': {'name': 'amount_usd',
#    'description': 'USD value of the trade at time of execution',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'token_standard': {'name': 'token_standard',
#    'description': 'Token standard',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'trade_type': {'name': 'trade_type',
#    'description': 'Identify whether it was a single NFT trade or multiple NFTs traded',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'number_of_items': {'name': 'number_of_items',
#    'description': 'Number of items traded',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'trade_category': {'name': 'trade_category',
#    'description': 'How was this NFT traded ? (Direct buy, auction, etc...)',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'evt_type': {'name': 'evt_type',
#    'description': 'Event type (Trade, Mint, Burn)',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'seller': {'name': 'seller',
#    'description': 'Seller wallet address',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'buyer': {'name': 'buyer',
#    'description': 'Buyer wallet address',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'amount_original': {'name': 'amount_original',
#    'description': 'Traded amount in original currency',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'amount_raw': {'name': 'amount_raw',
#    'description': 'Traded amount in original currency before decimals correction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'currency_symbol': {'name': 'currency_symbol',
#    'description': 'Symbol of original currency used for payment',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'currency_contract': {'name': 'currency_contract',
#    'description': 'Contract address of original token used for payment, with ETH contract address swapped for WETH',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'nft_contract_address': {'name': 'nft_contract_address',
#    'description': 'NFT contract address, only if 1 nft was transacted',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'project_contract_address': {'name': 'project_contract_address',
#    'description': 'Contract address used by the project, in this case wyvern contract',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'aggregator_name': {'name': 'aggregator_name',
#    'description': 'If the trade was performed via an aggregator, displays aggregator name',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'aggregator_address': {'name': 'aggregator_address',
#    'description': 'If the trade was performed via an aggregator, displays aggregator address',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'tx_hash': {'name': 'tx_hash',
#    'description': 'Transaction hash',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'block_number': {'name': 'block_number',
#    'description': 'Block number in which the transaction was executed ',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'tx_from': {'name': 'tx_from',
#    'description': 'Address that initiated the transaction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'tx_to': {'name': 'tx_to',
#    'description': 'Address that received the transaction',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []},
#   'unique_trade_id': {'name': 'unique_trade_id',
#    'description': 'Unique trade ID',
#    'meta': {},
#    'data_type': None,
#    'quote': None,
#    'tags': []}},
#  'meta': {'blockchain': 'ethereum, solana',
#   'sector': 'nft',
#   'contributors': 'soispoke, hildobby, ilemi'},
#  'docs': {'show': True},
#  'patch_path': 'spellbook://models/nft/nft_schema.yml',
#  'compiled_path': 'target/compiled/spellbook/models/nft/nft_trades.sql',
#  'build_path': None,
#  'deferred': False,
#  'unrendered_config': {'schema': 'nft',
#   'materialized': 'view',
#   'alias': 'trades'},
#  'created_at': 1661198884.630767,
#  'compiled_sql': '\n\nSELECT *\nFROM\n(\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM ._opensea.trades \n        UNION\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM ._magiceden.trades\n        UNION\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM ._looksrare_ethereum.trades\n        UNION\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM ._x2y2_ethereum.trades\n        UNION\n        SELECT\n                blockchain,\n                project,\n                version,\n                block_time,\n                token_id,\n                collection,\n                amount_usd,\n                token_standard,\n                trade_type,\n                number_of_items,\n                trade_category,\n                evt_type,\n                seller,\n                buyer,\n                amount_original,\n                amount_raw,\n                currency_symbol,\n                currency_contract,\n                nft_contract_address,\n                project_contract_address,\n                aggregator_name,\n                aggregator_address,\n                tx_hash,\n                block_number,\n                tx_from,\n                tx_to,\n                unique_trade_id\n        FROM ._sudoswap_ethereum.trades\n)',
#  'extra_ctes_injected': True,
#  'extra_ctes': [],
#  'relation_name': '._nft.trades'}