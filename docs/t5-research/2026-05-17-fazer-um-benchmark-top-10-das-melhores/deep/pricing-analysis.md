# Deep dive: pricing and TCO

{
  "currency": "USD",
  "unit": "USD/yr",
  "scenarios": {
    "solo_founder": {
      "label": "Solo founder · 1 usuário · 2-6 decks/mês",
      "rows": [
        {
          "player": "gamma",
          "setup": "Plus/Pro",
          "low": 96,
          "high": 240,
          "baseline": true
        },
        {
          "player": "canva",
          "setup": "Pro",
          "low": 120,
          "high": 156
        },
        {
          "player": "plus_ai",
          "setup": "Basic/Pro",
          "low": 120,
          "high": 300
        },
        {
          "player": "beautiful_ai",
          "setup": "Pro annual/monthly",
          "low": 144,
          "high": 540
        },
        {
          "player": "presenton",
          "setup": "Self-host BYOK",
          "low": 0,
          "high": 300
        }
      ]
    },
    "growth_squad_10": {
      "label": "Growth squad · 10 usuários · colaboração e marca",
      "rows": [
        {
          "player": "canva",
          "setup": "Teams/Business",
          "low": 1200,
          "high": 2400,
          "baseline": true
        },
        {
          "player": "pitch",
          "setup": "Team annual",
          "low": 2280,
          "high": 2760
        },
        {
          "player": "plus_ai",
          "setup": "Basic/Pro annual",
          "low": 1200,
          "high": 2400
        },
        {
          "player": "beautiful_ai",
          "setup": "Team annual",
          "low": 4800,
          "high": 6000
        },
        {
          "player": "gamma",
          "setup": "Team/Business",
          "low": 2400,
          "high": 4800
        }
      ]
    },
    "enterprise_control": {
      "label": "Enterprise/API · governança, privacidade, escala",
      "rows": [
        {
          "player": "presenton",
          "setup": "Self-host/API + infra/modelos",
          "low": 1500,
          "high": 12000,
          "baseline": true
        },
        {
          "player": "plus_ai",
          "setup": "Enterprise",
          "low": 5000,
          "high": 25000
        },
        {
          "player": "canva",
          "setup": "Enterprise",
          "low": 5000,
          "high": 30000
        },
        {
          "player": "beautiful_ai",
          "setup": "Enterprise",
          "low": 8000,
          "high": 40000
        },
        {
          "player": "pitch",
          "setup": "Enterprise",
          "low": 5000,
          "high": 25000
        }
      ]
    }
  }
}
