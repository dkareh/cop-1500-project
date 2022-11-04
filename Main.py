# Exercise Calculator
# Author: Daniel Kareh
# Description: Calculates how many calories were burned when biking, running,
#              or swimming, given information about the exercise, such as
#              distance and duration.
# Sources:
#     - https://www.omnicalculator.com/sports/calories-burned-biking
#     - https://www.omnicalculator.com/sports/running-calorie
#     - https://www.omnicalculator.com/sports/swimming-calorie

KILOMETERS_PER_MILE = 1.609344
KILOGRAMS_PER_POUND = 0.45359237
ACRES_PER_SQUARE_MILE = 640
CALORIES_PER_SQUARE = 100
MINUTES_PER_HOUR = 60
LABEL_COLUMN_SIZE = 28
# Most terminals support these "escape sequences". If yours doesn't, change the "True" to "False".
# https://en.wikipedia.org/wiki/ANSI_escape_code
TERMINAL_SUPPORTS_ESCAPE_SEQUENCES = True
if TERMINAL_SUPPORTS_ESCAPE_SEQUENCES:
    CURSOR_UP = "\x1b[A"
    CLEAR_REST_OF_SCREEN = "\x1b[J"
    CLEAR_REST_OF_LINE = "\x1b[K"
else:
    CURSOR_UP = CLEAR_REST_OF_SCREEN = CLEAR_REST_OF_LINE = ""
SWIMMING_STYLES = (
    ["intense backstroke", "backstroke", "intense breaststroke"]
    + ["breaststroke", "butterfly", "intense crawl", "crawl"]
    + ["sidestroke", "high effort treading water", "treading water"]
)
SWIMMING_STYLE_METS = [9.5, 4.8, 10.3, 5.3, 13.8, 10, 8.3, 7, 9.8, 3.5]
TITLE = "Daniel's Exercise Calculator"
COMMANDS = ["biking", "running", "swimming", "swimming styles", "exit"]


def constrain(lower_limit, number, upper_limit):
    return min(max(lower_limit, number), upper_limit)


def get_positive_number(prompt):
    # ljust adds as many spaces as necessary to make the prompt "LABEL_COLUMN_SIZE" characters long.
    prompt = prompt.ljust(LABEL_COLUMN_SIZE) + " | " + CLEAR_REST_OF_LINE
    while True:
        user_input = input(prompt).strip()
        print(CLEAR_REST_OF_SCREEN, end="")  # Clear any previous error message.
        try:
            number = float(user_input)
            if number > 0:
                return number
            print("The number must be positive. Please try again.")
        except:
            print("'" + user_input + "' is not a number. Please try again.")
        # Move the cursor back to the line where the prompt originally was.
        print(CURSOR_UP * 2, end="")


def get_index_of_one_of(prompt, options):
    prompt = prompt.ljust(LABEL_COLUMN_SIZE) + " | " + CLEAR_REST_OF_LINE
    while True:
        user_input = input(prompt).strip().lower()
        print(CLEAR_REST_OF_SCREEN, end="")
        try:
            return options.index(user_input)
        except:
            print("'" + user_input + "' is not an option. Please try again.")
            print(CURSOR_UP * 2, end="")


def print_stat(label, number):
    print(label.ljust(LABEL_COLUMN_SIZE), round(number, 2), sep=" | ")


def calc_biking(weight_kg, distance_miles, duration_hours):
    speed_mph = distance_miles / duration_hours
    # Approximate the "Metabolic Equivalent of Task", a way of measuring the
    # amount of energy expended by doing some physical activity.
    # 1 MET is approximately equal to 1 calorie per kilogram per hour.
    met = constrain(4, speed_mph - 5, 16)
    print_stat("Metabolic Equivalent of Task", met)
    # The distance covered is evenly divided between the four sides of a square.
    side_length_miles = distance_miles / 4
    # The area of a square is always its side length squared.
    area_square_miles = side_length_miles**2
    # Example: If there are 640 acres per square mile, and we have two square
    # miles of land, then we have 2 * 640, or 1,280 acres.
    area_acres = area_square_miles * ACRES_PER_SQUARE_MILE
    print_stat("Traced square area (miles^2)", area_square_miles)
    print_stat("Traced square area (acres)", area_acres)
    calories_burned = duration_hours * met * weight_kg
    return calories_burned


def calc_running(weight_kg, distance_km):
    age_years = get_positive_number("Age (years)?")
    resting_heart_bpm = get_positive_number("Resting heart rate (BPM)?")
    # Your maximum heart rate decreases as you age, so we *subtract* a number
    # proportional to your age to determine your maximum heart rate.
    max_heart_bpm = 208 - 0.7 * age_years
    # Calculate the maximal oxygen consumption: https://en.wikipedia.org/wiki/VO2_max
    vo2_max = 15.3 * max_heart_bpm / resting_heart_bpm
    # Calculate a "cardio-respiratory fitness factor".
    car_resp_fitness_factor = constrain(1, 1.285 - 0.005 * vo2_max, 1.07)
    # The *additional* 0.84 is due to air resistance. The calculator assumes the user is not
    # running on a treadmill, and when you run outdoors, you expend extra energy as you push
    # against the air (you're affected by drag!).
    calories_burned = (0.95 * weight_kg + 0.84) * distance_km * car_resp_fitness_factor
    return calories_burned


def calc_swimming(weight_kg, duration_hours):
    style_index = get_index_of_one_of("Swimming style?", SWIMMING_STYLES)
    style_met = SWIMMING_STYLE_METS[style_index]
    return duration_hours * style_met * weight_kg


def print_calories_bar(label, calories):
    # Calculate the number of squares with division, but always round down.
    # We can't print half of a square!
    number_of_squares = int(calories // CALORIES_PER_SQUARE)
    squares = "█" * number_of_squares
    # Calculate the number of calories that the squares don't represent i.e. the remainder.
    remainder = calories % CALORIES_PER_SQUARE
    # Decide which remainder character to use. For instance, if the remainder is 50 out of 100,
    # print a special character that fills half the area of a normal square.
    remainder_character = "░▌█"[round(remainder / (CALORIES_PER_SQUARE / 2))]
    # Put the label, squares, and remainder together via concatenation.
    print(label.ljust(13) + squares + remainder_character, round(calories))


def main():
    # Print the title and exactly enough horizontal lines ("─") to underline the title.
    print(TITLE, "─" * len(TITLE), sep="\n")
    # Print the commands separated by commas.
    print("The commands are:", ", ".join(COMMANDS))

    exercises = []
    while True:
        print("")  # Print a blank line.
        command_index = get_index_of_one_of("Command?", COMMANDS)

        if command_index == COMMANDS.index("exit"):
            break  # Exit the loop.

        command = COMMANDS[command_index]
        if command == "swimming styles":
            print("\nSwimming styles:")
            for style in SWIMMING_STYLES:
                print(" -", style)
            continue

        weight_lb = get_positive_number("Weight (pounds)?")
        weight_kg = weight_lb * KILOGRAMS_PER_POUND
        print_stat("Weight (kg)", weight_kg)

        if command == "biking" or command == "running":
            distance_miles = get_positive_number("Distance (miles)?")
            distance_km = distance_miles * KILOMETERS_PER_MILE
            print_stat("Distance (km)", distance_km)

        # The unnecessarily verbose condition is just to show that I can use "and", "not", and "!=".
        # De Morgan's laws tell us that the condition is equivalent to:
        # command == "biking" or command == "swimming"
        if not (command != "biking" and command != "swimming"):
            duration_minutes = get_positive_number("Duration (minutes)?")
            duration_hours = duration_minutes / MINUTES_PER_HOUR

        if command == "biking":
            calories_burned = calc_biking(weight_kg, distance_miles, duration_hours)
        elif command == "running":
            calories_burned = calc_running(weight_kg, distance_km)
        else:  # If the user isn't biking, and they aren't running, they must be swimming.
            calories_burned = calc_swimming(weight_kg, duration_hours)

        print_stat("Calories burned", calories_burned)
        # Use a nested list to keep track of the exercises *and* the calories burned.
        exercises.append([command, calories_burned])

    if len(exercises) > 0:
        total_calories_burned = 0
        print("\nCalories burned per exercise:")
        for index in range(len(exercises)):
            label = str(index + 1) + ". " + exercises[index][0]
            print_calories_bar(label, exercises[index][1])
            # Accumulate the calories burned from each exercise to get the total calories burned.
            total_calories_burned += exercises[index][1]
        print("\nTotal:", round(total_calories_burned), "calories")
    elif len(exercises) == 0:
        print("\nNo exercises recorded.")


if __name__ == "__main__":
    main()
