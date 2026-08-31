CREATE TABLE IF NOT EXISTS accounts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    username_key VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    password_salt VARBINARY(16) NOT NULL,
    password_hash VARBINARY(32) NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    last_login_at DATETIME(6) NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_accounts_username_key (username_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS characters (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    account_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(32) NOT NULL,
    name_key VARCHAR(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
    models_wire VARBINARY(60) NOT NULL,
    player_kit_wire VARBINARY(72) NOT NULL,
    charstats_wire VARBINARY(24) NOT NULL,
    is_tutorial_passed TINYINT UNSIGNED NOT NULL DEFAULT 0,
    gold_credit INT NOT NULL DEFAULT 0,
    renames_available INT NOT NULL DEFAULT 0,
    rename_required BOOLEAN NOT NULL DEFAULT FALSE,
    deletion_deadline DATETIME(6) NULL,
    last_space VARCHAR(128) NOT NULL DEFAULT 'spaces/so_origins',
    position_x DOUBLE NOT NULL DEFAULT 37.6137123,
    position_y DOUBLE NOT NULL DEFAULT 6.853166,
    position_z DOUBLE NOT NULL DEFAULT 66.95302,
    direction_x DOUBLE NOT NULL DEFAULT 0,
    direction_y DOUBLE NOT NULL DEFAULT 0,
    direction_z DOUBLE NOT NULL DEFAULT 0,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6),
    PRIMARY KEY (id),
    UNIQUE KEY uq_characters_name_key (name_key),
    KEY ix_characters_account_id (account_id),
    CONSTRAINT fk_characters_account
        FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
