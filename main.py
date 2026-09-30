import json
from django.db import transaction
import init_django_orm  # noqa: F401
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as f:
        players_data = json.load(f)

    with transaction.atomic():
        for player_name, pdata in players_data.items():

            race, _ = Race.objects.get_or_create(
                name=pdata["race"]["name"],
                defaults={
                    "description": pdata["race"]["description"]
                    }
            )

            guild = None
            if pdata["guild"]:
                guild, _ = Guild.objects.get_or_create(
                    name=pdata["guild"]["name"],
                    defaults={
                        "description": pdata["guild"]["description"]
                    }
                )

            for skill_data in pdata["race"].get("skills", []):

                skill, _ = Skill.objects.get_or_create(
                    name=skill_data["name"],
                    defaults={
                        "bonus": skill_data["bonus"],
                        "race": race
                    }
                )

            player, _ = Player.objects.get_or_create(
                nickname=player_name,
                defaults={
                    "email": pdata["email"],
                    "bio": pdata["bio"],
                    "race": race,
                    "guild": guild,
                }
            )


if __name__ == "__main__":
    main()
