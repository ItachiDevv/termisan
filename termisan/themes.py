"""Anime theme definitions for Termisan.

Contains 20 anime themes split into two categories:
- All-Time Classics (10): The most popular anime of all time
- Modern Hits (10): The most popular anime from 2019-2026
"""

from dataclasses import dataclass, field


@dataclass
class AnimeTheme:
    """A complete anime theme configuration."""

    id: str
    name: str
    category: str  # "classic" or "modern"
    year: str
    genre: str
    description: str

    # Colors (rich color names or hex)
    color_primary: str
    color_secondary: str
    color_accent: str
    color_bg: str
    color_text: str

    # Border styling
    border_style: str  # "heavy", "double", "rounded", etc.
    border_color: str

    # Prompt
    prompt_icon: str
    prompt_style: str

    # Quotes from the anime
    quotes: list[str] = field(default_factory=list)

    # Welcome message
    welcome: str = ""

    # Status bar text
    status_left: str = ""
    status_right: str = ""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ALL-TIME CLASSICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DRAGON_BALL_Z = AnimeTheme(
    id="dragonball",
    name="Dragon Ball Z",
    category="classic",
    year="1989-1996",
    genre="Action / Martial Arts",
    description="Follow Goku and the Z Fighters defending Earth against powerful foes",
    color_primary="#FF8C00",
    color_secondary="#FFD700",
    color_accent="#1E90FF",
    color_bg="#1A0A00",
    color_text="#FFE4B5",
    border_style="heavy",
    border_color="#FF8C00",
    prompt_icon="🐉",
    prompt_style="#FFD700",
    quotes=[
        "I am the hope of the universe! — Goku",
        "It's over 9000! — Vegeta",
        "Power comes in response to a need, not a desire. — Goku",
        "Push through the pain. Giving up hurts more. — Vegeta",
        "Strength is the only thing that matters in this world. — Vegeta",
    ],
    welcome="KAKAROT! Welcome to the Hyperbolic Time Chamber of coding!",
    status_left="⚡ Power Level: MAXIMUM",
    status_right="🌀 Saiyan Mode Active",
)

ONE_PIECE = AnimeTheme(
    id="onepiece",
    name="One Piece",
    category="classic",
    year="1999-Present",
    genre="Adventure / Fantasy",
    description="Join Monkey D. Luffy and the Straw Hat Pirates on their quest for the One Piece",
    color_primary="#CC0000",
    color_secondary="#FFD700",
    color_accent="#1C75BC",
    color_bg="#0A0A1E",
    color_text="#FFF8DC",
    border_style="double",
    border_color="#CC0000",
    prompt_icon="🏴‍☠️",
    prompt_style="#CC0000",
    quotes=[
        "I'm gonna be King of the Pirates! — Luffy",
        "When do you think people die? When they are forgotten. — Dr. Hiluluk",
        "Nothing happened. — Zoro",
        "A man's dream will never die! — Blackbeard",
        "The sea is vast. One day you'll find nakama. — Jinbe",
    ],
    welcome="Set sail, nakama! The Grand Line of code awaits!",
    status_left="🏴‍☠️ Straw Hat Crew",
    status_right="🌊 Grand Line Navigator",
)

NARUTO = AnimeTheme(
    id="naruto",
    name="Naruto",
    category="classic",
    year="2002-2017",
    genre="Action / Ninja",
    description="Follow Naruto Uzumaki's journey from outcast to Hokage",
    color_primary="#FF6600",
    color_secondary="#FFA500",
    color_accent="#4169E1",
    color_bg="#0D0D1A",
    color_text="#FFF0E0",
    border_style="heavy",
    border_color="#FF6600",
    prompt_icon="🍥",
    prompt_style="#FF6600",
    quotes=[
        "Believe it! — Naruto",
        "I'm not gonna run away. I never go back on my word! — Naruto",
        "Those who break the rules are scum, but those who abandon their friends are worse. — Kakashi",
        "The true measure of a shinobi is not how he lives but how he dies. — Jiraiya",
        "Hard work is worthless for those that don't believe in themselves. — Naruto",
    ],
    welcome="Believe it! The Will of Code burns strong in you, dattebayo!",
    status_left="🍥 Hokage Mode",
    status_right="📜 Shadow Clone Jutsu Ready",
)

ATTACK_ON_TITAN = AnimeTheme(
    id="aot",
    name="Attack on Titan",
    category="classic",
    year="2013-2023",
    genre="Dark Fantasy / Action",
    description="Humanity fights for survival against the monstrous Titans",
    color_primary="#8B0000",
    color_secondary="#556B2F",
    color_accent="#C0C0C0",
    color_bg="#0A0A0A",
    color_text="#D3D3D3",
    border_style="heavy",
    border_color="#556B2F",
    prompt_icon="⚔️",
    prompt_style="#8B0000",
    quotes=[
        "If you win, you live. If you lose, you die. If you don't fight, you can't win! — Eren",
        "The world is merciless, and it's also very beautiful. — Mikasa",
        "Give up on your dreams and die. — Levi",
        "I will keep moving forward. — Eren",
        "This world is cruel... but also very beautiful. — Mikasa",
    ],
    welcome="Dedicate your heart! The walls of bugs shall fall before you!",
    status_left="🗡️ Survey Corps",
    status_right="🛡️ Wings of Freedom",
)

POKEMON = AnimeTheme(
    id="pokemon",
    name="Pokémon",
    category="classic",
    year="1997-Present",
    genre="Adventure / Fantasy",
    description="Catch 'em all with Ash and Pikachu on their journey to become Pokémon Masters",
    color_primary="#FFCB05",
    color_secondary="#3D7DCA",
    color_accent="#FF0000",
    color_bg="#0A0A2E",
    color_text="#FFFFFF",
    border_style="rounded",
    border_color="#FFCB05",
    prompt_icon="⚡",
    prompt_style="#FFCB05",
    quotes=[
        "I see now that the circumstances of one's birth are irrelevant. — Mewtwo",
        "Gotta catch 'em all! — Ash",
        "There's no sense in going out of your way just to get somebody to like you. — Pikachu",
        "A Caterpie may change into a Butterfree, but the heart remains the same. — Brock",
        "The important thing is not how long you live. It's what you accomplish. — Mewtwo",
    ],
    welcome="A wild coding session appeared! Pikachu, I choose you!",
    status_left="⚡ Pokéball Ready",
    status_right="🎮 Pokédex Online",
)

DEATH_NOTE = AnimeTheme(
    id="deathnote",
    name="Death Note",
    category="classic",
    year="2006-2007",
    genre="Psychological Thriller",
    description="A supernatural notebook grants the power to kill — and a deadly game of cat and mouse begins",
    color_primary="#8B0000",
    color_secondary="#2F2F2F",
    color_accent="#FFD700",
    color_bg="#0D0D0D",
    color_text="#C8C8C8",
    border_style="heavy",
    border_color="#8B0000",
    prompt_icon="📓",
    prompt_style="#8B0000",
    quotes=[
        "I am justice! — Light Yagami",
        "L, did you know? Shinigami only eat apples. — Ryuk",
        "In this world, there is only good and evil. — Light",
        "The human whose name is written in this note shall die. — Death Note Rules",
        "I'll take a potato chip... and eat it! — Light",
    ],
    welcome="The name of every bug shall be written... in the Death Note.",
    status_left="📓 Death Note Active",
    status_right="🍎 Shinigami Realm",
)

FMA_BROTHERHOOD = AnimeTheme(
    id="fma",
    name="Fullmetal Alchemist: Brotherhood",
    category="classic",
    year="2009-2010",
    genre="Action / Fantasy",
    description="The Elric brothers seek the Philosopher's Stone to restore their bodies",
    color_primary="#B8860B",
    color_secondary="#CD853F",
    color_accent="#DC143C",
    color_bg="#0E0E14",
    color_text="#F5DEB3",
    border_style="double",
    border_color="#B8860B",
    prompt_icon="⚗️",
    prompt_style="#B8860B",
    quotes=[
        "A lesson without pain is meaningless. — Edward Elric",
        "Humankind cannot gain anything without first giving something in return. — Alphonse",
        "It's a terrible day for rain. — Roy Mustang",
        "Stand up and walk. Keep moving forward. — Edward Elric",
        "The world isn't perfect. But it's there for us. — Roy Mustang",
    ],
    welcome="Equivalent Exchange: your effort for elegant code! Transmutation circle ready.",
    status_left="⚗️ Transmutation Active",
    status_right="🔴 Philosopher's Stone",
)

HUNTER_X_HUNTER = AnimeTheme(
    id="hxh",
    name="Hunter x Hunter",
    category="classic",
    year="2011-2014",
    genre="Action / Adventure",
    description="Gon Freecss embarks on a journey to find his father and become a Hunter",
    color_primary="#228B22",
    color_secondary="#32CD32",
    color_accent="#FF4500",
    color_bg="#0A1A0A",
    color_text="#E0FFE0",
    border_style="rounded",
    border_color="#228B22",
    prompt_icon="🎯",
    prompt_style="#228B22",
    quotes=[
        "You should enjoy the little detours to the fullest. — Ging",
        "If you want to get to know someone, find out what makes them angry. — Gon",
        "Human potential for evolution is limitless. — Netero",
        "There are liars who only lie when there's a reason to. — Kurapika",
        "I do not fear death. I fear only that my rage will fade over time. — Kurapika",
    ],
    welcome="Your Nen ability: Code Manipulation! Hunter License activated.",
    status_left="🎯 Nen Activated",
    status_right="💚 Hunter License",
)

BLEACH = AnimeTheme(
    id="bleach",
    name="Bleach",
    category="classic",
    year="2004-2012 / 2022-2025",
    genre="Action / Supernatural",
    description="Ichigo Kurosaki becomes a Soul Reaper to protect the living and the dead",
    color_primary="#000000",
    color_secondary="#FF4500",
    color_accent="#00BFFF",
    color_bg="#0A0A14",
    color_text="#E8E8E8",
    border_style="heavy",
    border_color="#FF4500",
    prompt_icon="🗡️",
    prompt_style="#FF4500",
    quotes=[
        "If I were the rain, could I connect with someone's heart? — Orihime",
        "We stand in awe before that which cannot be seen. — Rukia",
        "I'm not fighting because I want to win. I'm fighting because I have to. — Ichigo",
        "Abandon your fear. Turn and face him. Don't give an inch. — Zangetsu",
        "The blade is me. — Ichigo",
    ],
    welcome="BANKAI! Your Zanpakuto is ready to slice through bugs!",
    status_left="🗡️ Bankai Released",
    status_right="💀 Soul Society Link",
)

COWBOY_BEBOP = AnimeTheme(
    id="bebop",
    name="Cowboy Bebop",
    category="classic",
    year="1998-1999",
    genre="Sci-Fi / Noir",
    description="Bounty hunters Spike and Jet cruise through space on the Bebop",
    color_primary="#8B4513",
    color_secondary="#DAA520",
    color_accent="#4682B4",
    color_bg="#0F0F0F",
    color_text="#DEB887",
    border_style="rounded",
    border_color="#DAA520",
    prompt_icon="🚀",
    prompt_style="#DAA520",
    quotes=[
        "See you space cowboy... — End Card",
        "Whatever happens, happens. — Spike",
        "I'm not going there to die. I'm going to find out if I'm really alive. — Spike",
        "The past is the past and the future is the future. — Spike",
        "You're gonna carry that weight. — End Card",
    ],
    welcome="3... 2... 1... Let's jam! Coding session on the Bebop begins.",
    status_left="🚀 Bebop Cruising",
    status_right="🎷 Jazz Mode",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODERN HITS (2019-2026)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEMON_SLAYER = AnimeTheme(
    id="demonslayer",
    name="Demon Slayer",
    category="modern",
    year="2019-Present",
    genre="Action / Supernatural",
    description="Tanjiro Kamado fights demons to save his sister and avenge his family",
    color_primary="#DC143C",
    color_secondary="#228B22",
    color_accent="#87CEEB",
    color_bg="#0A0A14",
    color_text="#FFF0F5",
    border_style="heavy",
    border_color="#DC143C",
    prompt_icon="🔥",
    prompt_style="#DC143C",
    quotes=[
        "No matter how many people you may lose, you have no choice but to go on living. — Tanjiro",
        "Don't ever give others a chance to kill you! — Zenitsu",
        "The strong should aid and protect the weak. — Rengoku",
        "Set your heart ablaze! — Rengoku",
        "All I can do is work hard! That's the story of my life! — Zenitsu",
    ],
    welcome="Total Concentration Breathing: Code Form! Your blade glows with purpose.",
    status_left="🔥 Hinokami Kagura",
    status_right="🌙 Demon Slayer Corps",
)

JUJUTSU_KAISEN = AnimeTheme(
    id="jjk",
    name="Jujutsu Kaisen",
    category="modern",
    year="2020-Present",
    genre="Action / Supernatural",
    description="Yuji Itadori joins the world of Jujutsu sorcerers after swallowing Sukuna's finger",
    color_primary="#4B0082",
    color_secondary="#9400D3",
    color_accent="#FF1493",
    color_bg="#0D0D1E",
    color_text="#E6E6FA",
    border_style="heavy",
    border_color="#4B0082",
    prompt_icon="👁️",
    prompt_style="#9400D3",
    quotes=[
        "Throughout Heaven and Earth, I alone am the honored one. — Gojo",
        "I'm going to help people. — Yuji",
        "Dying to win and risking death to win are completely different. — Todo",
        "It's not about whether I can. I have to do it. — Yuji",
        "Are you the strongest because you're Gojo Satoru? Or are you Gojo Satoru because you're the strongest? — Geto",
    ],
    welcome="Domain Expansion: Infinite Code Repository! Cursed energy flows through your fingers.",
    status_left="👁️ Six Eyes Active",
    status_right="🔮 Cursed Energy: MAX",
)

MY_HERO_ACADEMIA = AnimeTheme(
    id="mha",
    name="My Hero Academia",
    category="modern",
    year="2016-2025",
    genre="Action / Superhero",
    description="Izuku Midoriya inherits a powerful Quirk and trains to become the greatest hero",
    color_primary="#00AA00",
    color_secondary="#FF4444",
    color_accent="#FFD700",
    color_bg="#0A1A0A",
    color_text="#E0FFE0",
    border_style="double",
    border_color="#00AA00",
    prompt_icon="💪",
    prompt_style="#00AA00",
    quotes=[
        "It's fine now. Why? Because I am here! — All Might",
        "Sometimes I do feel like I'm a failure. Like there's no hope for me. — Deku",
        "If you feel yourself hitting up against your limit, remember for what reason you clench your fists. — All Might",
        "Go beyond! PLUS ULTRA! — UA Motto",
        "A hero is someone who can smile in the face of adversity. — All Might",
    ],
    welcome="PLUS ULTRA! Your Quirk: Code for All! Go beyond your limits!",
    status_left="💪 One For All: 100%",
    status_right="🏫 UA Academy Online",
)

SPY_X_FAMILY = AnimeTheme(
    id="spyfamily",
    name="Spy x Family",
    category="modern",
    year="2022-Present",
    genre="Comedy / Action",
    description="A spy, an assassin, and a telepath form a fake family for a secret mission",
    color_primary="#FF69B4",
    color_secondary="#FFB6C1",
    color_accent="#4169E1",
    color_bg="#14081E",
    color_text="#FFF0F5",
    border_style="rounded",
    border_color="#FF69B4",
    prompt_icon="🥜",
    prompt_style="#FF69B4",
    quotes=[
        "Waku waku! — Anya",
        "I will create a world where children won't have to cry. — Loid",
        "Papa is so cool! — Anya",
        "Everyone has a part of their lives they don't want others to know about. — Loid",
        "Anya wants to go on a mission! — Anya",
    ],
    welcome="WAKU WAKU! Operation: Code Mastery is a go! Anya can read your bugs~",
    status_left="🥜 Mission Active",
    status_right="🕵️ Operation Strix",
)

FRIEREN = AnimeTheme(
    id="frieren",
    name="Frieren: Beyond Journey's End",
    category="modern",
    year="2023-Present",
    genre="Fantasy / Adventure",
    description="An elf mage reflects on her journey and the bonds she formed with her mortal companions",
    color_primary="#9370DB",
    color_secondary="#E6E6FA",
    color_accent="#98FB98",
    color_bg="#0D0A1E",
    color_text="#E8E0FF",
    border_style="rounded",
    border_color="#9370DB",
    prompt_icon="✨",
    prompt_style="#9370DB",
    quotes=[
        "I should have tried to learn more about him. — Frieren",
        "Humans have such short lives, and yet they shine so brightly. — Frieren",
        "Magic is amazing. It can make flowers bloom even in the dead of winter. — Frieren",
        "I just didn't get to know them well enough. — Frieren",
        "These moments we share are precious. — Frieren",
    ],
    welcome="A journey of a thousand lines begins with a single function. Take your time.",
    status_left="✨ Zoltraak Ready",
    status_right="🌸 Era of Humans",
)

OSHI_NO_KO = AnimeTheme(
    id="oshinoko",
    name="Oshi no Ko",
    category="modern",
    year="2023-Present",
    genre="Drama / Supernatural",
    description="Reincarnated as the children of a famous idol, twins navigate the dark side of show business",
    color_primary="#00BFFF",
    color_secondary="#FF69B4",
    color_accent="#FFD700",
    color_bg="#0A0A1E",
    color_text="#E0F0FF",
    border_style="double",
    border_color="#00BFFF",
    prompt_icon="⭐",
    prompt_style="#00BFFF",
    quotes=[
        "The truth about this world is hidden behind a curtain of lies. — Aqua",
        "I want to shine on stage! — Ruby",
        "In this world, talent is a form of violence. — Kana",
        "Lies are the foundation of the entertainment world. — Aqua",
        "Sometimes you need to perform to survive. — Ai",
    ],
    welcome="The spotlight shines on your code! Star Eye activated — let's put on a show!",
    status_left="⭐ Star Eye Active",
    status_right="🎭 Stage is Set",
)

SOLO_LEVELING = AnimeTheme(
    id="sololeveling",
    name="Solo Leveling",
    category="modern",
    year="2024-Present",
    genre="Action / Fantasy",
    description="The weakest hunter Sung Jin-Woo gains a mysterious system that allows him to level up infinitely",
    color_primary="#4B0082",
    color_secondary="#8A2BE2",
    color_accent="#00CED1",
    color_bg="#050510",
    color_text="#D8BFD8",
    border_style="heavy",
    border_color="#8A2BE2",
    prompt_icon="🗡️",
    prompt_style="#8A2BE2",
    quotes=[
        "I alone level up. — Sung Jin-Woo",
        "Arise. — Sung Jin-Woo",
        "I'm used to being alone. — Sung Jin-Woo",
        "The weak have no right to choose how they die. — Igris",
        "I will become strong enough to protect everyone. — Sung Jin-Woo",
    ],
    welcome="ARISE! Your shadow army of functions awaits your command, Shadow Monarch!",
    status_left="🗡️ Shadow Monarch",
    status_right="📊 Level: ???",
)

CHAINSAW_MAN = AnimeTheme(
    id="chainsawman",
    name="Chainsaw Man",
    category="modern",
    year="2022-Present",
    genre="Action / Horror",
    description="Denji merges with a chainsaw devil and becomes a Public Safety Devil Hunter",
    color_primary="#FF4500",
    color_secondary="#FF6347",
    color_accent="#FFD700",
    color_bg="#1A0A0A",
    color_text="#FFE4E1",
    border_style="heavy",
    border_color="#FF4500",
    prompt_icon="🪚",
    prompt_style="#FF4500",
    quotes=[
        "I want to live a normal life! — Denji",
        "Devils are born from fears. — Makima",
        "The chainsaw devil is special. — Makima",
        "I'll kill anyone who gets in the way of my dream. — Denji",
        "This is the kind of life I've always wanted. — Denji",
    ],
    welcome="BRRRRR! The Chainsaw revs up! Time to tear through code like a devil hunter!",
    status_left="🪚 Chainsaw Active",
    status_right="😈 Devil Contract",
)

APOTHECARY_DIARIES = AnimeTheme(
    id="apothecary",
    name="The Apothecary Diaries",
    category="modern",
    year="2024-Present",
    genre="Mystery / Historical",
    description="Maomao uses her pharmaceutical knowledge to solve mysteries in the imperial court",
    color_primary="#8B4513",
    color_secondary="#D2691E",
    color_accent="#FF6347",
    color_bg="#14100A",
    color_text="#FAEBD7",
    border_style="rounded",
    border_color="#D2691E",
    prompt_icon="🧪",
    prompt_style="#D2691E",
    quotes=[
        "Poison and medicine are two sides of the same coin. — Maomao",
        "I simply find it fascinating. — Maomao",
        "Knowledge is the best weapon. — Maomao",
        "The truth is always in the details. — Maomao",
        "Curiosity is a virtue, not a sin. — Maomao",
    ],
    welcome="The prescription is clear: debug with precision and curiosity! Maomao approves.",
    status_left="🧪 Analyzing...",
    status_right="📜 Imperial Court",
)

CYBERPUNK_EDGERUNNERS = AnimeTheme(
    id="cyberpunk",
    name="Cyberpunk: Edgerunners",
    category="modern",
    year="2022",
    genre="Sci-Fi / Cyberpunk",
    description="David Martinez installs military-grade cyberware and becomes an edgerunner in Night City",
    color_primary="#00FFFF",
    color_secondary="#FF00FF",
    color_accent="#FFFF00",
    color_bg="#0A0A14",
    color_text="#E0FFFF",
    border_style="heavy",
    border_color="#00FFFF",
    prompt_icon="🌃",
    prompt_style="#00FFFF",
    quotes=[
        "You either run from things or face them head on. — David",
        "Night City will eat you alive if you let it. — Maine",
        "This is the edge, choom. — Lucy",
        "Let's go to the moon. — Lucy",
        "An edgerunner lives on the edge — that's the whole point. — Maine",
    ],
    welcome="Jacking in, choom. Night City's neural link to your codebase is live. Stay chrome!",
    status_left="🌃 Jacked In",
    status_right="⚡ Cyberware Online",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# THEME REGISTRY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ALL_THEMES: dict[str, AnimeTheme] = {
    t.id: t
    for t in [
        DRAGON_BALL_Z,
        ONE_PIECE,
        NARUTO,
        ATTACK_ON_TITAN,
        POKEMON,
        DEATH_NOTE,
        FMA_BROTHERHOOD,
        HUNTER_X_HUNTER,
        BLEACH,
        COWBOY_BEBOP,
        DEMON_SLAYER,
        JUJUTSU_KAISEN,
        MY_HERO_ACADEMIA,
        SPY_X_FAMILY,
        FRIEREN,
        OSHI_NO_KO,
        SOLO_LEVELING,
        CHAINSAW_MAN,
        APOTHECARY_DIARIES,
        CYBERPUNK_EDGERUNNERS,
    ]
}

CLASSIC_THEMES = {k: v for k, v in ALL_THEMES.items() if v.category == "classic"}
MODERN_THEMES = {k: v for k, v in ALL_THEMES.items() if v.category == "modern"}
