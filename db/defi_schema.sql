CREATE TABLE defi_historical_assets
(
    id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    owner_address VARCHAR(42),
    chain         VARCHAR(20),
    symbol        VARCHAR(20),
    usd_value     FLOAT,
    amount        FLOAT,
    price         FLOAT,
    asset_type    VARCHAR(20),
    is_debt       BOOLEAN,
    project       VARCHAR(50),
    recorded_at   timestamptz NOT NULL,
    constraint defi_historical_assets_uk
        unique (recorded_at, project, owner_address, chain, symbol)
);