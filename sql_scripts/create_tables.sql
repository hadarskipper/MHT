use telegram;

IF OBJECT_ID('[dbo].[raw_updates]', 'U') IS NOT NULL
DROP TABLE [dbo].[raw_updates]
create TABLE  raw_updates (
    update_id bigint primary key identity,
    update_telegram_id bigint,
    content nvarchar(max),
    recived_datetime DATETIME,
    sent_datetime DATETIME,
    from_id bigint
);

IF OBJECT_ID('[dbo].[update_handle_log]', 'U') IS NOT NULL
DROP TABLE [dbo].[update_handle_log]
create TABLE  update_handle_log (
    log_id bigint primary key identity,
    update_id bigint,
    log nvarchar(32),
    log_code INTEGER,
    log_datetime datetime
);

IF OBJECT_ID('[dbo].[state_entries]', 'U') IS NOT NULL
DROP TABLE [dbo].[state_entries]
create TABLE  state_entries (
    state_entry_id bigint primary key identity,
    user_id bigint,
    state_node_id bigint,
    state_entry_datetime datetime
);

IF OBJECT_ID('[dbo].[state_nodes]', 'U') IS NOT NULL
DROP TABLE [dbo].[state_nodes]
create TABLE  state_nodes (
    state_node_id bigint primary key identity,
    state_name nvarchar(32),
    state_desc nvarchar(256),
);

IF OBJECT_ID('[dbo].[options]', 'U') IS NOT NULL
DROP TABLE [dbo].[options]
create TABLE  options (
    option_id bigint primary key identity,
    current_state_node_id bigint,
    end_state_node_id bigint,
    option_name nvarchar(32),
    option_desc nvarchar(256),
);