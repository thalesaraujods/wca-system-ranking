import unittest

import pandas as pd

from domain.scoring import (
    build_combined_dataframe,
    build_general_ranking,
    build_stage_ranking,
    calculate_points,
)


def competition_payload(*results):
    return {
        "competitionEvents": [
            {
                "event": {"name": "3x3x3 Cube"},
                "rounds": [
                    {
                        "number": 1,
                        "results": list(results),
                    }
                ],
            }
        ]
    }


def result(name, ranking, wca_id=None):
    person = {"name": name}
    if wca_id:
        person["wcaId"] = wca_id
    return {"ranking": ranking, "person": person}


class ScoringTest(unittest.TestCase):
    def test_calculate_points_uses_aps_formula(self):
        self.assertEqual(calculate_points(10, 1), 5.0)
        self.assertEqual(calculate_points(10, 4), 2.0)
        self.assertEqual(calculate_points(0, 1), 0.0)
        self.assertEqual(calculate_points(10, None), 0.0)

    def test_build_combined_dataframe_skips_missing_stage_and_unranked_results(self):
        stages = {
            "Stage A": competition_payload(
                result("Ana", 1, "2024ANAA01"),
                result("Bruno", None, "2024BRUN01"),
            ),
            "Stage B": None,
        }

        df = build_combined_dataframe(stages)

        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["Etapa"], "Stage A")
        self.assertEqual(df.iloc[0]["Nome"], "Ana")
        self.assertEqual(df.iloc[0]["Competidor ID"], "2024ANAA01")

    def test_general_ranking_groups_by_competitor_id_when_available(self):
        df = pd.DataFrame(
            [
                {
                    "Competidor ID": "2024ANAA01",
                    "Nome": "Ana Silva",
                    "Pontos": 4.0,
                },
                {
                    "Competidor ID": "2024ANAA01",
                    "Nome": "Ana S.",
                    "Pontos": 3.0,
                },
                {
                    "Competidor ID": "2024BRUN01",
                    "Nome": "Bruno Lima",
                    "Pontos": 5.0,
                },
            ]
        )

        ranking = build_general_ranking(df)

        self.assertEqual(ranking.iloc[0]["Competidor"], "Ana Silva")
        self.assertEqual(ranking.iloc[0]["Pontos Totais"], 7.0)
        self.assertEqual(ranking.iloc[0]["#"], 1)

    def test_general_ranking_uses_dense_rank_for_ties(self):
        df = pd.DataFrame(
            [
                {"Nome": "Ana", "Pontos": 5.0},
                {"Nome": "Bruno", "Pontos": 5.0},
                {"Nome": "Caio", "Pontos": 3.0},
            ]
        )

        ranking = build_general_ranking(df)

        self.assertEqual(ranking["#"].tolist(), [1, 1, 2])

    def test_stage_ranking_filters_stage(self):
        df = pd.DataFrame(
            [
                {
                    "Etapa": "Stage A",
                    "Competidor ID": "ana",
                    "Nome": "Ana",
                    "Pontos": 2.0,
                },
                {
                    "Etapa": "Stage B",
                    "Competidor ID": "ana",
                    "Nome": "Ana",
                    "Pontos": 10.0,
                },
            ]
        )

        ranking = build_stage_ranking(df, "Stage A")

        self.assertEqual(len(ranking), 1)
        self.assertEqual(ranking.iloc[0]["Pontos na Etapa"], 2.0)


if __name__ == "__main__":
    unittest.main()
