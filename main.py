from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
import argparse
import sqlite3

# Set the log level to be info by default
logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("year", type=int, help="Competition year")
parser.add_argument("start_round", type=int, help="The first round to pull")
parser.add_argument("final_round", type=int, help="The final round to pull")
args = parser.parse_args()


cnx = sqlite3.connect("nrl.db")


# Set up the driver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def get_games_in_round(round_url):
    """
    Takes in the URL for the matches in the round and returns a list of all the URLs to each match.
    """
    driver.get(round_url)

    # Find the div with the specific id using find_element
    vue_draw_div = driver.find_element(By.ID, "vue-draw")

    # Extract the q-data attribute
    q_data = vue_draw_div.get_attribute("q-data")

    # Parse the q-data attribute as JSON
    q_data_json = json.loads(q_data.replace("&quot;", '"'))

    match_centre_urls = []

    # Extract the matchCentreUrl for each fixture
    for fixture in q_data_json["fixtures"]:
        match_centre_url = fixture["matchCentreUrl"]
        full_match_centre_url = "https://www.nrl.com" + match_centre_url
        match_centre_urls.append(full_match_centre_url)

        LOG.info(f"Matches in round array:{match_centre_urls}")

    return match_centre_urls


def match_data_extractor(match_url):

    response = requests.get(match_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    q_data = soup.find("div", {"id": "vue-match-centre"}).get("q-data")

    q_data_dict = json.loads(q_data)
    match_data = q_data_dict["match"]

    # match table
    match_stats = {
        "id": int(match_data["matchId"]),
        "round_number": match_data["roundNumber"],
        "competition_id": 111,
        "home_team_id": match_data["homeTeam"]["teamId"],
        "away_team_id": match_data["awayTeam"]["teamId"],
        "start_time": match_data["startTime"],
        "stadium": match_data["venue"],
        "city": match_data["venueCity"],
        "attendence": match_data["attendance"],
        "ground_conditions": "good",
        "home_team_score": match_data["homeTeam"]["score"],
        "away_team_score": match_data["awayTeam"]["score"],
    }

    LOG.info(match_stats)

    return match_stats


def player_stat_extractor(match_url, team):

    response = requests.get(match_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    q_data = soup.find("div", {"id": "vue-match-centre"}).get("q-data")

    q_data_dict = json.loads(q_data)

    match_data = q_data_dict["match"]

    # Assuming you have already loaded match_data JSON object
    team_stats = match_data["stats"]["players"][f"{team.lower()}Team"]

    team_players = match_data[f"{team.lower()}Team"]["players"]

    player_dict = {}
    for player in team_players:
        player_id = player["playerId"]
        full_name = player["firstName"] + " " + player["lastName"]
        position = player["position"]
        player_dict[player_id] = {"name": full_name, "position": position}

    players_stats_for_team = []
    for player in team_stats:
        player_stats = {
            "id": str(player["playerId"]) + str(match_data["matchId"]),
            "player_id": int(player["playerId"]),
            "player_team_id": match_data[f"{team.lower()}Team"]["teamId"],
            "player_name": player_dict.get(int(player["playerId"]))["name"],
            "player_position": player_dict.get(int(player["playerId"]))["position"],
            "game_id": int(match_data["matchId"]),
            "all_run_metres": player["allRunMetres"],
            "all_runs": player["allRuns"],
            "bomb_kicks": player["bombKicks"],
            "cross_field_kicks": player["crossFieldKicks"],
            "conversions": player["conversions"],
            "conversion_attempts": player["conversionAttempts"],
            "dummy_half_runs": player["dummyHalfRuns"],
            "dummy_half_run_metres": player["dummyHalfRunMetres"],
            "dummy_passes": player["dummyPasses"],
            "errors": player["errors"],
            "fantasy_points_total": player["fantasyPointsTotal"],
            "field_goals": player["fieldGoals"],
            "forced_drop_out_kicks": player["forcedDropOutKicks"],
            "forty_twenty_kicks": player["fortyTwentyKicks"],
            "goals": player["goals"],
            "goal_conversion_rate": player["goalConversionRate"],
            "grubber_kicks": player["grubberKicks"],
            "handling_errors": player["handlingErrors"],
            "hit_ups": player["hitUps"],
            "hit_up_run_metres": player["hitUpRunMetres"],
            "ineffective_tackles": player["ineffectiveTackles"],
            "intercepts": player["intercepts"],
            "kicks": player["kicks"],
            "kicks_dead": player["kicksDead"],
            "kicks_defused": player["kicksDefused"],
            "kick_metres": player["kickMetres"],
            "kick_return_metres": player["kickReturnMetres"],
            "line_break_assists": player["lineBreakAssists"],
            "line_breaks": player["lineBreaks"],
            "line_engaged_runs": player["lineEngagedRuns"],
            "minutes_played": player["minutesPlayed"],
            "missed_tackles": player["missedTackles"],
            "offloads": player["offloads"],
            "offside_within_ten_metres": player["offsideWithinTenMetres"],
            "one_on_one_lost": player["oneOnOneLost"],
            "one_on_one_steal": player["oneOnOneSteal"],
            "on_report": player["onReport"],
            "passes_to_run_ratio": player["passesToRunRatio"],
            "passes": player["passes"],
            "play_the_ball_total": player["playTheBallTotal"],
            "play_the_ball_average_speed": player["playTheBallAverageSpeed"],
            "penalties": player["penalties"],
            "points": player["points"],
            "penalty_goals": player["penaltyGoals"],
            "post_contact_metres": player["postContactMetres"],
            "receipts": player["receipts"],
            "ruck_infringements": player["ruckInfringements"],
            "send_offs": player["sendOffs"],
            "sin_bins": player["sinBins"],
            "stint_one": player["stintOne"],
            # 'stint_two': player['stintTwo'],
            "tackle_breaks": player["tackleBreaks"],
            "tackle_efficiency": player["tackleEfficiency"],
            "tackles_made": player["tacklesMade"],
            "tries": player["tries"],
            "try_assists": player["tryAssists"],
            "twenty_forty_kicks": player["twentyFortyKicks"],
            "two_point_field_goals": player["twoPointFieldGoals"],
        }
        players_stats_for_team.append(player_stats)
    return players_stats_for_team


def main(match_list):

    for match in match_list:
        LOG.info(match)
        match_data_to_be_inserted = match_data_extractor(match)
        # Construct the insert query using parameterized placeholders
        columns = ", ".join(match_data_to_be_inserted.keys())
        placeholders = ", ".join(["?"] * len(match_data_to_be_inserted))
        query = f"INSERT INTO game ({columns}) VALUES ({placeholders})"
        values = tuple(match_data_to_be_inserted.values())

        # Execute the query for match stats
        cursor = cnx.cursor()
        cursor.execute(query, values)
        cnx.commit()
        LOG.info(f"{cursor.rowcount} rows inserted.")
        cursor.close()

        home_player_date_to_be_inserted = player_stat_extractor(match, team="home")

        LOG.info(f"Getting home team data.")

        for home_player in home_player_date_to_be_inserted:
            columns = ", ".join(home_player.keys())
            placeholders = ", ".join(["?"] * len(home_player))
            query = (
                f"INSERT INTO playerGameStatistics ({columns}) VALUES ({placeholders})"
            )
            values = tuple(home_player.values())

            # Execute the query for match stats
            cursor = cnx.cursor()
            cursor.execute(query, values)
            cnx.commit()
            LOG.info(f"{cursor.rowcount} rows inserted.")
            cursor.close()

            away_player_data_to_be_inserted = player_stat_extractor(match, team="away")

        LOG.info(f"Getting away team data.")
        for away_player in away_player_data_to_be_inserted:
            columns = ", ".join(away_player.keys())
            placeholders = ", ".join(["?"] * len(away_player))
            query = (
                f"INSERT INTO playerGameStatistics ({columns}) VALUES ({placeholders})"
            )
            values = tuple(away_player.values())

            # Execute the query for match stats
            cursor = cnx.cursor()
            cursor.execute(query, values)
            cnx.commit()
            LOG.info(f"{cursor.rowcount} rows inserted.")
            cursor.close()


if __name__ == "__main__":
    for round in range(args.start_round, args.final_round + 1):
        LOG.info(f"Getting data from {args.year} Round {round}")
        ROUND_URL = f"https://www.nrl.com/draw/?competition=111&round={round}&season={args.year}"
        round_matches = get_games_in_round(ROUND_URL)
        LOG.info(round_matches)
        main(round_matches)
