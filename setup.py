from project_db import insert_admin_and_subreddit, create_tables, insert_initial_configs, insert_default_admin

initial_configs = [
    ('REDDIT_POST_TYPE', 'new'),
    ('REDDIT_MAX_PAGES_PER_SUBREDDIT', '2'),
    ('DELAY_IN_FETCHING_POSTS_IN_SECONDS', '30'),
    ('REDDIT_MESSAGE_RATE_LIMIT_PER_HOUR', '12'),
    ('REPLYING', True),
]

create_tables()
insert_initial_configs(initial_configs)
insert_default_admin()

insert_admin_and_subreddit('DiscussionAware113', 'AskAMechanic, Toyota, AskMechanics, MechanicAdvice,Jeep', 'Battery, dashboard light, coolant, smell, smoke, codes, wiring, smoking, head gasket, why, need advice, wrong with my car, engine, what is causing this, leak, dies, Battery issues, dashboard light warnings, coolant problems, unusual smell, smoke detection, diagnostic codes, wiring concerns, excessive smoking, head gasket failure, reasons for malfunction, identifying what\'s wrong with my car, engine troubles, understanding what is causing this, leak identification, car suddenly dies, electrical problems, transmission issues, noise from engine, starting difficulties, fuel system problems, overheating, brake failure, steering difficulties, tire issues, and maintenance questions.')
insert_admin_and_subreddit('Heydrianpay', 'Cartalk, CarTalkUk, autorepair, Hyundai', 'Battery, dashboard light, coolant, smell, smoke, codes, wiring, smoking, head gasket, why, need advice, wrong with my car, engine, what is causing this, leak, dies, Battery issues, dashboard light warnings, coolant problems, unusual smell, smoke detection, diagnostic codes, wiring concerns, excessive smoking, head gasket failure, reasons for malfunction, identifying what\'s wrong with my car, engine troubles, understanding what is causing this, leak identification, car suddenly dies, electrical problems, transmission issues, noise from engine, starting difficulties, fuel system problems, overheating, brake failure, steering difficulties, tire issues, and maintenance questions.')
