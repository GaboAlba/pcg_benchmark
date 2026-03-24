import pcg_benchmark
import json

def __main__():
    create_environments()
    init_pcg_contents()
    init_contents()
    parse_results()

def convert_to_int_array(array:list[list[str]]) -> list[list[int]]:
    int_array = []
    for row in array:
        int_row = [int(value) for value in row]
        int_array.append(int_row)
    return int_array

def create_environments():
    global binary_v0_env, binary_large_v0_env, binary_wide_v0_env
    global ddave_v0_env, ddave_complex_v0_env, ddave_large_v0_env
    global loderunner_v0_env, loderunner_gold_v0_env, loderunner_enemies_v0_env
    global mdungeons_v0_env, mdungeons_large_v0_env, mdungeons_enemies_v0_env
    global sokoban_v0_env, sokoban_large_v0_env, sokoban_complex_v0_env
    global smbtile_v0_env, smbtile_medium_v0_env, smbtile_small_v0_env
    global zelda_v0_env, zelda_enemies_v0_env, zelda_large_v0_env

    binary_v0_env = pcg_benchmark.make("binary-v0")
    binary_large_v0_env = pcg_benchmark.make("binary-large-v0")
    binary_wide_v0_env = pcg_benchmark.make("binary-wide-v0")
    ddave_v0_env = pcg_benchmark.make("ddave-v0")
    ddave_complex_v0_env = pcg_benchmark.make("ddave-complex-v0")
    ddave_large_v0_env = pcg_benchmark.make("ddave-large-v0")
    loderunner_v0_env = pcg_benchmark.make("loderunner-v0")
    loderunner_gold_v0_env = pcg_benchmark.make("loderunner-gold-v0")
    loderunner_enemies_v0_env = pcg_benchmark.make("loderunner-enemies-v0")
    mdungeons_v0_env = pcg_benchmark.make("mdungeons-v0")
    mdungeons_large_v0_env = pcg_benchmark.make("mdungeons-large-v0")
    mdungeons_enemies_v0_env = pcg_benchmark.make("mdungeons-enemies-v0")
    sokoban_v0_env = pcg_benchmark.make("sokoban-v0")
    sokoban_large_v0_env = pcg_benchmark.make("sokoban-large-v0")
    sokoban_complex_v0_env = pcg_benchmark.make("sokoban-complex-v0")
    smbtile_v0_env = pcg_benchmark.make("mario-v0")
    smbtile_medium_v0_env = pcg_benchmark.make("mario-medium-v0")
    smbtile_small_v0_env = pcg_benchmark.make("mario-small-v0")
    zelda_v0_env = pcg_benchmark.make("zelda-v0")
    zelda_enemies_v0_env = pcg_benchmark.make("zelda-enemies-v0")
    zelda_large_v0_env = pcg_benchmark.make("zelda-large-v0")

def init_contents():
    global binary_v0_content, binary_large_v0_content, binary_wide_v0_content
    global ddave_v0_content, ddave_complex_v0_content, ddave_large_v0_content
    global loderunner_v0_content, loderunner_gold_v0_content, loderunner_enemies_v0_content
    global mdungeons_v0_content, mdungeons_large_v0_content, mdungeons_enemies_v0_content
    global sokoban_v0_content, sokoban_large_v0_content, sokoban_complex_v0_content
    global smbtile_v0_content, smbtile_medium_v0_content, smbtile_small_v0_content
    global zelda_v0_content, zelda_enemies_v0_content, zelda_large_v0_content

    binary_v0_content = []
    binary_large_v0_content = []
    binary_wide_v0_content = []
    ddave_v0_content = []
    ddave_complex_v0_content = []
    ddave_large_v0_content = []
    loderunner_v0_content = []
    loderunner_gold_v0_content = []
    loderunner_enemies_v0_content = []
    mdungeons_v0_content = []
    mdungeons_large_v0_content = []
    mdungeons_enemies_v0_content = []
    sokoban_v0_content = []
    sokoban_large_v0_content = []
    sokoban_complex_v0_content = []
    smbtile_v0_content = []
    smbtile_medium_v0_content = []
    smbtile_small_v0_content = []
    zelda_v0_content = []
    zelda_enemies_v0_content = []
    zelda_large_v0_content = []

def init_pcg_contents():
    global binary_v0_pcg_contents, binary_v0_pcg_controls
    binary_v0_pcg_contents = [binary_v0_env.content_space.sample() for _ in range(len(binary_v0_content))]
    binary_v0_pcg_controls = binary_v0_env.control_space.sample()

    global binary_large_v0_pcg_contents, binary_large_v0_pcg_controls
    binary_large_v0_pcg_contents = [binary_large_v0_env.content_space.sample() for _ in range(len(binary_large_v0_content))]
    binary_large_v0_pcg_controls = binary_large_v0_env.control_space.sample()

    global binary_wide_v0_pcg_contents, binary_wide_v0_pcg_controls
    binary_wide_v0_pcg_contents = [binary_wide_v0_env.content_space.sample() for _ in range(len(binary_wide_v0_content))]
    binary_wide_v0_pcg_controls = binary_wide_v0_env.control_space.sample()

    global ddave_v0_pcg_contents, ddave_v0_pcg_controls
    ddave_v0_pcg_contents = [ddave_v0_env.content_space.sample() for _ in range(len(ddave_v0_content))]
    ddave_v0_pcg_controls = ddave_v0_env.control_space.sample()

    global ddave_complex_v0_pcg_contents, ddave_complex_v0_pcg_controls
    ddave_complex_v0_pcg_contents = [ddave_complex_v0_env.content_space.sample() for _ in range(len(ddave_complex_v0_content))]
    ddave_complex_v0_pcg_controls = ddave_complex_v0_env.control_space.sample()

    global ddave_large_v0_pcg_contents, ddave_large_v0_pcg_controls
    ddave_large_v0_pcg_contents = [ddave_large_v0_env.content_space.sample() for _ in range(len(ddave_large_v0_content))]
    ddave_large_v0_pcg_controls = ddave_large_v0_env.control_space.sample()

    global loderunner_v0_pcg_contents, loderunner_v0_pcg_controls
    loderunner_v0_pcg_contents = [loderunner_v0_env.content_space.sample() for _ in range(len(loderunner_v0_content))]
    loderunner_v0_pcg_controls = loderunner_v0_env.control_space.sample()

    global loderunner_gold_v0_pcg_contents, loderunner_gold_v0_pcg_controls
    loderunner_gold_v0_pcg_contents = [loderunner_gold_v0_env.content_space.sample() for _ in range(len(loderunner_gold_v0_content))]
    loderunner_gold_v0_pcg_controls = loderunner_gold_v0_env.control_space.sample()

    global loderunner_enemies_v0_pcg_contents, loderunner_enemies_v0_pcg_controls
    loderunner_enemies_v0_pcg_contents = [loderunner_enemies_v0_env.content_space.sample() for _ in range(len(loderunner_enemies_v0_content))]
    loderunner_enemies_v0_pcg_controls = loderunner_enemies_v0_env.control_space.sample()

    global mdungeons_v0_pcg_contents, mdungeons_v0_pcg_controls
    mdungeons_v0_pcg_contents = [mdungeons_v0_env.content_space.sample() for _ in range(len(mdungeons_v0_content))]
    mdungeons_v0_pcg_controls = mdungeons_v0_env.control_space.sample()

    global mdungeons_large_v0_pcg_contents, mdungeons_large_v0_pcg_controls
    mdungeons_large_v0_pcg_contents = [mdungeons_large_v0_env.content_space.sample() for _ in range(len(mdungeons_large_v0_content))]
    mdungeons_large_v0_pcg_controls = mdungeons_large_v0_env.control_space.sample()

    global mdungeons_enemies_v0_pcg_contents, mdungeons_enemies_v0_pcg_controls
    mdungeons_enemies_v0_pcg_contents = [mdungeons_enemies_v0_env.content_space.sample() for _ in range(len(mdungeons_enemies_v0_content))]
    mdungeons_enemies_v0_pcg_controls = mdungeons_enemies_v0_env.control_space.sample()

    global sokoban_v0_pcg_contents, sokoban_v0_pcg_controls
    sokoban_v0_pcg_contents = [sokoban_v0_env.content_space.sample() for _ in range(len(sokoban_v0_content))]
    sokoban_v0_pcg_controls = sokoban_v0_env.control_space.sample()

    global sokoban_large_v0_pcg_contents, sokoban_large_v0_pcg_controls
    sokoban_large_v0_pcg_contents = [sokoban_large_v0_env.content_space.sample() for _ in range(len(sokoban_large_v0_content))]
    sokoban_large_v0_pcg_controls = sokoban_large_v0_env.control_space.sample()

    global sokoban_complex_v0_pcg_contents, sokoban_complex_v0_pcg_controls
    sokoban_complex_v0_pcg_contents = [sokoban_complex_v0_env.content_space.sample() for _ in range(len(sokoban_complex_v0_content))]
    sokoban_complex_v0_pcg_controls = sokoban_complex_v0_env.control_space.sample()

    global smbtile_v0_pcg_contents, smbtile_v0_pcg_controls
    smbtile_v0_pcg_contents = [smbtile_v0_env.content_space.sample() for _ in range(len(smbtile_v0_content))]
    smbtile_v0_pcg_controls = smbtile_v0_env.control_space.sample()

    global smbtile_medium_v0_pcg_contents, smbtile_medium_v0_pcg_controls
    smbtile_medium_v0_pcg_contents = [smbtile_medium_v0_env.content_space.sample() for _ in range(len(smbtile_medium_v0_content))]
    smbtile_medium_v0_pcg_controls = smbtile_medium_v0_env.control_space.sample()

    global smbtile_small_v0_pcg_contents, smbtile_small_v0_pcg_controls
    smbtile_small_v0_pcg_contents = [smbtile_small_v0_env.content_space.sample() for _ in range(len(smbtile_small_v0_content))]
    smbtile_small_v0_pcg_controls = smbtile_small_v0_env.control_space.sample()

    global zelda_v0_pcg_contents, zelda_v0_pcg_controls
    zelda_v0_pcg_contents = [zelda_v0_env.content_space.sample() for _ in range(len(zelda_v0_content))]
    zelda_v0_pcg_controls = zelda_v0_env.control_space.sample()

    global zelda_enemies_v0_pcg_contents, zelda_enemies_v0_pcg_controls
    zelda_enemies_v0_pcg_contents = [zelda_enemies_v0_env.content_space.sample() for _ in range(len(zelda_enemies_v0_content))]
    zelda_enemies_v0_pcg_controls = zelda_enemies_v0_env.control_space.sample()

    global zelda_large_v0_pcg_contents, zelda_large_v0_pcg_controls
    zelda_large_v0_pcg_contents = [zelda_large_v0_env.content_space.sample() for _ in range(len(zelda_large_v0_content))]
    zelda_large_v0_pcg_controls = zelda_large_v0_env.control_space.sample()

def parse_results() -> None:
    # Constant strings
    BINARY_V0_CONTENT = "binary-v0"
    BINARY_LARGE_V0_CONTENT = "binary-large-v0"
    BINARY_WIDE_V0_CONTENT = "binary-wide-v0"
    DDAVE_V0_CONTENT = "ddave-v0"
    DDAVE_COMPLEX_V0_CONTENT = "ddave-complex-v0"
    DDAVE_LARGE_V0_CONTENT = "ddave-large-v0"
    LODERUNNER_V0_CONTENT = "loderunner-v0"
    LODERUNNER_GOLD_V0_CONTENT = "loderunner-gold-v0"
    LODERUNNER_ENEMIES_V0_CONTENT = "loderunner-enemies-v0"
    MDUNGEONS_V0_CONTENT = "mdungeons-v0"
    MDUNGEONS_LARGE_V0_CONTENT = "mdungeons-large-v0"
    MDUNGEONS_ENEMIES_V0_CONTENT = "mdungeons-enemies-v0"
    SOKOBAN_V0_CONTENT = "sokoban-v0"
    SOKOBAN_LARGE_V0_CONTENT = "sokoban-large-v0"
    SOKOBAN_COMPLEX_V0_CONTENT = "sokoban-complex-v0"
    SMBTILE_V0_CONTENT = "mario-v0"
    SMBTILE_MEDIUM_V0_CONTENT = "mario-medium-v0"
    SMBTILE_SMALL_V0_CONTENT = "mario-small-v0"
    ZELDA_V0_CONTENT = "zelda-v0"
    ZELDA_ENEMIES_V0_CONTENT = "zelda-enemies-v0"
    ZELDA_LARGE_V0_CONTENT = "zelda-large-v0"

    file_path = ".\pcg_results.json"
    with open(file_path, "r") as f:
        data = json.load(f)
        for result in data["Output"]:
            try:
              data["Output"][result] = convert_to_int_array(data["Output"][result])
            except (ValueError, TypeError):
                print(f"Error converting {result} to integer array")
                continue

            tempResult = result[:len(result) - 2]

            if (tempResult == BINARY_V0_CONTENT):
                binary_v0_content.append(data["Output"][result])
            elif (tempResult == BINARY_LARGE_V0_CONTENT):
                binary_large_v0_content.append(data["Output"][result])
            elif (tempResult == BINARY_WIDE_V0_CONTENT):
                binary_wide_v0_content.append(data["Output"][result])
            elif (tempResult == DDAVE_V0_CONTENT):
                ddave_v0_content.append(data["Output"][result])
            elif (tempResult == DDAVE_COMPLEX_V0_CONTENT):
                ddave_complex_v0_content.append(data["Output"][result])
            elif (tempResult == DDAVE_LARGE_V0_CONTENT):
                ddave_large_v0_content.append(data["Output"][result])
            elif (tempResult == LODERUNNER_V0_CONTENT):
                loderunner_v0_content.append(data["Output"][result])
            elif (tempResult == LODERUNNER_GOLD_V0_CONTENT):
                loderunner_gold_v0_content.append(data["Output"][result])
            elif (tempResult == LODERUNNER_ENEMIES_V0_CONTENT):
                loderunner_enemies_v0_content.append(data["Output"][result])
            elif (tempResult == MDUNGEONS_V0_CONTENT):
                mdungeons_v0_content.append(data["Output"][result])
            elif (tempResult == MDUNGEONS_LARGE_V0_CONTENT):
                mdungeons_large_v0_content.append(data["Output"][result])
            elif (tempResult == MDUNGEONS_ENEMIES_V0_CONTENT):
                mdungeons_enemies_v0_content.append(data["Output"][result])
            elif (tempResult == SOKOBAN_V0_CONTENT):
                sokoban_v0_content.append(data["Output"][result])
            elif (tempResult == SOKOBAN_LARGE_V0_CONTENT):
                sokoban_large_v0_content.append(data["Output"][result])
            elif (tempResult == SOKOBAN_COMPLEX_V0_CONTENT):
                sokoban_complex_v0_content.append(data["Output"][result])
            elif (tempResult == SMBTILE_V0_CONTENT):
                smbtile_v0_content.append(data["Output"][result])
            elif (tempResult == SMBTILE_MEDIUM_V0_CONTENT):
                smbtile_medium_v0_content.append(data["Output"][result])
            elif (tempResult == SMBTILE_SMALL_V0_CONTENT):
                smbtile_small_v0_content.append(data["Output"][result])
            elif (tempResult == ZELDA_V0_CONTENT):
                zelda_v0_content.append(data["Output"][result])
            elif (tempResult == ZELDA_ENEMIES_V0_CONTENT):
                zelda_enemies_v0_content.append(data["Output"][result])
            elif (tempResult == ZELDA_LARGE_V0_CONTENT):
                zelda_large_v0_content.append(data["Output"][result])
            else:
                print("Unknown content key: " + result)

            print("Parsed content for " + result + ": " + str(data["Output"][result]))

def evaluate():
    pass

if __name__ == "__main__":
    __main__()