import pcg_benchmark
import json

def __main__():
    create_environments()
    init_contents()
    parse_results()
    init_pcg_contents()
    evaluate()
    save_eval_results()
    render_eval_results()

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
    smbtile_v0_env = pcg_benchmark.make("smbtile-v0")
    smbtile_medium_v0_env = pcg_benchmark.make("smbtile-medium-v0")
    smbtile_small_v0_env = pcg_benchmark.make("smbtile-small-v0")
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
            tempData = data["Output"][result]
            
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
    global binary_v0_quality, binary_v0_diversity, binary_v0_controlability, binary_v0_details, binary_v0_infos
    global binary_v0_pcg_quality, binary_v0_pcg_diversity, binary_v0_pcg_controlability, binary_v0_pcg_details, binary_v0_pcg_infos
    binary_v0_quality, binary_v0_diversity, binary_v0_controlability, binary_v0_details, binary_v0_infos = binary_v0_env.evaluate(binary_v0_content, binary_v0_pcg_controls)
    binary_v0_pcg_quality, binary_v0_pcg_diversity, binary_v0_pcg_controlability, binary_v0_pcg_details, binary_v0_pcg_infos = binary_v0_env.evaluate(binary_v0_pcg_contents, binary_v0_pcg_controls)

    global binary_large_v0_quality, binary_large_v0_diversity, binary_large_v0_controlability, binary_large_v0_details, binary_large_v0_infos
    global binary_large_v0_pcg_quality, binary_large_v0_pcg_diversity, binary_large_v0_pcg_controlability, binary_large_v0_pcg_details, binary_large_v0_pcg_infos
    binary_large_v0_quality, binary_large_v0_diversity, binary_large_v0_controlability, binary_large_v0_details, binary_large_v0_infos = binary_large_v0_env.evaluate(binary_large_v0_content, binary_large_v0_pcg_controls)
    binary_large_v0_pcg_quality, binary_large_v0_pcg_diversity, binary_large_v0_pcg_controlability, binary_large_v0_pcg_details, binary_large_v0_pcg_infos = binary_large_v0_env.evaluate(binary_large_v0_pcg_contents, binary_large_v0_pcg_controls)

    global binary_wide_v0_quality, binary_wide_v0_diversity, binary_wide_v0_controlability, binary_wide_v0_details, binary_wide_v0_infos
    global binary_wide_v0_pcg_quality, binary_wide_v0_pcg_diversity, binary_wide_v0_pcg_controlability, binary_wide_v0_pcg_details, binary_wide_v0_pcg_infos
    binary_wide_v0_quality, binary_wide_v0_diversity, binary_wide_v0_controlability, binary_wide_v0_details, binary_wide_v0_infos = binary_wide_v0_env.evaluate(binary_wide_v0_content, binary_wide_v0_pcg_controls)
    binary_wide_v0_pcg_quality, binary_wide_v0_pcg_diversity, binary_wide_v0_pcg_controlability, binary_wide_v0_pcg_details, binary_wide_v0_pcg_infos = binary_wide_v0_env.evaluate(binary_wide_v0_pcg_contents, binary_wide_v0_pcg_controls)

    global ddave_v0_quality, ddave_v0_diversity, ddave_v0_controlability, ddave_v0_details, ddave_v0_infos
    global ddave_v0_pcg_quality, ddave_v0_pcg_diversity, ddave_v0_pcg_controlability, ddave_v0_pcg_details, ddave_v0_pcg_infos
    ddave_v0_quality, ddave_v0_diversity, ddave_v0_controlability, ddave_v0_details, ddave_v0_infos = ddave_v0_env.evaluate(ddave_v0_content, ddave_v0_pcg_controls)
    ddave_v0_pcg_quality, ddave_v0_pcg_diversity, ddave_v0_pcg_controlability, ddave_v0_pcg_details, ddave_v0_pcg_infos = ddave_v0_env.evaluate(ddave_v0_pcg_contents, ddave_v0_pcg_controls)

    global ddave_complex_v0_quality, ddave_complex_v0_diversity, ddave_complex_v0_controlability, ddave_complex_v0_details, ddave_complex_v0_infos
    global ddave_complex_v0_pcg_quality, ddave_complex_v0_pcg_diversity, ddave_complex_v0_pcg_controlability, ddave_complex_v0_pcg_details, ddave_complex_v0_pcg_infos
    ddave_complex_v0_quality, ddave_complex_v0_diversity, ddave_complex_v0_controlability, ddave_complex_v0_details, ddave_complex_v0_infos = ddave_complex_v0_env.evaluate(ddave_complex_v0_content, ddave_complex_v0_pcg_controls)
    ddave_complex_v0_pcg_quality, ddave_complex_v0_pcg_diversity, ddave_complex_v0_pcg_controlability, ddave_complex_v0_pcg_details, ddave_complex_v0_pcg_infos = ddave_complex_v0_env.evaluate(ddave_complex_v0_pcg_contents, ddave_complex_v0_pcg_controls)

    global ddave_large_v0_quality, ddave_large_v0_diversity, ddave_large_v0_controlability, ddave_large_v0_details, ddave_large_v0_infos
    global ddave_large_v0_pcg_quality, ddave_large_v0_pcg_diversity, ddave_large_v0_pcg_controlability, ddave_large_v0_pcg_details, ddave_large_v0_pcg_infos
    ddave_large_v0_quality, ddave_large_v0_diversity, ddave_large_v0_controlability, ddave_large_v0_details, ddave_large_v0_infos = ddave_large_v0_env.evaluate(ddave_large_v0_content, ddave_large_v0_pcg_controls)
    ddave_large_v0_pcg_quality, ddave_large_v0_pcg_diversity, ddave_large_v0_pcg_controlability, ddave_large_v0_pcg_details, ddave_large_v0_pcg_infos = ddave_large_v0_env.evaluate(ddave_large_v0_pcg_contents, ddave_large_v0_pcg_controls)

    global loderunner_v0_quality, loderunner_v0_diversity, loderunner_v0_controlability, loderunner_v0_details, loderunner_v0_infos
    global loderunner_v0_pcg_quality, loderunner_v0_pcg_diversity, loderunner_v0_pcg_controlability, loderunner_v0_pcg_details, loderunner_v0_pcg_infos
    loderunner_v0_quality, loderunner_v0_diversity, loderunner_v0_controlability, loderunner_v0_details, loderunner_v0_infos = loderunner_v0_env.evaluate(loderunner_v0_content, loderunner_v0_pcg_controls)
    loderunner_v0_pcg_quality, loderunner_v0_pcg_diversity, loderunner_v0_pcg_controlability, loderunner_v0_pcg_details, loderunner_v0_pcg_infos = loderunner_v0_env.evaluate(loderunner_v0_pcg_contents, loderunner_v0_pcg_controls)

    global loderunner_gold_v0_quality, loderunner_gold_v0_diversity, loderunner_gold_v0_controlability, loderunner_gold_v0_details, loderunner_gold_v0_infos
    global loderunner_gold_v0_pcg_quality, loderunner_gold_v0_pcg_diversity, loderunner_gold_v0_pcg_controlability, loderunner_gold_v0_pcg_details, loderunner_gold_v0_pcg_infos
    loderunner_gold_v0_quality, loderunner_gold_v0_diversity, loderunner_gold_v0_controlability, loderunner_gold_v0_details, loderunner_gold_v0_infos = loderunner_gold_v0_env.evaluate(loderunner_gold_v0_content, loderunner_gold_v0_pcg_controls)
    loderunner_gold_v0_pcg_quality, loderunner_gold_v0_pcg_diversity, loderunner_gold_v0_pcg_controlability, loderunner_gold_v0_pcg_details, loderunner_gold_v0_pcg_infos = loderunner_gold_v0_env.evaluate(loderunner_gold_v0_pcg_contents, loderunner_gold_v0_pcg_controls)

    global loderunner_enemies_v0_quality, loderunner_enemies_v0_diversity, loderunner_enemies_v0_controlability, loderunner_enemies_v0_details, loderunner_enemies_v0_infos
    global loderunner_enemies_v0_pcg_quality, loderunner_enemies_v0_pcg_diversity, loderunner_enemies_v0_pcg_controlability, loderunner_enemies_v0_pcg_details, loderunner_enemies_v0_pcg_infos
    loderunner_enemies_v0_quality, loderunner_enemies_v0_diversity, loderunner_enemies_v0_controlability, loderunner_enemies_v0_details, loderunner_enemies_v0_infos = loderunner_enemies_v0_env.evaluate(loderunner_enemies_v0_content, loderunner_enemies_v0_pcg_controls)
    loderunner_enemies_v0_pcg_quality, loderunner_enemies_v0_pcg_diversity, loderunner_enemies_v0_pcg_controlability, loderunner_enemies_v0_pcg_details, loderunner_enemies_v0_pcg_infos = loderunner_enemies_v0_env.evaluate(loderunner_enemies_v0_pcg_contents, loderunner_enemies_v0_pcg_controls)

    global mdungeons_v0_quality, mdungeons_v0_diversity, mdungeons_v0_controlability, mdungeons_v0_details, mdungeons_v0_infos
    global mdungeons_v0_pcg_quality, mdungeons_v0_pcg_diversity, mdungeons_v0_pcg_controlability, mdungeons_v0_pcg_details, mdungeons_v0_pcg_infos
    mdungeons_v0_quality, mdungeons_v0_diversity, mdungeons_v0_controlability, mdungeons_v0_details, mdungeons_v0_infos = mdungeons_v0_env.evaluate(mdungeons_v0_content, mdungeons_v0_pcg_controls)
    mdungeons_v0_pcg_quality, mdungeons_v0_pcg_diversity, mdungeons_v0_pcg_controlability, mdungeons_v0_pcg_details, mdungeons_v0_pcg_infos = mdungeons_v0_env.evaluate(mdungeons_v0_pcg_contents, mdungeons_v0_pcg_controls)

    global mdungeons_large_v0_quality, mdungeons_large_v0_diversity, mdungeons_large_v0_controlability, mdungeons_large_v0_details, mdungeons_large_v0_infos
    global mdungeons_large_v0_pcg_quality, mdungeons_large_v0_pcg_diversity, mdungeons_large_v0_pcg_controlability, mdungeons_large_v0_pcg_details, mdungeons_large_v0_pcg_infos
    mdungeons_large_v0_quality, mdungeons_large_v0_diversity, mdungeons_large_v0_controlability, mdungeons_large_v0_details, mdungeons_large_v0_infos = mdungeons_large_v0_env.evaluate(mdungeons_large_v0_content, mdungeons_large_v0_pcg_controls)
    mdungeons_large_v0_pcg_quality, mdungeons_large_v0_pcg_diversity, mdungeons_large_v0_pcg_controlability, mdungeons_large_v0_pcg_details, mdungeons_large_v0_pcg_infos = mdungeons_large_v0_env.evaluate(mdungeons_large_v0_pcg_contents, mdungeons_large_v0_pcg_controls)

    global mdungeons_enemies_v0_quality, mdungeons_enemies_v0_diversity, mdungeons_enemies_v0_controlability, mdungeons_enemies_v0_details, mdungeons_enemies_v0_infos
    global mdungeons_enemies_v0_pcg_quality, mdungeons_enemies_v0_pcg_diversity, mdungeons_enemies_v0_pcg_controlability, mdungeons_enemies_v0_pcg_details, mdungeons_enemies_v0_pcg_infos
    mdungeons_enemies_v0_quality, mdungeons_enemies_v0_diversity, mdungeons_enemies_v0_controlability, mdungeons_enemies_v0_details, mdungeons_enemies_v0_infos = mdungeons_enemies_v0_env.evaluate(mdungeons_enemies_v0_content, mdungeons_enemies_v0_pcg_controls)
    mdungeons_enemies_v0_pcg_quality, mdungeons_enemies_v0_pcg_diversity, mdungeons_enemies_v0_pcg_controlability, mdungeons_enemies_v0_pcg_details, mdungeons_enemies_v0_pcg_infos = mdungeons_enemies_v0_env.evaluate(mdungeons_enemies_v0_pcg_contents, mdungeons_enemies_v0_pcg_controls)

    global sokoban_v0_quality, sokoban_v0_diversity, sokoban_v0_controlability, sokoban_v0_details, sokoban_v0_infos
    global sokoban_v0_pcg_quality, sokoban_v0_pcg_diversity, sokoban_v0_pcg_controlability, sokoban_v0_pcg_details, sokoban_v0_pcg_infos
    sokoban_v0_quality, sokoban_v0_diversity, sokoban_v0_controlability, sokoban_v0_details, sokoban_v0_infos = sokoban_v0_env.evaluate(sokoban_v0_content, sokoban_v0_pcg_controls)
    sokoban_v0_pcg_quality, sokoban_v0_pcg_diversity, sokoban_v0_pcg_controlability, sokoban_v0_pcg_details, sokoban_v0_pcg_infos = sokoban_v0_env.evaluate(sokoban_v0_pcg_contents, sokoban_v0_pcg_controls)

    global sokoban_large_v0_quality, sokoban_large_v0_diversity, sokoban_large_v0_controlability, sokoban_large_v0_details, sokoban_large_v0_infos
    global sokoban_large_v0_pcg_quality, sokoban_large_v0_pcg_diversity, sokoban_large_v0_pcg_controlability, sokoban_large_v0_pcg_details, sokoban_large_v0_pcg_infos
    sokoban_large_v0_quality, sokoban_large_v0_diversity, sokoban_large_v0_controlability, sokoban_large_v0_details, sokoban_large_v0_infos = sokoban_large_v0_env.evaluate(sokoban_large_v0_content, sokoban_large_v0_pcg_controls)
    sokoban_large_v0_pcg_quality, sokoban_large_v0_pcg_diversity, sokoban_large_v0_pcg_controlability, sokoban_large_v0_pcg_details, sokoban_large_v0_pcg_infos = sokoban_large_v0_env.evaluate(sokoban_large_v0_pcg_contents, sokoban_large_v0_pcg_controls)

    global sokoban_complex_v0_quality, sokoban_complex_v0_diversity, sokoban_complex_v0_controlability, sokoban_complex_v0_details, sokoban_complex_v0_infos
    global sokoban_complex_v0_pcg_quality, sokoban_complex_v0_pcg_diversity, sokoban_complex_v0_pcg_controlability, sokoban_complex_v0_pcg_details, sokoban_complex_v0_pcg_infos
    sokoban_complex_v0_quality, sokoban_complex_v0_diversity, sokoban_complex_v0_controlability, sokoban_complex_v0_details, sokoban_complex_v0_infos = sokoban_complex_v0_env.evaluate(sokoban_complex_v0_content, sokoban_complex_v0_pcg_controls)
    sokoban_complex_v0_pcg_quality, sokoban_complex_v0_pcg_diversity, sokoban_complex_v0_pcg_controlability, sokoban_complex_v0_pcg_details, sokoban_complex_v0_pcg_infos = sokoban_complex_v0_env.evaluate(sokoban_complex_v0_pcg_contents, sokoban_complex_v0_pcg_controls)

    global smbtile_v0_quality, smbtile_v0_diversity, smbtile_v0_controlability, smbtile_v0_details, smbtile_v0_infos
    global smbtile_v0_pcg_quality, smbtile_v0_pcg_diversity, smbtile_v0_pcg_controlability, smbtile_v0_pcg_details, smbtile_v0_pcg_infos
    smbtile_v0_quality, smbtile_v0_diversity, smbtile_v0_controlability, smbtile_v0_details, smbtile_v0_infos = smbtile_v0_env.evaluate(smbtile_v0_content, smbtile_v0_pcg_controls)
    smbtile_v0_pcg_quality, smbtile_v0_pcg_diversity, smbtile_v0_pcg_controlability, smbtile_v0_pcg_details, smbtile_v0_pcg_infos = smbtile_v0_env.evaluate(smbtile_v0_pcg_contents, smbtile_v0_pcg_controls)

    global smbtile_medium_v0_quality, smbtile_medium_v0_diversity, smbtile_medium_v0_controlability, smbtile_medium_v0_details, smbtile_medium_v0_infos
    global smbtile_medium_v0_pcg_quality, smbtile_medium_v0_pcg_diversity, smbtile_medium_v0_pcg_controlability, smbtile_medium_v0_pcg_details, smbtile_medium_v0_pcg_infos
    smbtile_medium_v0_quality, smbtile_medium_v0_diversity, smbtile_medium_v0_controlability, smbtile_medium_v0_details, smbtile_medium_v0_infos = smbtile_medium_v0_env.evaluate(smbtile_medium_v0_content, smbtile_medium_v0_pcg_controls)
    smbtile_medium_v0_pcg_quality, smbtile_medium_v0_pcg_diversity, smbtile_medium_v0_pcg_controlability, smbtile_medium_v0_pcg_details, smbtile_medium_v0_pcg_infos = smbtile_medium_v0_env.evaluate(smbtile_medium_v0_pcg_contents, smbtile_medium_v0_pcg_controls)

    global smbtile_small_v0_quality, smbtile_small_v0_diversity, smbtile_small_v0_controlability, smbtile_small_v0_details, smbtile_small_v0_infos
    global smbtile_small_v0_pcg_quality, smbtile_small_v0_pcg_diversity, smbtile_small_v0_pcg_controlability, smbtile_small_v0_pcg_details, smbtile_small_v0_pcg_infos
    smbtile_small_v0_quality, smbtile_small_v0_diversity, smbtile_small_v0_controlability, smbtile_small_v0_details, smbtile_small_v0_infos = smbtile_small_v0_env.evaluate(smbtile_small_v0_content, smbtile_small_v0_pcg_controls)
    smbtile_small_v0_pcg_quality, smbtile_small_v0_pcg_diversity, smbtile_small_v0_pcg_controlability, smbtile_small_v0_pcg_details, smbtile_small_v0_pcg_infos = smbtile_small_v0_env.evaluate(smbtile_small_v0_pcg_contents, smbtile_small_v0_pcg_controls)

    global zelda_v0_quality, zelda_v0_diversity, zelda_v0_controlability, zelda_v0_details, zelda_v0_infos
    global zelda_v0_pcg_quality, zelda_v0_pcg_diversity, zelda_v0_pcg_controlability, zelda_v0_pcg_details, zelda_v0_pcg_infos
    zelda_v0_quality, zelda_v0_diversity, zelda_v0_controlability, zelda_v0_details, zelda_v0_infos = zelda_v0_env.evaluate(zelda_v0_content, zelda_v0_pcg_controls)
    zelda_v0_pcg_quality, zelda_v0_pcg_diversity, zelda_v0_pcg_controlability, zelda_v0_pcg_details, zelda_v0_pcg_infos = zelda_v0_env.evaluate(zelda_v0_pcg_contents, zelda_v0_pcg_controls)

    global zelda_enemies_v0_quality, zelda_enemies_v0_diversity, zelda_enemies_v0_controlability, zelda_enemies_v0_details, zelda_enemies_v0_infos
    global zelda_enemies_v0_pcg_quality, zelda_enemies_v0_pcg_diversity, zelda_enemies_v0_pcg_controlability, zelda_enemies_v0_pcg_details, zelda_enemies_v0_pcg_infos
    zelda_enemies_v0_quality, zelda_enemies_v0_diversity, zelda_enemies_v0_controlability, zelda_enemies_v0_details, zelda_enemies_v0_infos = zelda_enemies_v0_env.evaluate(zelda_enemies_v0_content, zelda_enemies_v0_pcg_controls)
    zelda_enemies_v0_pcg_quality, zelda_enemies_v0_pcg_diversity, zelda_enemies_v0_pcg_controlability, zelda_enemies_v0_pcg_details, zelda_enemies_v0_pcg_infos = zelda_enemies_v0_env.evaluate(zelda_enemies_v0_pcg_contents, zelda_enemies_v0_pcg_controls)

    global zelda_large_v0_quality, zelda_large_v0_diversity, zelda_large_v0_controlability, zelda_large_v0_details, zelda_large_v0_infos
    global zelda_large_v0_pcg_quality, zelda_large_v0_pcg_diversity, zelda_large_v0_pcg_controlability, zelda_large_v0_pcg_details, zelda_large_v0_pcg_infos
    zelda_large_v0_quality, zelda_large_v0_diversity, zelda_large_v0_controlability, zelda_large_v0_details, zelda_large_v0_infos = zelda_large_v0_env.evaluate(zelda_large_v0_content, zelda_large_v0_pcg_controls)
    zelda_large_v0_pcg_quality, zelda_large_v0_pcg_diversity, zelda_large_v0_pcg_controlability, zelda_large_v0_pcg_details, zelda_large_v0_pcg_infos = zelda_large_v0_env.evaluate(zelda_large_v0_pcg_contents, zelda_large_v0_pcg_controls)

def save_eval_results():
    eval_results = {
        "binary_v0": {
            "quality": binary_v0_quality,
            "diversity": binary_v0_diversity,
            "controlability": binary_v0_controlability,
            "details": binary_v0_details,
            "infos": binary_v0_infos,
            "pcg_quality": binary_v0_pcg_quality,
            "pcg_diversity": binary_v0_pcg_diversity,
            "pcg_controlability": binary_v0_pcg_controlability,
            "pcg_details": binary_v0_pcg_details,
            "pcg_infos": binary_v0_pcg_infos
        },
        "binary_large_v0": {
            "quality": binary_large_v0_quality,
            "diversity": binary_large_v0_diversity,
            "controlability": binary_large_v0_controlability,
            "details": binary_large_v0_details,
            "infos": binary_large_v0_infos,
            "pcg_quality": binary_large_v0_pcg_quality,
            "pcg_diversity": binary_large_v0_pcg_diversity,
            "pcg_controlability": binary_large_v0_pcg_controlability,
            "pcg_details": binary_large_v0_pcg_details,
            "pcg_infos": binary_large_v0_pcg_infos
        },
        "binary_wide_v0": {
            "quality": binary_wide_v0_quality,
            "diversity": binary_wide_v0_diversity,
            "controlability": binary_wide_v0_controlability,
            "details": binary_wide_v0_details,
            "infos": binary_wide_v0_infos,
            "pcg_quality": binary_wide_v0_pcg_quality,
            "pcg_diversity": binary_wide_v0_pcg_diversity,
            "pcg_controlability": binary_wide_v0_pcg_controlability,
            "pcg_details": binary_wide_v0_pcg_details,
            "pcg_infos": binary_wide_v0_pcg_infos
        },
        "ddave_v0": {
            "quality": ddave_v0_quality,
            "diversity": ddave_v0_diversity,
            "controlability": ddave_v0_controlability,
            "details": ddave_v0_details,
            "infos": ddave_v0_infos,
            "pcg_quality": ddave_v0_pcg_quality,
            "pcg_diversity": ddave_v0_pcg_diversity,
            "pcg_controlability": ddave_v0_pcg_controlability,
            "pcg_details": ddave_v0_pcg_details,
            "pcg_infos": ddave_v0_pcg_infos
        },
        "ddave_complex_v0": {
            "quality": ddave_complex_v0_quality,
            "diversity": ddave_complex_v0_diversity,
            "controlability": ddave_complex_v0_controlability,
            "details": ddave_complex_v0_details,
            "infos": ddave_complex_v0_infos,
            "pcg_quality": ddave_complex_v0_pcg_quality,
            "pcg_diversity": ddave_complex_v0_pcg_diversity,
            "pcg_controlability": ddave_complex_v0_pcg_controlability,
            "pcg_details": ddave_complex_v0_pcg_details,
            "pcg_infos": ddave_complex_v0_pcg_infos
        },
        "ddave_large_v0": {
            "quality": ddave_large_v0_quality,
            "diversity": ddave_large_v0_diversity,
            "controlability": ddave_large_v0_controlability,
            "details": ddave_large_v0_details,
            "infos": ddave_large_v0_infos,
            "pcg_quality": ddave_large_v0_pcg_quality,
            "pcg_diversity": ddave_large_v0_pcg_diversity,
            "pcg_controlability": ddave_large_v0_pcg_controlability,
            "pcg_details": ddave_large_v0_pcg_details,
            "pcg_infos": ddave_large_v0_pcg_infos
        },
        "loderunner_v0": {
            "quality": loderunner_v0_quality,
            "diversity": loderunner_v0_diversity,
            "controlability": loderunner_v0_controlability,
            "details": loderunner_v0_details,
            "infos": loderunner_v0_infos,
            "pcg_quality": loderunner_v0_pcg_quality,
            "pcg_diversity": loderunner_v0_pcg_diversity,
            "pcg_controlability": loderunner_v0_pcg_controlability,
            "pcg_details": loderunner_v0_pcg_details,
            "pcg_infos": loderunner_v0_pcg_infos
        },
        "loderunner_gold_v0": {
            "quality": loderunner_gold_v0_quality,
            "diversity": loderunner_gold_v0_diversity,
            "controlability": loderunner_gold_v0_controlability,
            "details": loderunner_gold_v0_details,
            "infos": loderunner_gold_v0_infos,
            "pcg_quality": loderunner_gold_v0_pcg_quality,
            "pcg_diversity": loderunner_gold_v0_pcg_diversity,
            "pcg_controlability": loderunner_gold_v0_pcg_controlability,
            "pcg_details": loderunner_gold_v0_pcg_details,
            "pcg_infos": loderunner_gold_v0_pcg_infos
        },
        "loderunner_enemies_v0": {
            "quality": loderunner_enemies_v0_quality,
            "diversity": loderunner_enemies_v0_diversity,
            "controlability": loderunner_enemies_v0_controlability,
            "details": loderunner_enemies_v0_details,
            "infos": loderunner_enemies_v0_infos,
            "pcg_quality": loderunner_enemies_v0_pcg_quality,
            "pcg_diversity": loderunner_enemies_v0_pcg_diversity,
            "pcg_controlability": loderunner_enemies_v0_pcg_controlability,
            "pcg_details": loderunner_enemies_v0_pcg_details,
            "pcg_infos": loderunner_enemies_v0_pcg_infos
        },
        "mdungeons_v0": {
            "quality": mdungeons_v0_quality,
            "diversity": mdungeons_v0_diversity,
            "controlability": mdungeons_v0_controlability,
            "details": mdungeons_v0_details,
            "infos": mdungeons_v0_infos,
            "pcg_quality": mdungeons_v0_pcg_quality,
            "pcg_diversity": mdungeons_v0_pcg_diversity,
            "pcg_controlability": mdungeons_v0_pcg_controlability,
            "pcg_details": mdungeons_v0_pcg_details,
            "pcg_infos": mdungeons_v0_pcg_infos
        },
        "mdungeons_large_v0": {
            "quality": mdungeons_large_v0_quality,
            "diversity": mdungeons_large_v0_diversity,
            "controlability": mdungeons_large_v0_controlability,
            "details": mdungeons_large_v0_details,
            "infos": mdungeons_large_v0_infos,
            "pcg_quality": mdungeons_large_v0_pcg_quality,
            "pcg_diversity": mdungeons_large_v0_pcg_diversity,
            "pcg_controlability": mdungeons_large_v0_pcg_controlability,
            "pcg_details": mdungeons_large_v0_pcg_details,
            "pcg_infos": mdungeons_large_v0_pcg_infos
        },
        "mdungeons_enemies_v0": {
            "quality": mdungeons_enemies_v0_quality,
            "diversity": mdungeons_enemies_v0_diversity,
            "controlability": mdungeons_enemies_v0_controlability,
            "details": mdungeons_enemies_v0_details,
            "infos": mdungeons_enemies_v0_infos,
            "pcg_quality": mdungeons_enemies_v0_pcg_quality,
            "pcg_diversity": mdungeons_enemies_v0_pcg_diversity,
            "pcg_controlability": mdungeons_enemies_v0_pcg_controlability,
            "pcg_details": mdungeons_enemies_v0_pcg_details,
            "pcg_infos": mdungeons_enemies_v0_pcg_infos
        },
        "sokoban_v0": {
            "quality": sokoban_v0_quality,
            "diversity": sokoban_v0_diversity,
            "controlability": sokoban_v0_controlability,
            "details": sokoban_v0_details,
            "infos": sokoban_v0_infos,
            "pcg_quality": sokoban_v0_pcg_quality,
            "pcg_diversity": sokoban_v0_pcg_diversity,
            "pcg_controlability": sokoban_v0_pcg_controlability,
            "pcg_details": sokoban_v0_pcg_details,
            "pcg_infos": sokoban_v0_pcg_infos
        },
        "sokoban_large_v0": {
            "quality": sokoban_large_v0_quality,
            "diversity": sokoban_large_v0_diversity,
            "controlability": sokoban_large_v0_controlability,
            "details": sokoban_large_v0_details,
            "infos": sokoban_large_v0_infos,
            "pcg_quality": sokoban_large_v0_pcg_quality,
            "pcg_diversity": sokoban_large_v0_pcg_diversity,
            "pcg_controlability": sokoban_large_v0_pcg_controlability,
            "pcg_details": sokoban_large_v0_pcg_details,
            "pcg_infos": sokoban_large_v0_pcg_infos
        },
        "sokoban_complex_v0": {
            "quality": sokoban_complex_v0_quality,
            "diversity": sokoban_complex_v0_diversity,
            "controlability": sokoban_complex_v0_controlability,
            "details": sokoban_complex_v0_details,
            "infos": sokoban_complex_v0_infos,
            "pcg_quality": sokoban_complex_v0_pcg_quality,
            "pcg_diversity": sokoban_complex_v0_pcg_diversity,
            "pcg_controlability": sokoban_complex_v0_pcg_controlability,
            "pcg_details": sokoban_complex_v0_pcg_details,
            "pcg_infos": sokoban_complex_v0_pcg_infos
        },
        "smbtile_v0": {
            "quality": smbtile_v0_quality,
            "diversity": smbtile_v0_diversity,
            "controlability": smbtile_v0_controlability,
            "details": smbtile_v0_details,
            "infos": smbtile_v0_infos,
            "pcg_quality": smbtile_v0_pcg_quality,
            "pcg_diversity": smbtile_v0_pcg_diversity,
            "pcg_controlability": smbtile_v0_pcg_controlability,
            "pcg_details": smbtile_v0_pcg_details,
            "pcg_infos": smbtile_v0_pcg_infos
        },
        "smbtile_medium_v0": {
            "quality": smbtile_medium_v0_quality,
            "diversity": smbtile_medium_v0_diversity,
            "controlability": smbtile_medium_v0_controlability,
            "details": smbtile_medium_v0_details,
            "infos": smbtile_medium_v0_infos,
            "pcg_quality": smbtile_medium_v0_pcg_quality,
            "pcg_diversity": smbtile_medium_v0_pcg_diversity,
            "pcg_controlability": smbtile_medium_v0_pcg_controlability,
            "pcg_details": smbtile_medium_v0_pcg_details,
            "pcg_infos": smbtile_medium_v0_pcg_infos
        },
        "smbtile_small_v0": {
            "quality": smbtile_small_v0_quality,
            "diversity": smbtile_small_v0_diversity,
            "controlability": smbtile_small_v0_controlability,
            "details": smbtile_small_v0_details,
            "infos": smbtile_small_v0_infos,
            "pcg_quality": smbtile_small_v0_pcg_quality,
            "pcg_diversity": smbtile_small_v0_pcg_diversity,
            "pcg_controlability": smbtile_small_v0_pcg_controlability,
            "pcg_details": smbtile_small_v0_pcg_details,
            "pcg_infos": smbtile_small_v0_pcg_infos
        },
        "zelda_v0": {
            "quality": zelda_v0_quality,
            "diversity": zelda_v0_diversity,
            "controlability": zelda_v0_controlability,
            "details": zelda_v0_details,
            "infos": zelda_v0_infos,
            "pcg_quality": zelda_v0_pcg_quality,
            "pcg_diversity": zelda_v0_pcg_diversity,
            "pcg_controlability": zelda_v0_pcg_controlability,
            "pcg_details": zelda_v0_pcg_details,
            "pcg_infos": zelda_v0_pcg_infos
        },
        "zelda_enemies_v0": {
            "quality": zelda_enemies_v0_quality,
            "diversity": zelda_enemies_v0_diversity,
            "controlability": zelda_enemies_v0_controlability,
            "details": zelda_enemies_v0_details,
            "infos": zelda_enemies_v0_infos,
            "pcg_quality": zelda_enemies_v0_pcg_quality,
            "pcg_diversity": zelda_enemies_v0_pcg_diversity,
            "pcg_controlability": zelda_enemies_v0_pcg_controlability,
            "pcg_details": zelda_enemies_v0_pcg_details,
            "pcg_infos": zelda_enemies_v0_pcg_infos
        },
        "zelda_large_v0": {
            "quality": zelda_large_v0_quality,
            "diversity": zelda_large_v0_diversity,
            "controlability": zelda_large_v0_controlability,
            "details": zelda_large_v0_details,
            "infos": zelda_large_v0_infos,
            "pcg_quality": zelda_large_v0_pcg_quality,
            "pcg_diversity": zelda_large_v0_pcg_diversity,
            "pcg_controlability": zelda_large_v0_pcg_controlability,
            "pcg_details": zelda_large_v0_pcg_details,
            "pcg_infos": zelda_large_v0_pcg_infos
        }
    }

    with open("eval_results.json", "w") as f:
        json.dump(eval_results, f, indent=4)


def render_eval_results():
    binary_v0_imgs = binary_v0_env.render(binary_v0_content)
    binary_large_v0_imgs = binary_large_v0_env.render(binary_large_v0_content)
    binary_wide_v0_imgs = binary_wide_v0_env.render(binary_wide_v0_content)
    ddave_v0_imgs = ddave_v0_env.render(ddave_v0_content)
    ddave_complex_v0_imgs = ddave_complex_v0_env.render(ddave_complex_v0_content)
    ddave_large_v0_imgs = ddave_large_v0_env.render(ddave_large_v0_content)
    loderunner_v0_imgs = loderunner_v0_env.render(loderunner_v0_content)
    loderunner_gold_v0_imgs = loderunner_gold_v0_env.render(loderunner_gold_v0_content)
    loderunner_enemies_v0_imgs = loderunner_enemies_v0_env.render(loderunner_enemies_v0_content)
    mdungeons_v0_imgs = mdungeons_v0_env.render(mdungeons_v0_content)
    mdungeons_large_v0_imgs = mdungeons_large_v0_env.render(mdungeons_large_v0_content)
    mdungeons_enemies_v0_imgs = mdungeons_enemies_v0_env.render(mdungeons_enemies_v0_content)
    sokoban_v0_imgs = sokoban_v0_env.render(sokoban_v0_content)
    sokoban_large_v0_imgs = sokoban_large_v0_env.render(sokoban_large_v0_content)
    sokoban_complex_v0_imgs = sokoban_complex_v0_env.render(sokoban_complex_v0_content)
    smbtile_v0_imgs = smbtile_v0_env.render(smbtile_v0_content)
    smbtile_medium_v0_imgs = smbtile_medium_v0_env.render(smbtile_medium_v0_content)
    smbtile_small_v0_imgs = smbtile_small_v0_env.render(smbtile_small_v0_content)
    zelda_v0_imgs = zelda_v0_env.render(zelda_v0_content)
    zelda_enemies_v0_imgs = zelda_enemies_v0_env.render(zelda_enemies_v0_content)
    zelda_large_v0_imgs = zelda_large_v0_env.render(zelda_large_v0_content)

    # Save the rendered images to disk
    for i, img in enumerate(binary_v0_imgs):
        img.save(f"binary_v0_{i}.png")
    for i, img in enumerate(binary_large_v0_imgs):
        img.save(f"binary_large_v0_{i}.png")
    for i, img in enumerate(binary_wide_v0_imgs):
        img.save(f"binary_wide_v0_{i}.png")
    for i, img in enumerate(ddave_v0_imgs):
        img.save(f"ddave_v0_{i}.png")
    for i, img in enumerate(ddave_complex_v0_imgs):
        img.save(f"ddave_complex_v0_{i}.png")
    for i, img in enumerate(ddave_large_v0_imgs):
        img.save(f"ddave_large_v0_{i}.png")
    for i, img in enumerate(loderunner_v0_imgs):
        img.save(f"loderunner_v0_{i}.png")
    for i, img in enumerate(loderunner_gold_v0_imgs):
        img.save(f"loderunner_gold_v0_{i}.png")
    for i, img in enumerate(loderunner_enemies_v0_imgs):
        img.save(f"loderunner_enemies_v0_{i}.png")
    for i, img in enumerate(mdungeons_v0_imgs):
        img.save(f"mdungeons_v0_{i}.png")
    for i, img in enumerate(mdungeons_large_v0_imgs):
        img.save(f"mdungeons_large_v0_{i}.png")
    for i, img in enumerate(mdungeons_enemies_v0_imgs):
        img.save(f"mdungeons_enemies_v0_{i}.png")
    for i, img in enumerate(sokoban_v0_imgs):
        img.save(f"sokoban_v0_{i}.png")
    for i, img in enumerate(sokoban_large_v0_imgs):
        img.save(f"sokoban_large_v0_{i}.png")
    for i, img in enumerate(sokoban_complex_v0_imgs):
        img.save(f"sokoban_complex_v0_{i}.png")
    for i, img in enumerate(smbtile_v0_imgs):
        img.save(f"smbtile_v0_{i}.png")
    for i, img in enumerate(smbtile_medium_v0_imgs):
        img.save(f"smbtile_medium_v0_{i}.png")
    for i, img in enumerate(smbtile_small_v0_imgs):
        img.save(f"smbtile_small_v0_{i}.png")
    for i, img in enumerate(zelda_v0_imgs):
        img.save(f"zelda_v0_{i}.png")
    for i,	img in enumerate(zelda_enemies_v0_imgs):
       	img.save(f"zelda_enemies_v0_{i}.png")
    for i,	img in enumerate(zelda_large_v0_imgs):
        img.save(f"zelda_large_v0_{i}.png")


if __name__ == "__main__":
    __main__()