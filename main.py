import pandas as pd

from config import DEFAULT_TABLE, N_SIMULATIONS, N_USERS, TRAINING_INTERVAL_DAYS, logger
from organization import Organization
from sql import QueryParams, db_connection, query_db_to_df


def create_records_into_db() -> None:
    """Create database records from Hoxhunt training."""
    dummy_organization = Organization(
        n_users=N_USERS, n_simulations=N_SIMULATIONS, training_interval_days=TRAINING_INTERVAL_DAYS
    )
    logger.info("Organization created: %s", dummy_organization)
    dummy_organization.do_training()
    logger.info("Organization has now been trained in Hoxhunt!")
    result = dummy_organization.get_result()
    result.to_sql(DEFAULT_TABLE, db_connection,
                  if_exists="replace", index=None)


def get_data_with_query__types() -> pd.DataFrame:
    """
    Load records from the database into a DataFrame.
    Loads the different user types, their successes and fails and the dates.
    """
    # (Task 3):
    # Write a SQL query that aggregates the simulated data to a format that you want to visualize
    # To do this, you will use a Jinja template that compiles a query from a set of given arguments
    # You are allowed to write multiple queries if you wish to visualize multiple things.

    query_params = QueryParams(
        dimensions=[
            "strftime('%Y-%m', timestamp) AS date",
            "type",
            "COUNT(CASE WHEN outcome = 'SUCCESS' THEN 1 END) AS successes",
            "COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails"
        ],
        table=DEFAULT_TABLE,
        group_by=["date, type"],
        order_by=["date ASC"],
    )

    return query_db_to_df(query_params, result_columns=["date", "type", "successes", "fails"])


def get_data_with_query__individuals() -> pd.DataFrame:
    """
    Load records from the database into a DataFrame.
    Loads the different users, their successes, fails and misses
    """

    query_params = QueryParams(
        dimensions=[
            "user_id",
            "name",
            "type",
            "COUNT(CASE WHEN outcome = 'SUCCESS' THEN 1 END) AS successes",
            "COUNT(CASE WHEN outcome = 'FAIL' THEN 1 END) AS fails",
            "COUNT(CASE WHEN outcome = 'MISS' THEN 1 END) AS misses"
        ],
        table=DEFAULT_TABLE,
        group_by=["user_id"],
        order_by=["name ASC"],
    )

    return query_db_to_df(query_params, result_columns=["user_id", "name", "type", "successes", "fails", "misses"])


def main() -> None:
    """Run the entire simulation application."""
    create_records_into_db()
    logger.info("Training results successfully uploaded to the database")
    aggregated_data_1 = get_data_with_query__types()
    aggregated_data_2 = get_data_with_query__individuals()
    logger.info("Aggregated training results have been fetched from the db.")
    csv_filename_1 = "visualize_types.csv"
    csv_filename_2 = "visualize_individuals.csv"
    aggregated_data_1.to_csv(csv_filename_1, index=False)
    aggregated_data_2.to_csv(csv_filename_2, index=False)
    logger.info("Data ready for visualization can be found in %s and %s",
                csv_filename_1, csv_filename_2)


if __name__ == "__main__":
    main()
