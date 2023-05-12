"""
Functions to (set when to) update predicted ratings
"""

new_ratings_counter = 0  # global variable


def increment_new_ratings_counter():
    """
    Increment the global variable new_ratings_counter by 1, meaning there has been a new rating
    """

    global new_ratings_counter
    new_ratings_counter = new_ratings_counter + 1


def check_update_predicted_ratings():
    """
    Check if the predicted ratings shall be updated or not.
    If yes, set the new_ratings_counter back to 0
    :return: True if they shall be updated, False if not
    """

    global new_ratings_counter

    print(new_ratings_counter)

    if new_ratings_counter >= 1:
        new_ratings_counter = 0
        return True

    return False
